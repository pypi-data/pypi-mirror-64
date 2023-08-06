import llabs
import matplotlib.pyplot as plt
import matplotlib as mpl

class DLAPlot:
    '''
    Main plotting routine to plot DLA systems
    '''

    def __init__(self):
        '''
        Wrap all subplots into single figure.
        '''
        fig = figure(figsize=(8.27,11.69))
        axis('off'),xticks(()),yticks(())
        subplots_adjust(left=0.05, right=0.95, bottom=0.01, top=0.93, hspace=0, wspace=0.05)
        llplot(fig,vmin=-5000,vmax=5000)
        specplot(fig)
        print('|- Plotting Lyman series...',)
        start_time = time.time()
        vmin,vmax  = -2000,3000
        for Ntrans in range(0,31,1):
            Nplot=(2*Ntrans-1)+10
            Hplot(fig,Ntrans,Nplot=Nplot,vmin=vmin,vmax=vmax)
            if Ntrans == 30:
                xticks((np.arange(vmin,vmax,400)))
        print(round(float(time.time()-start_time),3),'seconds')
        print('|- Plotting metal transitions...',)
        start_time = time.time()
        vmin,vmax  = -500,500
        for Ntrans in range(0,31,1):
            Nplot=(2*Ntrans-1)+11
            metalplot(fig,Ntrans,Nplot=Nplot,vmin=vmin,vmax=vmax)
            if Ntrans == 30:
                xticks((np.arange(vmin,vmax,100)))
        print(round(float(time.time()-start_time),3),'seconds.')
        os.system('mkdir -p ./candidates/dla/')
        savefig('./candidates/dla/'+self.qsoname+'.pdf')
        clf()

    def llplot(self,fig,vmin=-10000.,vmax=10000.,Ncol=1,Nplot=1):    
        '''
        Plot the spectrum region where the Lyman-limit is detected
    
        Parameters
        ----------
        fig   : Figure to be plotted on
        vmin  : Minimum velocity on plot in km/s
        vmax  : Maximum velocity on plot in km/s
        Ncol  : Number of columns to plot over
        Nplot : Plot number
        '''
        llinfo  = '$\lambda_\mathrm{LL,obs}$ = %.2f $\AA$  |  $\mathrm{dv}_\mathrm{LL,shift}$ = %.0f km/s'%(self.wallobs,self.dvshift)
        dlainfo = '$z_\mathrm{abs}$ = %.5f  |  $\mathrm{dv}_\mathrm{DLA}$ = %.0f km/s'%(self.zalpha,self.dlawidth)
        plt.title(self.filename+'\n'+llinfo+'\n'+dlainfo+'\n',fontsize=7)
        Nrows   = 23
        dv_neg  = -2500
        dv_pos  = 12000
        wastart = self.walldla*(2*self.c+dv_neg)/(2*self.c-dv_neg)
        waend   = self.walldla*(2*self.c+dv_pos)/(2*self.c-dv_pos)
        istart  = abs(self.wa - wastart).argmin()
        iend    = abs(self.wa - waend).argmin()
        ymax    = 1 if istart==iend else sorted(self.fl[istart:iend])[int(0.99*(iend-istart))]
        wafit   = np.arange(wastart,waend,0.05)
        ax = fig.add_subplot(Nrows,Ncol,Nplot,xlim=[wastart,waend],ylim=[-ymax,ymax])
        ax.xaxis.tick_top()
        ax.xaxis.set_major_locator(plt.FixedLocator([self.walldla,self.wallobs]))
        ax.yaxis.set_major_locator(plt.FixedLocator([0]))
        npix1a = self.npix1a
        npix1b = self.npix1b
        npix2a = self.npix2a
        npix2b = self.npix2b
        ilim = abs(self.wa-self.wallobs1).argmin()
        ax.axvline(x=self.wallobs1,color='green',lw=2,alpha=0.7)
        ax.axvspan(self.wa[ilim-npix1b],self.wa[ilim+npix1a],color='lime',lw=1,alpha=0.2,zorder=1)
        ilim = abs(self.wa-float(self.wallobs)).argmin()
        ax.axvline(x=self.wallobs,color='blue',lw=2,alpha=0.7)
        ax.axvspan(self.wa[ilim-npix2b],self.wa[ilim+npix2a],color='blue',lw=1,alpha=0.2,zorder=1)
        ax.plot(self.wa[istart:iend],self.fl[istart:iend],'black',lw=0.2)
        ax.plot(self.wa[istart:iend],self.er[istart:iend],'cyan',lw=0.2)
        ax.axhline(y=0,ls='dotted',color='red',lw=0.2)
        ax.axvline(x=float(self.walldla),color='red',lw=2,alpha=0.5)
        ax.axvline(x=float(self.wallobs),color='red',lw=2,alpha=0.5)
        #if '--dlafit' in sys.argv:
        #    fit = residual(self.fitparams,wafit)
        #    ax.plot(wafit,fit,'red',lw=0.7)
        #elif '--sdss' not in sys.argv:
        #    flux = 1.
        #    for Ntrans in range (len(self.HIlist)):
        #        flux = flux*self.p_voigt(self.N,\
        #                                 self.b,\
        #                                 wafit/(self.zalpha+1),\
        #                                 self.HIlist[Ntrans]['wave'],\
        #                                 self.HIlist[Ntrans]['gamma'],\
        #                                 self.HIlist[Ntrans]['strength'])
        #        flux  = gaussian_filter1d(flux,1.5)
        #    ax.plot(wafit,flux,'red',lw=0.7)
    
    def specplot(self,fig,Ncol=1,Nplot=2):
        '''
        Plot the spectrum region from the detected Lyman-limit to the detected Lyman-alpha
    
        Parameters
        ----------
        fig   : Figure to be plotted on
        Ncol  : Number of columns to plot over
        Nplot : Plot number
        '''
        Nrows  = 23
        ymin   = 0
        istart = abs(self.wa - ((self.zalpha+1)*self.HIlist[-1]['wave']-20)).argmin()
        iend   = abs(self.wa - ((self.zalpha+1)*self.HIlist[0]['wave']+20)).argmin()
        ymax   = 1 if istart==iend else sorted(self.fl[istart:iend])[int(0.9*(iend-istart))]
        x = self.wa[istart:iend]
        y = self.fl[istart:iend]        
        ax = fig.add_subplot(Nrows,Ncol,Nplot,xlim=[self.wa[istart],self.wa[iend]],ylim=[ymin,ymax])
        ax.yaxis.set_major_locator(NullLocator())
        ax.xaxis.set_major_locator(NullLocator())
        ax.plot(x,y,'black',lw=0.2)
        ax.plot(x,self.er[istart:iend],'cyan',lw=0.2)
        for trans in self.HIlist:
            ax.axvline(x=(self.zalpha+1)*trans['wave'], color='red', lw=0.5)
        ax.axvline(x=self.wallobs, color='lime', lw=1)
        xmin = 10*round(min(x)/10)
        xmax = 10*round(max(x)/10)
        if 10*round((xmax-xmin)/100)>0:
            ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(xmin,xmax,10*round((xmax-xmin)/100))))
        else:
            ax.xaxis.set_major_locator(plt.FixedLocator([xmin,xmax]))            
    
    def Hplot(self,fig,Ntrans,vmin=-1200.,vmax=3000.,Ncol=2,Nplot=10):    
        '''
        Plot the HI lines
    
        Parameters
        ----------
        fig    : Figure to be plotted on
        Ntrans : Transition number
        vmin   : Minimum velocity on plot in km/s
        vmax   : Maximum velocity on plot in km/s
        Ncol   : Number of columns to plot over
        Nplot  : Plot number
        '''
        Nrows   = 36
        ymin    = 0
        watrans = self.HIlist[Ntrans]['wave']*(self.zalpha+1) #observed wavelength of transition
        wabeg   = watrans*(1+vmin/self.c)
        waend   = watrans*(1+vmax/self.c)
        istart  = abs(self.wa-wabeg).argmin()
        iend    = abs(self.wa-waend).argmin()
        ymax    = 1 if istart==iend else sorted(self.fl[istart:iend])[int(0.99*(iend-istart))]
        istart  = istart-1 if istart!=0 else istart
        iend    = iend+1
        v       = self.c*((self.wa-watrans)/watrans)
        vllobs  = self.c*((self.wallobs-watrans)/watrans)
        ax = fig.add_subplot(Nrows,Ncol,Nplot,xlim=[vmin,vmax],ylim=[ymin,ymax])
        ax.xaxis.set_major_locator(NullLocator())
        ax.yaxis.set_major_locator(NullLocator())
        ax.plot(v[istart:iend],self.fl[istart:iend],'black',lw=0.2)
        ax.plot(v[istart:iend],self.er[istart:iend],'cyan',lw=0.2)
        ax.axvline(x=0,ls='dashed',color='blue',lw=0.5,alpha=0.7)
        ax.axvline(x=self.wallobs,color='red',lw=2,alpha=0.5)
        if self.zmin!=self.zmax:
            wamin = self.HIlist[Ntrans]['wave']*(self.zmin+1)
            wamax = self.HIlist[Ntrans]['wave']*(self.zmax+1)
            vmin2 = self.c*(2*(wamin-watrans)/(wamin+watrans))
            vmax2 = self.c*(2*(wamax-watrans)/(wamin+watrans))
            ax.axvline(x=vmin2,color='blue',lw=1,alpha=0.7)
            ax.axvline(x=vmax2,color='blue',lw=1,alpha=0.7)
        if '--dlasearch' in sys.argv and self.zmin!=self.zmax:
            '''Plotting the edges found of the system...'''
            ax.axvline(x=v[self.point],color='orange',lw=1,alpha=0.7)
            if Ntrans==self.nleftHI:
                ax.axvspan(vmin2,0,color='lime',lw=1)
            if Ntrans==self.nrightHI:
                ax.axvspan(0,vmax2,color='lime',lw=1)
        if '--manual' not in sys.argv:
            '''Plotting first guesses'''
            wafit = np.arange(wabeg,waend,0.05)
            v     = self.c*((wafit-watrans)/watrans)
            flux  = p_voigt(self.N,self.b,wafit/(self.zalpha+1),self.HIlist[Ntrans]['wave'],self.HIlist[Ntrans]['gamma'],self.HIlist[Ntrans]['strength'])
            ax.plot(v,flux,'red',lw=0.7,alpha=0.7)
        if '--dlafit' in sys.argv:
            '''Plotting mask'''
            y = np.ma.array(self.fl,mask=1-self.fitmask)
            ax.plot(v,y,'magenta',lw=1,alpha=0.7)
            '''Plotting fit'''
            wafit = np.arange(wabeg,waend,0.1)
            v     = self.c*((wafit-watrans)/watrans)
            fit   = residual(self.fitparams,wafit)
            ax.plot(v,fit,'magenta',lw=0.7,alpha=0.7)
    
    def metalplot(self,fig,Ntrans,vmin=-500.,vmax=500.,Ncol=2,Nplot=11):
        '''
        Plot the HI lines
    
        Parameters
        ----------
        fig    : Figure to be plotted on
        Ntrans : Transition number
        vmin   : Minimum velocity on plot in km/s
        vmax   : Maximum velocity on plot in km/s
        Ncol   : Number of columns to plot over
        Nplot  : Plot number
        '''
        Nrows   = 36
        ymin    = 0
        watrans = (self.zalpha+1.)*self.Metallist[Ntrans]['Metalwave']
        v       = (self.c*((self.wa-watrans)/self.wa))
        istart  = abs(v-vmin).argmin()
        iend    = abs(v-vmax).argmin()
        ymax    = 1 if istart==iend else sorted(self.fl[istart:iend])[int(0.99*(iend-istart))]
        istart  = istart-1 if istart!=0 else istart
        iend    = iend+1
        y       = self.fl[istart:iend]
        ax      = fig.add_subplot(Nrows,Ncol,Nplot,xlim=[vmin,vmax],ylim=[ymin,ymax])
        ax.yaxis.set_major_locator(NullLocator())
        ax.xaxis.set_major_locator(NullLocator())
        ax.plot(v[istart:iend],y,'black',lw=0.2)
        ax.text(0.9*vmin,0.2*ymax,self.Metallist[Ntrans]['Metalline']+'_'+str(int(self.Metallist[Ntrans]['Metalwave'])),color='blue',fontsize=7)
        ax.axvline(x=0, ls='dotted', color='blue', lw=0.2)
        if self.zmin!=self.zmax:
            '''Plotting the found edges of the system...'''
            wamin = self.Metallist[Ntrans]['Metalwave']*(self.zmin+1)
            wamax = self.Metallist[Ntrans]['Metalwave']*(self.zmax+1)
            vmin2 = self.c*((wamin-watrans)/watrans)
            vmax2 = self.c*((wamax-watrans)/watrans)
            ax.axvline(x=vmin2,color='blue',lw=0.2)
            ax.axvline(x=vmax2,color='blue',lw=0.2)

def wholespec():
    '''
    Plot the spectrum region from the detected Lyman-limit to the detected Lyman-alpha

    Parameters
    ----------
    fig   : Figure to be plotted on
    Ncol  : Number of columns to plot over
    Nplot : Plot number
    '''
    print('|- Plotting whole spectrum...',)
    start_time = time.time()
    fig = figure(figsize=(8.27,11.69))
    axis('off'),xticks(()),yticks(())
    subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.2, wspace=0.05)
    if self.flag==None:
        plt.title(self.qsoname+'   -   No suitable DLAs found in this spectrum!',fontsize=7)
    elif self.flag=='dlafound':
        plt.title(self.qsoname+'   |   Lyman-limit shift of %i km/s'%self.dvshift,fontsize=7)
    else:
        plt.title(self.qsoname+'   |   Lyman-limit found at %.2f'%self.wallobs,fontsize=7)
    #colcode = []
    #for k in range(0,len(self.zll)):
    #    r = lambda: randint(0,255)
    #    colcode.append('#%02X%02X%02X' % (r(),r(),r()))
    Ncol    = 1
    Nrows   = 8
    ymin    = 0
    ymax    = 1.2
    waveint = (self.wa[-1]-self.wa[0])/Nrows
    wmin    = self.wa[0]
    wmax    = self.wa[0] + waveint
    istart  = 0
    iend    = abs(self.wa - wmax).argmin()
    for i in range(1,Nrows+1):
        x    = self.wa[istart:iend]
        y    = self.fl[istart:iend]
        ymax = 1 if iend==istart else sorted(y)[int(0.95*(iend-istart))]
        ax   = fig.add_subplot(Nrows,Ncol,i,xlim=[wmin,wmax],ylim=[-ymax,ymax])
        ax.plot(x,self.er[istart:iend],'cyan',lw=0.2)
        ax.axhline(y=0,color='orange',lw=1,ls='dashed')
        if self.flag=='dlafound':
            for trans in self.HIlist:
                ax.axvline(x=(self.zalpha+1)*trans['wave'], color='red', lw=1,alpha=0.4,zorder=2)
        if self.flag!=None:
            ilim = abs(self.wa-self.wallobs1).argmin()
            ax.axvline(x=self.wallobs1,color='green',lw=2,alpha=0.7)
            ax.axvspan(self.wa[ilim-self.npix1b],self.wa[ilim+self.npix1a],color='lime',lw=1,alpha=0.2,zorder=1)
            ilim = abs(self.wa-self.wallobs).argmin()
            ax.axvline(x=self.wallobs,color='blue',lw=2,alpha=0.7)
            ax.axvspan(self.wa[ilim-self.npix2b],self.wa[ilim+self.npix2a],color='blue',lw=1,alpha=0.2,zorder=1)
        ax.plot(x,y,'black',lw=0.1,alpha=0.6,zorder=3)
        wmin   = wmax
        wmax   = wmin+waveint
        istart = iend
        iend   = abs(self.wa - wmax).argmin()
    path = 'limit' if self.flag=='llfound' else 'spec'
    os.system('mkdir -p ./candidates/'+path)
    savefig('./candidates/'+path+'/'+self.qsoname+'.pdf')
    print(round(float(time.time()-start_time),3),'seconds.')
    close(fig)
