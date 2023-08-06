import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot') # this was just used for the examples


def tsplot(x, y, n=20, percentile_min=1, percentile_max=99, color='r', plot_mean=True, plot_median=False, line_color='k', **kwargs):
    r"""
    from https://github.com/arviz-devs/arviz/issues/2#issuecomment-310468720
    """
    # calculate the lower and upper percentile groups, skipping 50 percentile
    perc1 = np.percentile(y, np.linspace(percentile_min, 50, num=n, endpoint=False), axis=0)
    perc2 = np.percentile(y, np.linspace(50, percentile_max, num=n+1)[1:], axis=0)

    if 'alpha' in kwargs:
        alpha = kwargs.pop('alpha')
    else:
        alpha = 1/n
    # fill lower and upper percentile groups
    for p1, p2 in zip(perc1, perc2):
        plt.fill_between(x, p1, p2, alpha=alpha, color=color, edgecolor=None)


    if plot_mean:
        plt.plot(x, np.mean(y, axis=0), color=line_color)


    if plot_median:
        plt.plot(x, np.median(y, axis=0), color=line_color)
    
    plt.show()
    #return plt.gca()

if __name__ == "__main__":

    # data
    n = 2
    k = 100
    t = np.linspace(0,2,k)
    y = 5 * np.sin(t/10) + 4*np.random.randn(n*k).reshape(n, k)

    tsplot(t, y, n=5, percentile_min=2.5, percentile_max=97.5, plot_median=True, plot_mean=False, color='g', line_color='navy')
    plt.show()
