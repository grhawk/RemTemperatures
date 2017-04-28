#!/usr/bin/env python3


graph = True
try:
    import argparse
    import sys
    import numpy as np
    import scipy.optimize as optim
except ImportError:
    print('You miss some libraries... Use the following to install them:')
    print('sudo aptitude install \\')
    print('python3-numpy python3-scipy python3-matplotlib python3-args')
    print('')
    print('See you later!')
    sys.exit()

try:
    import matplotlib.pylab as plt
except ImportError:
    print('If you want to see a graph you should install matplotlib ;)')
    print('Use:')
    print('sudo aptitude install python3-matplolib')
    graph = False




factor = 2  # This is used to initialize the least-square method

def main():

    args = _parser()
    tmin = args.Tmin
    tmax = args.Tmax
    N = int(args.N)
    c = args.adjust
    if c == None:
        c = .3
#    rp = 1. - args.rp

#    f = optim.leastsq(_tominimize, factor, args=(tmin, tmax, N))[0][0]
#    rem_t = _getTemps(tmin, N, f)
    rem_t = remTempEstimator(tmin, tmax, N, c).t_list
    print(rem_t)

    print('Initial Parameters')
    print('Tmin: %12.6f | Tmax: %12.6f | N: %i ' % (tmin, tmax, N))
    print('Number of Replicas {0:4d}'.format(len(rem_t)))
    print('Copy paste the following line(s) in the ipi input')
    print
    msg = '<temp_list units=\'kelvin\'> ['
    msg += '{:7.2f}'.format(rem_t[0])
    for t in rem_t[1:]:
        msg += ', {:7.2f}'.format(t)
        if len(msg) > 50 and (len(msg) % 85 > 72): msg += '\n                '
    msg += '] </temp_list>'
    print(msg)

    if graph:
        plt.plot(np.arange(len(rem_t)), np.array([tmin] * len(rem_t)), label='Tmin')
        plt.plot(np.arange(len(rem_t)), np.array([tmax] * len(rem_t)), label='Tmax')
        plt.plot(np.arange(len(rem_t)), np.array(rem_t), '-o', label='Optimized')
        plt.legend(loc='upper left')
        plt.show()

def _parser():
    parser = argparse.ArgumentParser(
        description='Given a temperature range and a number of replicas, this script will estimate the best temperature fore each replica.')

    parser.add_argument('Tmin',
                        action='store',
                        type=float,
                        help='Smallest REM temperature')

    parser.add_argument('Tmax',
                        action='store',
                        type=float,
                        help='Highest REM temperature')

    parser.add_argument('N',
                        action='store',
                        type=int,
                        help='Number of replicas')

    parser.add_argument('--adjust',
                        action='store',
                        type=float,
                        help='scaling temperature factor')

    parser.add_argument('--debug',
                        action='store_true',
                        dest='debug_flag',
                        default=False,
                        help='be more verbose')


    return parser.parse_args()


class remTempEstimator(list):

    def __init__(self, tmin, tmax, N, c=.3):
        self.c = c
        f = optim.leastsq(self._tominimize, factor, args=(tmin, tmax, N))[0][0]
        self.t_list = self._getTemps(tmin, N, f)
#        print(self)

    def _tominimize(self, f, tmin, tmax, N):
        temp_list = self._getTemps(tmin, N, f)
        return tmax - temp_list[-1]

    def _getTemps(self, tmin, N, f):

        rem_t = [tmin]
        while True:
            if len(rem_t) == N: break
            rem_t.append(rem_t[-1] + self._DeltaT(rem_t[-1], f, len(rem_t)))

        return rem_t


    def _DeltaT(self, T, f, n):
        c = self.c
        return f * (np.exp(c*n) - np.exp(c*n-c))
        # return T * f


if __name__ == '__main__':
    main()
