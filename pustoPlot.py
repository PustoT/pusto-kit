#!/usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

lnX=np.linspace(-1,1,256,endpoint=True)
lnY=lnX**2
pntX=np.array([-1, 0, 1])
pntY=np.array([1, 0, 1])

font = {'family' : 'SimHei',
    'weight' : 'bold',
    'size'  : '16'}
plt.rc('font', **font)        # 步骤一（设置字体的更多属性）
plt.rc('axes', unicode_minus=False) # 步骤二（解决坐标轴负数的负号显示问题）

plt.figure(figsize=(8,4))
plt.plot(lnX, lnY, 'r', label="插值曲线")
plt.scatter(pntX, pntY, c='b', marker='*', label="插值点")
plt.legend()
plt.xlabel("自变量值")
plt.ylabel("函数值")
plt.title("使用重节点差商表的埃尔米特插值结果")
plt.axis('equal')

plt.savefig(r"interpo1.png", dpi=500)



lnX=np.linspace(-2,2,256,endpoint=True)
lnY=lnX**3
pntX=np.array([-2, -1, 0, 1, 2])
pntY=np.array([-8, -1, 0, 1, 8])

font = {'family' : 'SimHei',
    'weight' : 'bold',
    'size'  : '16'}
plt.rc('font', **font)        # 步骤一（设置字体的更多属性）
plt.rc('axes', unicode_minus=False) # 步骤二（解决坐标轴负数的负号显示问题）

plt.figure(figsize=(2,8))
plt.plot(lnX, lnY, 'r', label="插值曲线")
plt.scatter(pntX, pntY, c='b', marker='*', label="插值点")
plt.legend()
plt.xlabel("自变量值")
plt.ylabel("函数值")
plt.title("分段样条插值结果")
plt.axis('equal')

plt.savefig(r"interpo2.png", dpi=500)
