#!/usr/bin/python

import numpy as np
import pylab as p

delta = 2

x = y = np.arange(-4.0,4.01,delta)
X,Y = np.meshgrid(x,y)

Z1 = p.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = p.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)

Z = 10 * (Z1 - Z2)

nr, nc = Z.shape

Z[-nr//8: -nc//8:]=np.nan

Z = p.ma.array(Z)

Z[:nr//8, :nc//8] = np.ma.masked


print Z

"""
levels=[-2, \
        -1, \
        0,  \
        0.5,\
        1,  \
        2,  \
        8 ]
"""

levels = [ 0, 0.5, 1, 1.3, 1.31]
colors = [ '#123456','r','#9966CC', 'g', 'b']
#colors = [ '#9966CC']
        
CS = p.contourf(X,Y,Z,levels=levels, \
#                        cmap=p.cm.bone, \
                        colors=colors, \
                        origin='lower', \
                        extend='both')

                        
CS.cmap.set_under('cyan')
CS.cmap.set_over('yellow')
#p.figure()

#print CS.cmap
#p.colorbar(CS)

p.show()

#print Z.shape

