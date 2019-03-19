#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import numpy as np
import torch

def getCoreFrom4Point(*pnts):

    if len(pnts) is not 4:
        print("Invalid number of points. (Required 4, got %d.)"%(len(pnts)))
        return

    a0, b0, c0 = pnts[0][0]-pnts[1][0], pnts[0][1]-pnts[1][1], pnts[0][2]-pnts[1][2]
    a1, b1, c1 = pnts[1][0]-pnts[2][0], pnts[1][1]-pnts[2][1], pnts[1][2]-pnts[2][2]
    a2, b2, c2 = pnts[2][0]-pnts[3][0], pnts[2][1]-pnts[3][1], pnts[2][2]-pnts[3][2]
    k0 = 1/2.0*(pnts[0][0]**2-pnts[1][0]**2+pnts[0][1]**2-pnts[1][1]**2+pnts[0][2]**2-pnts[1][2]**2)
    k1 = 1/2.0*(pnts[1][0]**2-pnts[2][0]**2+pnts[1][1]**2-pnts[2][1]**2+pnts[1][2]**2-pnts[2][2]**2)
    k2 = 1/2.0*(pnts[2][0]**2-pnts[3][0]**2+pnts[2][1]**2-pnts[3][1]**2+pnts[2][2]**2-pnts[3][2]**2)

    # 370+ ms
    D = a0*b1*c2+a2*b0*c1+a1*b2*c0 - (a2*b1*c0+a1*b0*c2+a0*b2*c1)
    Dx = k0*b1*c2+k2*b0*c1+k1*b2*c0 - (k2*b1*c0+k1*b0*c2+k0*b2*c1)
    Dy = a0*k1*c2+a2*k0*c1+a1*k2*c0 - (a2*k1*c0+a1*k0*c2+a0*k2*c1)
    Dz = a0*b1*k2+a2*b0*k1+a1*b2*k0 - (a2*b1*k0+a1*b0*k2+a0*b2*k1)

    # 1900+ ms
    #D = np.linalg.det(np.array([[a0,b0,c0],[a1,b1,c1],[a2,b2,c2]]))
    #Dx = np.linalg.det(np.array([[k0,b0,c0],[k1,b1,c1],[k2,b2,c2]]))
    #Dy = np.linalg.det(np.array([[a0,k0,c0],[a1,k1,c1],[a2,k2,c2]]))
    #Dz = np.linalg.det(np.array([[a0,b0,k0],[a1,b1,k1],[a2,b2,k2]]))

    return (Dx/D, Dy/D, Dz/D)

'''
# np.linalg.solve edition. 840+ ms, BAD
def getCoreFrom4Point02(*pnts):

    if len(pnts) is not 4:
        print("Invalid number of points. (Required 4, got %d.)"%(len(pnts)))
        return
    
    para_left = np.array([
            [pnts[0][0]-pnts[1][0], pnts[0][1]-pnts[1][1], pnts[0][2]-pnts[1][2]],
            [pnts[1][0]-pnts[2][0], pnts[1][1]-pnts[2][1], pnts[1][2]-pnts[2][2]],
            [pnts[2][0]-pnts[3][0], pnts[2][1]-pnts[3][1], pnts[2][2]-pnts[3][2]]
            ])
    para_right = np.array([
            1/2.0*(pnts[0][0]**2-pnts[1][0]**2+pnts[0][1]**2-pnts[1][1]**2+pnts[0][2]**2-pnts[1][2]**2),
            1/2.0*(pnts[1][0]**2-pnts[2][0]**2+pnts[1][1]**2-pnts[2][1]**2+pnts[1][2]**2-pnts[2][2]**2),
            1/2.0*(pnts[2][0]**2-pnts[3][0]**2+pnts[2][1]**2-pnts[3][1]**2+pnts[2][2]**2-pnts[3][2]**2)
            ])

    return np.linalg.solve(para_left, para_right)
'''


t0 = time.clock()

for i in range(128*416):
    ans = getCoreFrom4Point((1+i*0.001,0,0),(0.1,1.0,0),(0.1,-1.0,0),(0.1,0,1+i*0.001))
    #print(getCoreFrom4Point((1.1,0,0),(0.1,1.0,0),(0.1,-1.0,0),(0.1,0,1.0)))    # 0.1, 0, 0
#print(getCoreFrom4Point((3,4,6),(3,4,4),(2,4,5),(3,5,5)))                   # 3, 4, 5
#print(getCoreFrom4Point((1,2,4),(1,2,2),(1,1,3),(2,2,3)))                   # 1, 2, 3

t1 = time.clock()

print('final result: %f, %f, %f' % (ans[0], ans[1], ans[2]) )
print('time cost: %f s'%(t1-t0))
