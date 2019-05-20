# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt 

## TODO: Change file name for yourself
fname = "1551907_2086.9.txt"
stg = 0 # two stages are there in this .txt file, where we use 1 for p-V
ang = []
p1 = []
vol = []
p2 = []
for l in open(fname):
    if l[0] == 'V': stg = 1
    if l[0] != '-' and (l[0]<'0' or l[0]>'9'): continue
    if not stg:
        ang.append(float(l.split()[0]))
        p1.append(float(l.split()[1]))
    else:
        vol.append(float(l.split()[0]))
        p2.append(float(l.split()[1]))

#plt.style.use('ggplot')
plt.figure(1, figsize=(14,9))
ang, p1 = np.array(ang), np.array(p1)
plt.title("$p - \phi$ figure")
plt.xlabel("$\phi / \degree$")
plt.ylabel("$p/bar$")
plt.plot(ang, p1)
#plt.show()
plt.savefig("quest6_pphi.jpg")

plt.figure(2, figsize=(14,9))
vol, p2 = np.array(vol), np.array(p2)
plt.title("$p - V$ figure")
plt.xlabel("$V / cm^3$")
plt.ylabel("$p/bar$")
plt.plot(vol, p2)
#plt.show() # when uncommented, plt.savefig() saves a blank fig
plt.savefig("quest6_pv.jpg")
