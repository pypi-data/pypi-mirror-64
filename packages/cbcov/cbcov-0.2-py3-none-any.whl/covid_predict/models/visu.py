#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:43:31 2020

@author: trouve
"""
import torch
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.dates import (drange)
import datetime # for dates

import covid_predict.models.zm as mod

# Routine d'affichage basique des données du nombre de morts journaliers

def fit_slope(mj, start=10, label = 'morts'):
    # cumul du nombre de morts
    m = np.cumsum(mj)
    t = np.arange(np.shape(mj)[0]) # temps en jours

    plt.figure()
    # On calcule le taux d'acrroissement en tenant compte des données nulles
    num, den = mj[1::], m[0:-1]
    Dotm, mask = np.zeros((len(num),)), (num>0)&(den>0)
    Dotm[mask], Dotm[~mask] = num[mask]/den[mask], np.nan
    plt.title('Estim. taux accroissement du nb de ' + label + ' (echelle logarithmique)')                
    reg = stats.linregress(t[start:-1], np.log(Dotm[start::]))
    plt.semilogy(t[start:-1],np.exp(reg[0]*t[start:-1]+reg[1]))
    plt.semilogy(t[0:-1],Dotm)
    plt.grid(which='minor')
    plt.show()
    print('rho estimé',-reg[0])
    return reg

def show_data(mj,pays='France', label='morts'):
  nb_j = np.shape(mj)[0] # nb points de donnée

  # cumul du nombre de morts
  m = np.cumsum(mj)
  t = np.arange(nb_j) # temps en jours

  plt.rcParams["figure.figsize"] = (16, 4) # (w, h)
  plt.subplot(131)
  plt.bar(t,mj,0.5)
  plt.title('Nombre de ' + label +' journalier (' + pays +')')
  plt.grid()

  plt.subplot(132)
  plt.bar(t,m,0.5)
  plt.title('Nombre de ' + label + ' cumulés (' + pays + ')')
  plt.grid()

  plt.subplot(133)
  plt.semilogy(t,m)
  plt.title('Idem en échelle log (' + pays + ')')
  plt.grid()
  
# Affiche les resultats de la prediction du modA après calibaration
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
    l=modA.Shooting(param[0:2], param, nt=nt, deltat = deltat,
               Integrator=modA.RalstonIntegrator())
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
