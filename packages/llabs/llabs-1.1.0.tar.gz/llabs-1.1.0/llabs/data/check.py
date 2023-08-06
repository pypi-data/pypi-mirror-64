import numpy as np

zlist = np.loadtxt('sdss_redshift.dat',dtype=str)
qso,zabs = [],[]

for i in range(len(zlist)):
    print i+1,'/',len(zlist)
    if zlist[i,0] not in qso:
        qso.append(zlist[i,0])
        zabs.append(zlist[i,1])
    else:
        j = np.where(np.array(qso)==zlist[i,0])[0][0]
        zabs[j]=zlist[i,1]
                            
opfile = open('out.dat','w')
for i in range(len(qso)):
    opfile.write(qso[i]+'   '+zabs[i]+'\n')
opfile.close()
