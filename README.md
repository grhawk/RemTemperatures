Estimating the best temperature in a REMD-PT framework
======================================================

This script will estimate the best temperature for each replica given 
the temperature range and the number of replica to use.

Some info
---------
For a system of armonic oscillators the best choice of temperature is 
given by:

Tm+1 - Tm = f * Tm

f is a constant that depend on the numbers of ocillators in the system 
and on the heat capacity at constant volume.
The script runs a least-square method to optimze the value of f for a 
given number of replicas and a given range.


Have a nice REMD! 