#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:30:09 2020

@author: trouve
"""
import os
import numpy as np
import scipy as sp
import pandas as pd
import torch
import time
import matplotlib.pyplot as plt
# gestiondes dates
from matplotlib.dates import (drange)
import datetime

from covid_predict.util.math_util import RalstonIntegrator
from  covid_predict.util.plot_util import tsplot
from  covid_predict.io import default_data_dir
import covid_predict.models.visu as visu


def ZombieSystem(param):
    (m0,alpha0,rho)= param
    def F(m, alpha):
        return (alpha*m, -rho*alpha)
    return F

def ll(param, data):
    deltat = len(data) -1# Durée de simulation
    K = 10 # nb pas temporel par jour
    nt =K*deltat # nb de pas temporel
    x0 = param[0:2] # Données initiales
    l = Shooting(x0, param, nt=nt,
                 deltat = deltat, Integrator=RalstonIntegrator())
    n = len(data)
    
    if torch.is_tensor(param):
        out = torch.zeros((1,), requires_grad = False)       
        for i in range(n):
            out = out - (data[i]*l[i*K][0].log()-l[i*K][0])
    else:
        out = np.zeros(1)
        for i in range(n):
            out = out - (data[i]*np.log(l[i*K][0])-l[i*K][0])
    return out
    
def Shooting(x0, param, nt=20, deltat = 10., Integrator= RalstonIntegrator()):
    return Integrator(ZombieSystem(param), x0, nt, deltat=deltat)

def fit_zombie(ndata, param_init = [10., 0., 0.], lr = 0.05, 
               niter = 2000, verbose = False, Adam = False):
    data = torch.from_numpy(ndata)
    param = torch.tensor(param_init, requires_grad = True)
    optimizer = torch.optim.LBFGS([param], lr, max_iter=20, max_eval=None, 
                  tolerance_grad=1e-07, tolerance_change=1e-09, 
                  history_size=100, line_search_fn=None)
    if Adam:
      optimizer = torch.optim.Adam([param], lr)
    print('performing optimization...')
    start = time.time()

    lL=[]
    def closure():
        optimizer.zero_grad()
        L = ll(param, data)
        if verbose:
            print('log likelihood', L.detach().cpu().numpy())
        L.backward()
        if verbose:
            print(param)
        lL.append(-L)
        return L

    for i in range(niter):
        if verbose:
            print('it ', i, ': ', end='')
        optimizer.step(closure)
    
    print('Optimization (L-BFGS) time: ', round(time.time() - start, 2), 
              ' seconds')
    plt.figure()
    plt.plot(lL,'k-')
    plt.title('Evolution log vraisemblance')
    plt.show()
    
    return param

def disp_fit(param, m, horizon, start = 10, label = 'morts', 
             date1 = datetime.date(2020, 2, 21)):
  
    data = torch.from_numpy(m)
    deltat = len(data) -start + horizon -1 # Durée de simulation

    date2 = date1 + datetime.timedelta(days=start)
    date3 = date2 + datetime.timedelta(days=deltat+1)
    delta = datetime.timedelta(days=1)
    dates = drange(date2, date3, delta)
    print(len(dates))
    
    K = 10 # nb pas temporel par jour
    nt =K*deltat # nb de pas temporel
    l=Shooting(param[0:2], param, nt=nt, deltat = deltat,
               Integrator=RalstonIntegrator())
    tl = tuple(map(lambda x: x[0],l))
    stl = tl[0::K]
    plt.rcParams["figure.figsize"] = (16, 4) # (w, h)

    ax = plt.subplot(121, yscale='log')
    plt.title('Prevision nb ' + label + ' cumulés (échelle log)')
    plt.plot_date(dates,stl,'-')
    date2a = date2
    date2b = date2a + datetime.timedelta(days=len(data)- start)
    plt.plot_date(drange(date2a, date2b, delta), data[start::],'o-')
    ax.xaxis.set_tick_params(rotation=30, labelsize=8)
    plt.grid()
    #plt.semilogy(np.arange(len(data)), data)

    ax = plt.subplot(122)
    plt.title('Prevision nb ' + label +  ' par jour')
    dtl = tuple(map(lambda i: stl[i+1]-stl[i], range(len(stl)-1)))
    #plt.plot_date(dates, data[1::]-data[0:-1], 'mo')
    date2a = date2 + delta
    date2b = date2a + datetime.timedelta(days=len(data)- start-1)
    plt.plot_date(drange(date2a, date2b, delta), 
                  data[start+1::]-data[start:-1], 'mo-')
    date2b = date2a + datetime.timedelta(days=deltat)
    plt.plot_date(drange(date2a, date2b, delta), dtl, 'b-')
    ax.xaxis.set_tick_params(rotation=30, labelsize=8)
    plt.grid()
    plt.show()
    
# Boelow are need functions to simulate the posterior distribution
    
def bayes_sensitivity_analysis(data_mle, theta_mle, 
        nb_days_forecast = 3, traj_horizon = 200, 
        prior_win = (0.01, 0.003), verbose = True):
    """
    Bayes predictor
    
    :data_mle: observed data used for mle of theta
    :theta_mle: mle value of theta
    :nb_previion_days: nb of prevision days
    :traj_horizon: horizon of simulated trajectories of m
    """
    
    # simulation aginst the posterior of cumulated death numbers
    zm=sample_post_m_from_data(data_mle, theta_mle, 
            traj_horizon = traj_horizon, prior_win = prior_win, 
            verbose = verbose)
    # Computation of deaths per day
    z = np.abs(zm[:,1::]-zm[:,0:-1])
    
    plt.rcParams["figure.figsize"] = (10, 4)
    ins = np.argmax(z, axis=1)
    plt.subplot(121)
    plt.boxplot(ins, labels = (' '))
    plt.title('Estimated time to peak')
    ax = plt.subplot(122)
    ax.boxplot(np.log10(np.max(z, axis = 1)), whis = [5, 95])
    plt.title('Peak height (log10 scale)')
    plt.show()

    ax = plt.subplot(111)
    labels = tuple(map(lambda x: 't+'+f'{x}', 
                       np.arange(nb_days_forecast)+1))
    ax.boxplot(z[:,0:nb_days_forecast], showfliers = False, labels = labels)
    ax.xaxis.set_tick_params(rotation=45, labelsize=8)
    plt.title('Forecast for the next ' 
              + f'{nb_days_forecast}' + ' days' )
    plt.show()

    plt.figure()
    t = np.linspace(1,200,200)
    tsplot(t, z, n=5, percentile_min=2.5, percentile_max=97.5, plot_median=True, plot_mean=False, color='g', line_color='navy')
    plt.show()

def simulate_zm(theta, N):
    """
    Simulate the law of (m_0, m_1,..., m_N) given the parameter theta
    
    :N: number of dates to simulate after t0
    :theta: parameter (m0, alpha0, rho) at day t0
    :return: a numpy array of size (N+1,)
    """
    # extract the parameter
    m0, alpha0, rho = theta
    
    # Initialization of the output times serie
    x = np.zeros(N+1)
    K = 10 # number of tempral steps per day for the integrator
    nt = K*N # Total nb of steps
    x0 = (m0, alpha0) # Initial condition
    
    # ODE integration
    l = Shooting(x0, theta, nt=nt,
                 deltat = N, Integrator = RalstonIntegrator())
    
    # Extract the m part of it
    lm = np.asarray(tuple(map(lambda x: x[0],l)))
    # Return of the time integer steps
    m = lm[0::K]
    
    # Simulation of the poisson variables
    x[0] = m0
    for i in range(N):
        x[i+1] = np.random.poisson(lam = m[i+1])
    return x


def sample_post_m_from_data(data_mle, param_mle, M = 1000, traj_horizon = 30,
                            prior_win = (0.01, 0.003), verbose = False):
    """
    Genrate samples of trajectories for m from posterior distribution
    
    :data_mle: np array of observed data used to compute the mle
    :param_mle: mle of theta
    :M: number of trajectories to be sampled
    :traj_horizon: horizon of each trajectory
    :prior_win: (alpha0_half_width, rho_half_width) half size of prior window
    :return: np array of size (M,horizon) containing the trajectories.
    """

    z = np.zeros((M ,traj_horizon+1))
    
    if verbose:
        print('Building posterior sampler')
        
    post_theta_sampler = build_post_theta_sampler_from_data(data_mle, 
                param_mle, prior_win = prior_win)
    sm0, salpha0, srho = post_theta_sampler(M)
    deltat, K = len(data_mle), 10
    nt = K*deltat
    
    if verbose:
        print('Generating posterior sample for m. Number of runs: ', M)
        
    for i in range(M):
        deltat = len(data_mle) -1 # Durée de simulation
        theta_i = (sm0[i], salpha0[i], srho[i])
        l = Shooting(theta_i[0:2], theta_i, nt=nt,
                     deltat=deltat, Integrator=RalstonIntegrator())
        theta = (l[-1][0], l[-1][1], srho[i])
        z[i,:] = simulate_zm(theta, traj_horizon)
    return  z
    
    
def build_post_theta_sampler_from_data(data_mle, 
                param_mle, prior_win = (0.01, 0.003)):
    """
    Simulation of the posterior distribution on m for a uniform prior 
    around the MLE.
    
    :data_mle: Observed data used to get param_mle
    :param_mle: MLE for theta
    :prior_win: half size window for the uniform prior aroun MLE
    :return: sampler for posterior distrib on alpha and rho (m0 is fixed)
    """
    
    def post_theta_sampler_from_density(eF, theta_grid):
        """
        Build a sampler for the posterior law of theta given density eF
        """
        (m0, alpha0, rho) = theta_grid
        pk = eF
        pk = pk/sum(pk)
        vk = np.arange(len(pk))
        sampler = sp.stats.rv_discrete(name='custm', values=(vk, pk))
        def f(M):
            sind = sampler.rvs(size=M)
            salpha0 = alpha0[sind]
            srho = rho[sind]
            sm0 = m0[sind]
            return (sm0, salpha0, srho)
        return f

    # Discretisation rate for the window
    na, nr = (81, 81)
    nparam_mle = param_mle.detach().numpy()
    da, dr = prior_win
    # Discrete samples on the window for the prior
    # m0 is not sampled and fixed to the MLE (relax ? (MCMC))
    m0_mle, alpha0_mle, rho_mle = nparam_mle[0], nparam_mle[1], nparam_mle[2]
    rect = [alpha0_mle - da, alpha0_mle + da, 
            rho_mle - dr, rho_mle + dr]
    amin, amax, rmin, rmax = rect
    alpha0, rho = np.meshgrid(np.linspace(amin,amax,na),
                              np.linspace(rmin,rmax,nr))
    m0 = m0_mle*np.ones_like(alpha0)

    # Compute of the log-likelihood on the paramter grid
    F = np.zeros_like(alpha0)
    for i in range(na):
        for j in range(nr):
            #theta_ij = torch.tensor([m0_mle, alpha0[i,j], rho[i,j]])
            theta_ij = (m0_mle, alpha0[i,j], rho[i,j])
            F[i,j] = -ll(theta_ij,data_mle)
    ind = np.unravel_index(np.argmax(F, axis=None), F.shape)
    # Max is subtracted
    F = F-F[ind]
    # Posterior density (not normalized)
    eF = np.exp(F)
    # Normalized density
    dF = eF/(4*np.sum(eF)*(da*dr)/(na*nr))
    
    
    # Contour plot of the density
    plt.rcParams["figure.figsize"] = (6, 6)
    fig = plt.figure()
    ax = fig.gca()
    acF = ax.contour(alpha0, rho, dF, 4, cmap= 'coolwarm')
    ax.clabel(acF, inline=1, fontsize=10)
    plt.ylabel('rho')
    plt.xlabel('alpha')
    plt.title('Posterior density at time 0')
    
    # Build the posterior sampler for theta
    theta_grid = (m0.flatten(), alpha0.flatten(), rho.flatten())
    sampler = post_theta_sampler_from_density(dF.flatten(), theta_grid)
    
    # Sampling of point under the posterior for visual display
    (sm0, salpha0, srho) = sampler(200)
    ax.plot(salpha0,srho,'b.')
    
    # Plot the MLE
    ax.plot(alpha0_mle,rho_mle,'ro')
    
    #   ax.plot(np.linspace(rect[0], rect[1], 100), np.zeros((100,)),'r-')
    plt.show()
    print("alpha0 = {:.2f}".format(alpha0[ind]))
    print("rho    = {:.2f}".format(rho[ind]))
    return sampler

def zm_analysis(CountryName, start, nb_days_forecast = 7, 
            niter = 100, lr = 0.05, 
            date_init_serie = (2020, 1, 22),
            prior_win = (0.01, 0.003)):
    
    if CountryName == "France":
        state = pd.read_csv(
        default_data_dir + os.path.sep + "data/data_time_series_covid19_deaths_global_france.csv")
    elif CountryName == "Italy":
        state = pd.read_csv(
        default_data_dir + os.path.sep + "data/data_time_series_covid19_deaths_global_italy.csv")
    elif CountryName == "US":
        covid = pd.read_csv(
        default_data_dir + os.path.sep + "data/time_series_covid19_deaths_global.csv")
        state = covid[covid["Country/Region"]==CountryName]
    else:
        covid = pd.read_csv(
        default_data_dir + os.path.sep + "data/time_series_covid19_deaths_global.csv")
        state = covid[covid["Country/Region"]==CountryName]
    state.head()
    
    if CountryName == "US":
        m = np.sum(state.iloc[:,4::].to_numpy(),axis = 0)
    elif CountryName == "United Kingdom":
        m = np.sum(state.iloc[:,4::].to_numpy(),axis = 0)
    else:
        m = state.iloc[0,4::].to_numpy(dtype = int)
    print(m)

    # Compute number of death per day
    mj = np.zeros_like(m)
    mj[0]=m[0]
    mj[1::]=m[1::] - m[0:-1]
    visu.show_data(mj,CountryName)

    # LSE fit of the growth rate decrease
    reg = visu.fit_slope(mj, start = start)
    # MLE of theta
    param_init = [m[start], reg[1], -reg[0]]
    param = fit_zombie(m[start::], param_init = param_init, niter = 100)
    print(param)

    # Affichage des paramètres
    date1 = datetime.date(*date_init_serie)
    disp_fit(param, m, 30, start = start, date1 = date1)
    
    # Sensitivity analysis avec forcast at 7 days with error bars
    bayes_sensitivity_analysis(m[start::], 
        param, nb_days_forecast = nb_days_forecast, prior_win = prior_win)
