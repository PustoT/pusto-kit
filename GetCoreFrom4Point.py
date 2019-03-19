#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import numpy as np

def getCoreFrom4Point(*pnts):

    if len(pnts) is not 4:
        print("Error in getCoreFrom4Point: invalid number of points. (Required 4, got %d.)"%(len(pnts)))
        return

    #p0, p1, p2, p3 = np.array(pnts[0]), np.array(pnts[1]), np.array(pnts[2]), np.array(pnts[3])
    a0, b0, c0 = pnts[0][0]-pnts[1][0], pnts[0][1]-pnts[1][1], pnts[0][2]-pnts[1][2]
    a1, b1, c1 = pnts[1][0]-pnts[2][0], pnts[1][1]-pnts[2][1], pnts[1][2]-pnts[2][2]
    a2, b2, c2 = pnts[2][0]-pnts[3][0], pnts[2][1]-pnts[3][1], pnts[2][2]-pnts[3][2]
    k0 = 1/2.0*(pnts[0][0]**2-pnts[1][0]**2+pnts[0][1]**2-pnts[1][1]**2+pnts[0][2]**2-pnts[1][2]**2)
    k1 = 1/2.0*(pnts[1][0]**2-pnts[2][0]**2+pnts[1][1]**2-pnts[2][1]**2+pnts[1][2]**2-pnts[2][2]**2)
    k2 = 1/2.0*(pnts[2][0]**2-pnts[3][0]**2+pnts[2][1]**2-pnts[3][1]**2+pnts[2][2]**2-pnts[3][2]**2)

    #if np.dot(np.cross(p0-p1,p0-p2),p0-p3) == 0:# too slow to use numpy, so expand them as below
    x0, y0, z0 = pnts[0][0]-pnts[1][0], pnts[0][1]-pnts[1][1], pnts[0][2]-pnts[1][2]
    x1, y1, z1 = pnts[0][0]-pnts[2][0], pnts[0][1]-pnts[2][1], pnts[0][2]-pnts[2][2]
    x2, y2, z2 = y0*z1-y1*z0, -(x0*z1-x1*z0), x0*y1-x1*y0
    x3, y3, z3 = pnts[0][0]-pnts[3][0], pnts[0][1]-pnts[3][1], pnts[0][2]-pnts[3][2]
    if x2*x3+y2*y3+z2*z3 == 0:
        print("Error in getCoreFrom4Point: input points are coplane.")
        return
    
    D = a0*b1*c2+a2*b0*c1+a1*b2*c0 - (a2*b1*c0+a1*b0*c2+a0*b2*c1)
    Dx = k0*b1*c2+k2*b0*c1+k1*b2*c0 - (k2*b1*c0+k1*b0*c2+k0*b2*c1)
    Dy = a0*k1*c2+a2*k0*c1+a1*k2*c0 - (a2*k1*c0+a1*k0*c2+a0*k2*c1)
    Dz = a0*b1*k2+a2*b0*k1+a1*b2*k0 - (a2*b1*k0+a1*b0*k2+a0*b2*k1)

    return (Dx/D, Dy/D, Dz/D)


if __name__ =='__main__':
    
    print(getCoreFrom4Point((1,0,0),(-1,0,0),(0,1,0),(0,0,1)))                  # 0,0,0
    print(getCoreFrom4Point((1,0,0),(-1,0,0),(0,-1,0),(0,0,-1)))                # 0,0,0
    print(getCoreFrom4Point((1,np.sqrt(3),0),(0,0,2),(0,0,-2),(2,0,0)))         # 0,0,0
    print(getCoreFrom4Point((1,np.sqrt(5),np.sqrt(3)),(0,0,-3),(0,3,0),(3,0,0)))# 0,0,0
    print(getCoreFrom4Point((1,2,4),(1,2,2),(1,1,3),(2,2,3)))                   # 1, 2, 3
    print(getCoreFrom4Point((np.sqrt(0.5)+1,2.5,2.5),(1,3,3),(0,2,3),(1,2,2)))  # 1, 2, 3
    print(getCoreFrom4Point((1+np.sqrt(2),1,4),(-1,2,3),(1,4,3),(3,2,3)))       # 1, 2, 3
    print(getCoreFrom4Point((1,2,4),(2,2,3),(1,1,3),(1,2,2)))                   # 1, 2, 3
    print(getCoreFrom4Point((2,1,3+np.sqrt(2)),(-1,2,3),(1,0,3),(3,2,3)))       # 1, 2, 3
    print(getCoreFrom4Point((2,2+np.sqrt(2),4),(1,2,5),(1,4,3),(3,2,3)))        # 1, 2, 3
    print(getCoreFrom4Point((2.5,2+np.sqrt(1.5),3.5),(1,2,5),(1,4,3),(3,2,3)))  # 1, 2, 3
    print(getCoreFrom4Point((10,0,0),(8,0,0),(9,1,0),(9,0,1)))                  # 9,0,0
    print(getCoreFrom4Point((1,9,0),(-1,9,0),(0,10,0),(0,9,1)))                 # 0,9,0
    print(getCoreFrom4Point((1,0,9),(-1,0,9),(0,1,9),(0,0,10)))                 # 0,0,9
    print(getCoreFrom4Point((1.1,0,0),(0.1,1.0,0),(0.1,-1.0,0),(0.1,0,1.0)))    # 0.1, 0, 0
    print(getCoreFrom4Point((3,4,6),(3,4,4),(2,4,5),(3,5,5)))                   # 3, 4, 5

    print(getCoreFrom4Point((1,2,4),(1,2,2),(1,1,3)))   # Error
    print(getCoreFrom4Point((1,2,4),(1,2,2),(1,1,3),(1,2,3),(0,0,0)))   # Error

    print(getCoreFrom4Point((1,2,4),(1,2,2),(1,1,3),(1,2,3)))   # Error
    print(getCoreFrom4Point((1,2,2),(1,2,5),(1,2,9),(1,2,3)))   # Error

    t0 = time.clock()
    for i in range(128*416):
        ans = getCoreFrom4Point((1+i*0.001,0,0),(0.1,1.0,0),(0.1,-1.0,0),(0.1,0,1+i*0.001))
    t1 = time.clock()
    print('time cost: %f s'%(t1-t0))

