#!/usr/bin/env python3

import matplotlib.pylab as plt
import numpy as np
import argparse
import sys
import numpy as np
import scipy.optimize as optim

kb = 1.3806488E-23  # m^2 kg s^-2 K^-1 -> kjoule/K
precision = 0.1  # Precision used in various computations
interval = 0.01  # Interval used in sharpening or shallowing the temeperatures
factor = 3

def main():

    args = _parser()
    tmin = args.Tmin
    tmax = args.Tmax
    N = int(args.N)
#    rp = 1. - args.rp

    f = optim.leastsq(_tominimize, factor, args=(tmin, tmax, N))[0][0]
    print(f)
    rem_t = _getTemps(tmin, N, f)
    plt.plot(np.arange(len(rem_t)), np.array(rem_t), '-*', label='1st Guess')
    rem_1 = rem_t



    
    # if tmax > rem_t[-1] - (rem_t[-1] - rem_t[-2])*(rp):
    #     print('TRUE')
    #     k = 0
    #     f = 1
    #     while rem_t[-1] > tmax+interval*tmax:
    #         f += -1*precision
    #         rem_t = _getTemps(tmin, tmax, c2, N, f)
    #         k += 1
    #         if args.debug_flag: print (k, rem_t[-1])
    # else:
    #     k = 0
    #     f = 1
    #     print(tmax, rem_t[-1]-interval*tmax)
    #     while rem_t[-1] > tmax+interval*tmax:
    #         f += precision
    #         rem_t = _getTemps(tmin, tmax, c2, N, f)
    #         k += 1
    #         if args.debug_flag: print (k, rem_t[-1])
        
    # print()
    # print()
    print('Initial Parameters')
    print('Tmin: %12.6f | Tmax: %12.6f | N: %i ' % (tmin, tmax, N))
    # print('1st Guessed Temperatures')
    # print(rem_1)
    # print('Optimized Temperatures')
    print(rem_t)
    # print('Number of Replicas')
    print(len(rem_t))
    for t in enumerate(rem_t):
        pass
    
    plt.plot(np.arange(len(rem_1)), np.array([tmin] * len(rem_1)), label='Tmin')
    plt.plot(np.arange(len(rem_1)), np.array([tmax] * len(rem_1)), label='Tmax')
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
        rem_t.append(rem_t[-1] + _DeltaT(rem_t[-1],f))

    return rem_t


def _DeltaT(T, f):
    return T*f


def _parser():
    parser = argparse.ArgumentParser(version='%prog 0.1',
                                     description='Provide optimal temperatures for a REM')

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
