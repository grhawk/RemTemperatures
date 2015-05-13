#!/usr/bin/env python3

import matplotlib.pylab as plt
import numpy as np
import argparse
import sys
import numpy as np
import scipy.optimize as optim

factor = 3  # This is used to initialize the least-square method

def main():

    args = _parser()
    tmin = args.Tmin
    tmax = args.Tmax
    N = int(args.N)
#    rp = 1. - args.rp

    f = optim.leastsq(_tominimize, factor, args=(tmin, tmax, N))[0][0]
    rem_t = _getTemps(tmin, N, f)
    plt.plot(np.arange(len(rem_t)), np.array(rem_t), '-*', label='1st Guess')

    print('Initial Parameters')
    print('Tmin: %12.6f | Tmax: %12.6f | N: %i ' % (tmin, tmax, N))
    print('Number of Replicas {0:4d}'.format(len(rem_t)))
    print('Copy paste the following line(s) in the ipi input')
    print
    msg = '<temp_list units=\'Kelvin\'['
    for t in rem_t:
        msg += '{:7.2f} '.format(t)
        if len(msg) > 50 and (len(msg) % 85 > 72): msg += '\n                '
    msg += '] </temp_list>'
    print(msg)  

    plt.plot(np.arange(len(rem_t)), np.array([tmin] * len(rem_t)), label='Tmin')
    plt.plot(np.arange(len(rem_t)), np.array([tmax] * len(rem_t)), label='Tmax')
    plt.plot(np.arange(len(rem_t)), np.array(rem_t), '-o', label='Optimized')
    plt.legend(loc='upper left')
    plt.show()

def _tominimize(f, tmin, tmax, N):
    temp_list = _getTemps(tmin, N, f)
    return tmax - temp_list[-1]
    
def _getTemps(tmin, N, f):

    rem_t = [tmin]
    while True:
        if len(rem_t) == N: break
        rem_t.append(rem_t[-1] + _DeltaT(rem_t[-1], f))

    return rem_t


def _DeltaT(T, f):
    return T * f


def _parser():
    parser = argparse.ArgumentParser(version='%prog 0.1',
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

    parser.add_argument('--debug',
                        action='store_true',
                        dest='debug_flag',
                        default=False,
                        help='be more verbose')


    return parser.parse_args()


if __name__ == '__main__':
    main()
