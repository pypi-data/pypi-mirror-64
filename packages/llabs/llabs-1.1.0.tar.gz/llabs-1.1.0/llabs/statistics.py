import llabs,numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages

def llhist(data,binning,output,fit,xlimits):
    '''
    Distribution of calculated apparent shift of Lyman limit break.
    '''
    def gauss(x, a, b, c):
        return a * numpy.exp(-(x - b)**2.0 / (2 * c**2))

    (xmin,xmax) = xlimits
    fig = plt.figure(figsize=(12,7),dpi=120)
    plt.style.use('seaborn')
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0.15, wspace=0.2)
    ax   = plt.subplot(111,xlim=[xmin,xmax])
    idxs = numpy.where(numpy.logical_and(data['shift']>xmin,data['shift']<xmax))[0]
    hist = ax.hist(data['shift'][idxs],bins=binning,stacked=True,fill=True,
                   alpha=0.4,edgecolor="black",range=[xmin,xmax])
    best = numpy.where(data['SNR']>10)[0]
    ax.hist(data['shift'][best],bins=binning,stacked=True,fill=True,
            alpha=0.4,color='red',edgecolor="black",range=[xmin,xmax])
    if fit:
        x = numpy.array([0.5 * (hist[1][i] + hist[1][i+1]) for i in range(len(hist[1])-1)])
        y = hist[0]
        popt, pcov = curve_fit(gauss,x,y,p0=[20,2000,500])
        x = numpy.arange(xmin,xmax,0.1)
        y = gauss(x, *popt)
        plt.plot(x, y, lw=3, color="r")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.set_xlabel('Apparent shift in the Lyman limit break (km/s)')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.show() if output==None else plt.savefig(output)

class StatPlot:
    '''
    Statistical multiplot figures.
    '''
    def __init__(self):
        xmin,xmax = 2,5
        ymin,ymax = 0,3000
        name = 'shift-zabs.pdf'
        xlab = 'Absorption redshift'
        ylab = 'Lyman limit shift (km/s)'
        unit = ''
        print('|-',name)
        plotting(name,llabs.data['z'],llabs.data['shift'],llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax)
        if llabs.data['QSO'][0].split('/')[0].lower()=='sdss':
            print('Statistical plots not possible for SDSS spectra.')
            quit()
        xmin,xmax = 0,2500
        ymin,ymax = 0,500
        name = 'dlawidth-shift.pdf'
        xlab = 'Lyman limit shift (km/s)'
        ylab = 'DLA velocity dispersion (km/s)'
        print('|-',name)
        plotting(name,llabs.data['shift'],llabs.data['DLAwidth'],llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax)
        xmin,xmax = 0,600
        ymin,ymax = 0,1
        name = 'metew-dlawidth.pdf'
        xlab = 'DLA velocity dispersion (km/s)'
        ylab = r'Average equivalent width ($\mathrm{\AA}$)'
        print('|-',name)
        plotting(name,llabs.data['DLAwidth'],llabs.metew,llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax,yerr=llabs.metew_err)
        xmin,xmax = 0,3000
        ymin,ymax = 0,1.1*max(llabs.metew)
        name = 'metew-shift.pdf'
        xlab = 'Lyman limit shift (km/s)'
        ylab = 'Average equivalent width ($\mathrm{\AA}$)'
        print('|-',name)
        plotting(name,llabs.data['shift'],llabs.metew,llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax,yerr=llabs.metew_err)
        xmin,xmax = 0,600
        ymin,ymax = 0,1
        name = 'metfr-dlawidth.pdf'
        xlab = 'DLA velocity dispersion (km/s)'
        ylab = 'Pixel fraction of metal absorption'
        print('|-',name)
        plotting(name,llabs.data['DLAwidth'],llabs.metfr,llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax,yerr=llabs.metfr_err)
        xmin,xmax = 0,3000
        ymin,ymax = 0,1
        name = 'metfr-shift.pdf'
        xlab = 'Lyman limit shift (km/s)'
        ylab = 'Pixel fraction of metal absorption'
        print('|-',name)
        plotting(name,llabs.data['shift'],llabs.metfr,llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax,yerr=llabs.metfr_err)
        xmin,xmax = 0,1
        ymin,ymax = 0,1
        name = 'metew-metfr.pdf'
        xlab = 'Pixel fraction of metal absorption'
        ylab = 'Average equivalent width ($\mathrm{\AA}$)'
        print('|-',name)
        plotting(name,llabs.metfr,llabs.metew,llabs.data['SNR'],xlab,ylab,xmin,xmax,ymin,ymax)

    def plotting(self,name,x,y,c,xlab,ylab,xmin,xmax,ymin,ymax,xerr=None,yerr=None):
        '''
        Generic function to do all the plots in the statplots module.
        '''
        def func(x,a,b):
            return a + b*x
        #plt.rc('font', size=12, family='sans-serif')
        #plt.rc('axes', labelsize=12, linewidth=0.5)
        #plt.rc('legend', fontsize=12, handlelength=10)
        #plt.rc('xtick', labelsize=12)
        #plt.rc('ytick', labelsize=12)
        #plt.rc('lines', lw=2, mew=0.2)
        #plt.rc('grid', linewidth=1)
        style = ['o' if 'UVES' in llabs.data['QSO'][i] else 's' if 'HIRES' in llabs.data['QSO'][i] else 'd' for i in range(len(llabs.data['QSO']))]
        label = ['UVES' if 'UVES' in llabs.data['QSO'][i] else 'HIRES' if 'HIRES' in llabs.data['QSO'][i] else 'SDSS' for i in range(len(llabs.data['QSO']))]
        fig = plt.figure(figsize=(7,6))
        plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
        ax = subplot(111,xlim=[xmin,xmax],ylim=[ymin,ymax])
        for i in range(len(x)):
            xerr1 = None if xerr==None else xerr[i]
            yerr1 = None if yerr==None else yerr[i]
            scatter(x[i],y[i],marker=style[i],c=c[i],s=120,edgecolors='none',zorder=1,cmap=mpl.cm.rainbow,vmin=min(c),vmax=max(c),alpha=0.7)
            errorbar(x[i],y[i],xerr=xerr1,yerr=yerr1,fmt='o',ms=0,c='0.5',zorder=2)
        xfit = numpy.arange(0,4000,0.001)
        if yerr==None:
            coeffs,matcov = curve_fit(func,x,y)
            yfit = func(xfit,coeffs[0],coeffs[1])
            print('|  |- Unweighted fit: %.6f +/- %.6f'%(coeffs[1],numpy.sqrt(matcov[1][1])))
            plot(xfit,yfit,color='black',lw=3,ls='dashed')
        else:
            coeffs,matcov = curve_fit(func,x,y,sigma=yerr)
            yfit = func(xfit,coeffs[0],coeffs[1])
            print('|  |- Weighted fit: %.6f +/- %.6f'%(coeffs[1],numpy.sqrt(matcov[1][1])))
            plot(xfit,yfit,color='black',lw=3,ls='dashed')
        ax.set_ylabel(ylab,fontsize=12)
        ax.set_xlabel(xlab,fontsize=12)
        ax1  = fig.add_axes([0.87,0.1,0.04,0.85])
        cmap = mpl.cm.rainbow
        norm = mpl.colors.Normalize(vmin=min(c),vmax=max(c))
        cb1  = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm)
        cb1.set_label('Signal-to-Noise ratio',fontsize=12)
        plt.savefig(name)
        plt.clf()        

def metalplots(data,fname=None,metals=None):
    '''
    Scatter plot of metals.
    '''
    metals = None if metals==None else numpy.loadtxt(metals,dtype=str)
    plt.rc('font', size=12, family='sans-serif')
    plt.rc('axes', labelsize=12, linewidth=0.5)
    plt.rc('legend', fontsize=12, handlelength=10)
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    plt.rc('lines', lw=0.5, mew=0.2)
    plt.rc('grid', linewidth=1)
    fig = plt.figure(figsize=(12,10))
    plt.subplots_adjust(left=0.05, right=0.87, bottom=0.05, top=0.95, hspace=0.1, wspace=0.1)
    for j in range (1,len(llabs.Metallist)):
        metal = llabs.Metallist[j]['Metalline']+'_'+str(llabs.Metallist[j]['Metalwave']).split('.')[0]
        if metal!='ZnII_2062':
            ax = plt.subplot(6,5,j,xlim=[0,1])
            for i in range (len(data['QSO'])):
                if llabs.metals is not None:
                    met   = [float(llabs.metals[k,1]) for k in range(len(llabs.metals))]
                    cond1 = llabs.metals[:,0]==data['QSO'][i]
                    cond2 = abs(data['z'][i]-met)<0.02
                    pos   = numpy.where(numpy.logical_and(cond1,cond2))[0]
                    idx   = None if len(pos)==0 else pos[0]
                if llabs.metals is None or (idx is not None and metal in llabs.metals[idx,2].split('-')):
                    shift = data['shift'][i]
                    ewmet = data['EW_'+metal][i]
                    color = data['SNR'][i]
                    plt.scatter(ewmet,shift,c=color,s=20,edgecolors='none',zorder=2,
                                cmap=mpl.cm.rainbow,vmin=min(data['SNR']),vmax=max(data['SNR']))
            y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
            ax.yaxis.set_major_formatter(y_formatter)
            ax.set_ylim([0,5000])
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            if j<5*5: plt.setp(ax.get_xticklabels(), visible=False)
            if (j-1)%5!=0: plt.setp(ax.get_yticklabels(), visible=False)
            t1 = ax.text(0.5,0.8*llabs.limshift,metal,color='grey',ha='center',fontsize=10)
            t1.set_bbox(dict(color='white', alpha=0.7, edgecolor=None))
    ax   = fig.add_axes([0.9,0.05,0.04,0.9])
    cmap = mpl.cm.rainbow
    norm = mpl.colors.Normalize(vmin=min(data['SNR']),vmax=max(data['SNR']))
    cb1  = mpl.colorbar.ColorbarBase(ax,cmap=cmap,norm=norm)
    cb1.set_label('Estimated SNR')
    plt.show() if fname==None else plt.savefig(fname,frameon=False)

def multiplots():
    '''
    Various multiplots.
    '''
    print('|- multiplots.pdf')
    matplotlib.rc('font', size=8, family='sans-serif')
    matplotlib.rc('axes', labelsize=8, linewidth=0.5)
    matplotlib.rc('legend', fontsize=8, handlelength=10)
    matplotlib.rc('xtick', labelsize=8)
    matplotlib.rc('ytick', labelsize=8)
    matplotlib.rc('lines', lw=0.5, mew=0.2)
    matplotlib.rc('grid', linewidth=1)
    fig = plt.figure(figsize=(12,10))
    plt.subplots_adjust(left=0.07, right=0.87, bottom=0.1, top=0.95, hspace=0.2, wspace=0.25)
    totavg = []
    for i in range (len(data['QSO'])):
        totavg.append(float(data['SNR'][i]))
    ax = subplot(331)
    for i in range (len(data['QSO'])):
        llshift = float(data['shift'][i])
        coldens = float(data['N'][i])
        scatter(coldens,llshift,c=totavg[i],s=30,edgecolors='none',zorder=0,
                cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    ax.set_xlabel('HI column density (log)')
    ax.set_ylabel('Lyman limit shift (km/s)')
    ax = subplot(332)
    x,y,yerr = [],[],[]
    for i in range (len(data['QSO'])):
        EWmet = []
        llshift = float(data['shift'][i])
        for j in range (1,len(llabs.Metallist)):
            prev = llabs.Metallist[j-1]['Metalline']+'_'+str(llabs.Metallist[j-1]['Metalwave']).split('.')[0]
            name = llabs.Metallist[j]['Metalline']+'_'+str(llabs.Metallist[j]['Metalwave']).split('.')[0]
            cond2 = data['EW_'+name][i] not in ['0.00','1.00']
            cond3 = llabs.Metallist[j-1]['Metalline']!=llabs.Metallist[j]['Metalline']
            cond4 = llabs.Metallist[j-1]['Metalline']==llabs.Metallist[j]['Metalline'] and float(data['EW_'+name][i])<float(data['EW_'+prev][i])
            if cond2 and (cond3 or cond4):
                EWmet.append(float(data['EW_'+name][i]))
        if EWmet!=[] and float(data['SNR'][i])>llabs.limsnr:
            EWmed = numpy.mean(EWmet)
            errorbar(EWmed,llshift,xerr=numpy.std(EWmet),fmt='o',ms=0,c='0.7',zorder=1)
            scatter(EWmed,llshift,c=totavg[i],s=30,edgecolors='none',zorder=2,
                    cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
            x.append(numpy.mean(EWmet))
            y.append(llshift)
            yerr.append(numpy.std(EWmet))
    #fitlinear(x,y,min(x),max(x),min(y),max(y),min(x),max(x),err=yerr)
    ax.xlabel('Average Metal Absorption Equivalent Width')
    ax.ylabel('Lyman limit shift (km/s)')
    ax = subplot(333)
    for i in range (len(data['QSO'])):
        EWmet = []
        coldens = float(data['N'][i])
        for j in range (1,len(llabs.Metallist)):
            name = llabs.Metallist[j]['Metalline']+'_'+str(llabs.Metallist[j]['Metalwave']).split('.')[0]
            if data['EW_'+name][i] not in ['0.00','1.00']:
                EWmet.append(float(data['EW_'+name][i]))
        if EWmet!=[]:
            EWmet = numpy.mean(EWmet)
            scatter(coldens,EWmet,c=totavg[i],s=30,edgecolors='none',zorder=1,
                    cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    ax.xlabel('HI column density (log)')
    ax.ylabel('Average Metal Absorption Equivalent Width')
    ax = subplot(334)
    num_bins = 50
    llshift = []
    for i in range (len(data['QSO'])):
        llshift.append(float(data['shift'][i]))
    n, bins, patches = plt.hist(llshift, num_bins, facecolor='blue', alpha=0.5)
    ax.xlabel('Lyman limit shift (km/s)')
    ax = subplot(335)
    for i in range (len(data['QSO'])):
        llshift = float(data['shift'][i])
        scatter(llshift,totavg[i],c=totavg[i],s=30,edgecolors='none',zorder=1,cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    ax.xlabel(r'Lyman limit shift (km/s)')
    ax.ylabel('Estimated SNR')
    #ax = subplot(336)
    #for i in range (len(data['QSO'])):
    #    hilimit = float(data['HI_Limit'][i])
    #    llshift = float(data['shift'][i])
    #    scatter(llshift,hilimit,c=totavg[i],s=30,edgecolors='none',zorder=1,cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    #ax.xlabel('Lyman limit shift (km/s)')
    #ax.ylabel('Number of transition available')
    ax = subplot(337)
    for i in range (len(data['QSO'])):
        if data['QSO'][i] in llabs.pub[:,0]:
            k = numpy.where(llabs.pub[:,0]==data['QSO'][i])[0][0]
            llshift = float(data['shift'][i])
            errorbar(float(llabs.pub[k,1]),llshift,xerr=float(llabs.pub[k,2]),fmt='o',ms=0,c='0.5')
            scatter(float(llabs.pub[k,1]),llshift,c=totavg[i],s=30,edgecolors='none',
                    zorder=1,cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    ax.xlabel('Published D/H values (log)')
    ax.ylabel('Lyman limit shift (km/s)')
    #ax = subplot(338)
    #for i in range (len(data['QSO'])):
    #    scatter(data['Shift_fit'][i],data['Shift_guess'][i],c=totavg[i],s=30,edgecolors='none',zorder=0,cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    #ax.xlabel('Lyman limit shift from fit (km/s)')
    #ax.ylabel('Lyman limit shift from first guess (km/s)')
    ax = subplot(339)
    for i in range (len(data['QSO'])):
        EWmet,FRmet = [],[]
        for j in range (1,len(llabs.Metallist)):
            name = llabs.Metallist[j]['Metalline']+'_'+str(llabs.Metallist[j]['Metalwave']).split('.')[0]
            if data['EW_'+name][i] not in ['0.00','1.00']:
                EWmet.append(float(data['EW_'+name][i]))
            if data['FR_'+name][i] not in ['0.00','1.00']:
                FRmet.append(float(data['FR_'+name][i]))
        if EWmet!=[]:
            EWmet = numpy.mean(EWmet)
            FRmet = numpy.mean(FRmet)
            scatter(FRmet,EWmet,c=totavg[i],s=30,edgecolors='none',zorder=0,
                    cmap=mpl.cm.rainbow,vmin=min(totavg),vmax=max(totavg))
    ax.xlabel('Metal fraction')
    ax.ylabel('Metal equivalent width')
    ax  = fig.add_axes([0.9,0.1,0.04,0.85])
    cmap = mpl.cm.rainbow
    norm = mpl.colors.Normalize(vmin=min(totavg),vmax=max(totavg))
    cb1  = mpl.colorbar.ColorbarBase(ax,cmap=cmap,norm=norm)
    cb1.set_label('Estimated SNR')
    plt.savefig('multiplots.pdf')
    plt.clf()

def llregions():
    '''
    Plot of Lyman limit region for all systems in log file.
    '''
    print('|- Create plots of all the Lyman limit regions...')
    pdf_pages = PdfPages('llregions.pdf')
    i=p=0
    while (i<len(data['QSO'])):
        f   = 1
        fig = plt.figure(figsize=(8.27, 11.69))
        axis('off')
        subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.96, wspace=0, hspace=0)
        while i<len(data['QSO']) and f<=10:
            p = p + 1
            print('%4.f'%(p)+'/'+str(len(data['QSO'])),':',data['QSO'][i])
            llabs.filename   = data['QSO'][i]
            llabs.fullpath   = llabs.home+llabs.filename
            llabs.spectrum   = re.split(r'[/.]',llabs.fullpath)
            llabs.qsoname    = llabs.spectrum[-2]
            readspec()
            dv_neg  = -2500
            dv_pos  = 12000
            wastart = float(data['walldla'][i])*(2*llabs.c+dv_neg)/(2*llabs.c-dv_neg)
            waend   = float(data['walldla'][i])*(2*llabs.c+dv_pos)/(2*llabs.c-dv_pos)
            istart  = abs(llabs.wa - wastart).argmin()
            iend    = abs(llabs.wa - waend).argmin()
            ymax    = 1 if istart==iend else sorted(llabs.fl[istart:iend])[int(0.99*(iend-istart))]
            wafit   = numpy.arange(wastart,waend,0.05)
            ax = fig.add_subplot(10,1,f,xlim=[wastart,waend],ylim=[-ymax,ymax])
            ax.xaxis.tick_top()
            ax.xaxis.set_major_locator(NullLocator())
            ax.yaxis.set_major_locator(plt.FixedLocator([0]))
            npix1a = int(data['npix1a'][i])
            npix1b = int(data['npix1b'][i])
            npix2a = int(data['npix2a'][i])
            npix2b = int(data['npix2b'][i])
            ilim = abs(llabs.wa-float(data['wallobs1'][i])).argmin()
            ax.axvline(x=data['wallobs1'][i],color='green',lw=2,alpha=0.7)
            ax.axvspan(llabs.wa[ilim-npix1b],llabs.wa[ilim+npix1a],color='lime',lw=1,alpha=0.2,zorder=1)
            ilim = abs(llabs.wa-float(data['wallobs'][i])).argmin()
            ax.axvline(x=data['wallobs'][i],color='blue',lw=2,alpha=0.7)
            ax.axvspan(llabs.wa[ilim-npix2b],llabs.wa[ilim+npix2a],color='blue',lw=1,alpha=0.2,zorder=1)
            ax.plot(llabs.wa[istart:iend],llabs.fl[istart:iend],'black',lw=0.2)
            ax.plot(llabs.wa[istart:iend],llabs.er[istart:iend],'cyan',lw=0.2)
            ax.axhline(y=0,ls='dotted',color='red',lw=0.2)
            ax.axvline(x=float(data['walldla'][i]),color='red',lw=2,alpha=0.5)
            ax.axvline(x=float(data['wallobs'][i]),color='red',lw=2,alpha=0.5)
            t1 = text(float(data['walldla'][i]),0,data['walldla'][i],size=8,rotation=90,color='red',ha='center',va='center')
            t2 = text(float(data['wallobs'][i]),0,data['wallobs'][i],size=8,rotation=90,color='red',ha='center',va='center')
            t3 = text(wastart+0.99*(waend-wastart),-0.50*ymax,data['QSO'][i],size=8,color='blue',ha='right',va='center')
            t4 = text(wastart+0.99*(waend-wastart),-0.75*ymax,'%i km/s'%data['shift'][i],size=6,color='blue',ha='right',va='center')
            for t in [t1,t2,t3,t4]:
                t.set_bbox(dict(color='white', alpha=0.8, edgecolor=None))
            f = f + 1
            i = i + 1
        pdf_pages.savefig(fig)
        close(fig)
    pdf_pages.close()

def llregions2():
    '''
    Plot of Lyman limit region for all systems in log file.
    '''
    print('|- Create plots of all the Lyman limit regions...')
    pdf_pages = PdfPages('llregions.pdf')
    i=p=0
    shiftlist = data['shift']
    idxs = sorted(range(len(shiftlist)),key=lambda x:shiftlist[x],reverse=True)
    while (i<len(data['QSO'])):
        f   = 1
        fig = plt.figure(figsize=(16,12))
        axis('off')
        subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.96, wspace=0.1, hspace=0)
        nfigs = 18#27
        while i<len(data['QSO']) and f<=2*nfigs:
            k = idxs[i]
            p = p + 1
            print('%4.f'%(p)+'/'+str(len(data['QSO'])),':',data['QSO'][k])
            llabs.filename   = data['QSO'][k]
            llabs.fullpath   = llabs.home+llabs.filename
            llabs.spectrum   = re.split(r'[/.]',llabs.fullpath)
            llabs.qsoname    = llabs.spectrum[-2]
            readspec()
            # plot velocity plot of Lyman-limit regio
            wa = llabs.wa/(1+data['z'][k])
            #wastart = 0.99*min(data['walldla']) #900
            #waend   = 1300*(1+max(data['z'])) #1220
            wastart = 900
            waend   = 1220
            istart  = abs(wa - wastart).argmin()
            iend    = abs(wa - waend).argmin()
            ymax    = 1 if istart==iend else sorted(llabs.fl[istart:iend])[int(0.999*(iend-istart))]
            ax = fig.add_subplot(nfigs,2,f,xlim=[wastart,waend],ylim=[0,ymax])
            ax.xaxis.set_major_locator(NullLocator())
            ax.yaxis.set_major_locator(NullLocator())
            ax.plot(wa[istart:iend],llabs.fl[istart:iend],'black',lw=0.2)
            ax.axhline(y=0,ls='dotted',color='red',lw=0.2)
            ax.axvline(x=(data['wallobs'][k]),color='red',lw=1.5,ls='dashed')
            ax.axvline(x=1215.6701*(1+data['z'][k]),color='red',lw=1.5,ls='dotted')
            # plot rest-frame wavelength of spectrum
            vel  = 2*(llabs.wa-data['walldla'][k])/(llabs.wa+data['walldla'][k])*llabs.c 
            xmin = -3000
            xmax = 5000
            imin = abs(vel-xmin).argmin()
            imax = abs(vel-xmax).argmin()
            ymax = 1 if imin==imax else sorted(llabs.fl[imin:imax])[int(0.999*(imax-imin))]
            ax = fig.add_subplot(nfigs,2,f+1,xlim=[xmin,xmax],ylim=[0,ymax])
            ax.yaxis.set_major_locator(NullLocator())
            ax.plot(vel,llabs.fl,'black',lw=0.2)
            ax.plot(vel,llabs.er,'cyan',lw=0.2)
            ax.axvline(x=0,color='red',lw=2,alpha=0.5,ls='dashed')
            if f<2*nfigs-1:
                plt.setp(ax.get_xticklabels(), visible=False)
            npix1a = int(data['npix1a'][k])
            npix1b = int(data['npix1b'][k])
            npix2a = int(data['npix2a'][k])
            npix2b = int(data['npix2b'][k])
            #ilim = abs(llabs.wa-float(data['wallobs1'][k])).argmin()
            #ax.axvline(x=vel [ilim],color='green',lw=2,alpha=0.7,ls='dotted')
            #ax.axvspan(vel[ilim-npix1b],vel[ilim+npix1a],color='lime',lw=1,alpha=0.1,zorder=1)
            ilim = abs(llabs.wa-float(data['wallobs'][k])).argmin()
            ax.axvline(x=vel[ilim],color='blue',lw=2,alpha=0.7,ls='dotted')
            ax.axvspan(vel[ilim-npix2b],vel[ilim+npix2a],color='blue',lw=1,alpha=0.1,zorder=1)
            ax.xlabel('Velocity from DLA Lyman limit (km/s)')
            f = f + 2
            i = i + 1
        pdf_pages.savefig(fig)
        close(fig)
    pdf_pages.close()

def keyfig():
    '''
    Key figure for manuscript.
    '''
    print('|- Figure for paper...')
    data = numpy.genfromtxt(sys.argv[1],names=True,dtype=object,comments='!')
    # list metal found for each quasar
    metals = open('list_metals.dat','w')
    metals.write('system  zabs  snr  shift  trans  spread  ewidth\n')
    for i in range(len(data)):
        qso    = data['QSO'][i]
        zabs   = float(data['z'][i])
        spread = float(data['DLAwidth'][i])
        snr    = float(data['SNR'][i])
        shift  = float(data['shift'][i])
        for j in range(len(llabs.Metallist)):
            ion   = llabs.Metallist[j]['Metalline']
            wave  = str(llabs.Metallist[j]['Metalwave']).split('.')[0]
            trans = ion+'_'+wave
            width = float(data['EW_'+trans][i])
            if width>0:
                metals.write(' {:<40}'.format(str(qso)))
                metals.write(' {:>15}'.format('%.4f'%zabs))
                metals.write(' {:>15}'.format('%.4f'%snr))
                metals.write(' {:>15}'.format('%.4f'%shift))
                metals.write(' {:>15}'.format(trans))
                metals.write(' {:>15}'.format(int(spread)))
                metals.write(' {:>15}'.format('%.2f'%width))
                metals.write('\n')
    metals.close()
    # extract list of transitions
    llabs.metals = numpy.genfromtxt('list_metals.dat',names=True,dtype=object)
    translist = list(set(llabs.metals['trans']))
    # check for each system, which transitions are available
    data = open('list_availability.dat','w')
    data.write('system ')
    for trans in translist:
        data.write('%s '%trans)
    data.write('\n')
    for system in data['QSO']:
        data.write(system+' ')
        for trans in translist:
            idxs = numpy.where(numpy.logical_and(llabs.metals['system']==system,
                                           llabs.metals['trans']==trans))[0]
            flag = 0 if len(idxs)==0 else 1
            data.write('%i '%flag)
        data.write('\n')
    data.close()
    d = numpy.genfromtxt('list_availability.dat',names=True,dtype=float)
    d = pd.DataFrame(d)
    # loop over all the combinations
    if '--combination' in sys.argv:
        k = 1
        print(len(set(itertools.combinations(translist,llabs.ntrans))),'combinations...')
        data = open('t%i_combination.dat'%llabs.ntrans,'w')
        cols = ' '.join(['trans%i '%n for n in range(1,llabs.ntrans+1)])
        data.write(cols+' nmatch\n')
        for subset in itertools.combinations(translist,llabs.ntrans):
            print('%i/%i'%(k,len(set(itertools.combinations(translist,llabs.ntrans)))))
            idxs = d[(d[list(subset)] == 1).all(1)].index.tolist()
            data.write(' '.join(list(subset))+' %i\n'%len(idxs))
            k+=1
        data.close()
    # find best combination
    data    = numpy.genfromtxt('t%i_combination.dat'%llabs.ntrans,names=True,dtype=object)
    nmax    = max([float(i) for i in data['nmatch']])
    i       = numpy.where(data['nmatch']=='%i'%nmax)[0][0]
    subset  = [data['trans%i'%n][i] for n in range(1,llabs.ntrans+1)]
    idxs    = d[(d[list(subset)] == 1).all(1)].index.tolist()
    data    = numpy.genfromtxt('list_availability.dat',names=True,dtype=object)
    systems = [data['system'][i] for i in idxs]
    # store equivalent width results
    data = open('t%i_data.dat'%llabs.ntrans,'w')
    data.write('width  zabs  snr  shift  dv\n')
    # loop over every flagged system
    for system in systems:
        # initialise arrays for selected transitions
        spread,ewidth = [],[]
        for trans in subset:
            # find row index of transition for given system
            i = numpy.where(numpy.logical_and(llabs.metals['system']==system,llabs.metals['trans']==trans))[0][0]
            # add value of spread, equivalent width and snr
            spread.append(float(llabs.metals['spread'][i]))
            ewidth.append(float(llabs.metals['ewidth'][i]))
            zabs  = float(llabs.metals['zabs'][i])
            noise = float(llabs.metals['snr'][i])
            shift = float(llabs.metals['shift'][i])
        # store relevant information in data array
        data.write( '{:>9}'.format('%.4f'%numpy.mean(ewidth)))
        data.write('{:>10}'.format('%.4f'%zabs))
        data.write('{:>10}'.format('%.2f'%noise))
        data.write('{:>10}'.format('%.4f'%shift))
        data.write( '{:>9}'.format('%i'%(numpy.mean(spread))))
        data.write('\n')
    data.close()
    data = numpy.genfromtxt('t%i_data.dat'%llabs.ntrans,names=True,dtype=float)
    # Setup figure information
    rc('font', size=2)
    rc('axes', labelsize=8, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=12)
    rc('ytick', labelsize=12)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=1)
    #iremove1 = numpy.where(data['shift']>llabs.limshift)[0]
    #iremove2 = numpy.where(data['snr']<llabs.limsnr)[0]
    #iremove  = numpy.append(iremove1,iremove2)
    #for key in data.keys():
    #    data[key] = numpy.delete(data[key],iremove,axis=0)
    # define linear function to fit datasets
    def func(x,a,b):
        return a + b*x    
    # differentiate UVES and HIRES systems
    style = ['o' if 'UVES'  in system else
             's' if 'HIRES' in system else
             'd' for system in systems]
    # identify systems already studied for D/H
    color = []
    for i in range(len(systems)):
        color.append('black')
        for j in range(len(llabs.knownd2h)):
            cond1 = re.split('[/ .]',systems[i])[-2]==llabs.knownd2h[j]['name']
            cond2 = abs(float(data['zabs'][i])-llabs.knownd2h[j]['zabs'])<0.01
            if cond1 and cond2:
                color[-1]='red'
                break
    # do equivalent width vs. Lyman limit shift plot
    x,y = data['shift'],data['width']
    fig = figure(figsize=(12,5))
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0, wspace=0)
    ax = subplot(111,ylim=[0,1],xlim=[0,4000])
    for i in range(len(x)):
        order = 1 if color[i]=='black' else 2
        scatter(x[i],y[i],marker=style[i],c=color[i],s=150,edgecolors='none',zorder=order,alpha=0.6)
    xfit = numpy.arange(0,4000,0.001)
    coeffs,matcov = curve_fit(func,x,y)
    yfit = func(xfit,coeffs[0],coeffs[1])
    print('|  |- Weighted fit: %.6f +/- %.6f'%(coeffs[1],numpy.sqrt(matcov[1][1])))
    plot(xfit,yfit,color='black',lw=3,ls='dashed')
    xlabel('Lyman limit shift (km/s)',fontsize=12)
    ylabel('Average equivalent width ($\mathrm{\AA}$)',fontsize=12)
    savefig('t%i_equiwidth_vs_shift.pdf'%llabs.ntrans)
    clf()
    # do DLA velocity spread vs. Lyman limit shift plot
    x,y = data['shift'],data['dv']
    fig = figure(figsize=(7,6))
    plt.subplots_adjust(left=0.1, right=0.87, bottom=0.1, top=0.95, hspace=0, wspace=0)
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0, wspace=0)
    ax = subplot(111,ylim=[0,500],xlim=[0,2500])
    for i in range(len(x)):
        order = 1 if color[i]=='black' else 2
        scatter(x[i],y[i],marker=style[i],c=color[i],s=150,edgecolors='none',zorder=order,alpha=0.6)
    xfit = numpy.arange(0,4000,0.001)
    coeffs,matcov = curve_fit(func,x,y)
    yfit = func(xfit,coeffs[0],coeffs[1])
    print('|  |- Weighted fit: %.6f +/- %.6f'%(coeffs[1],numpy.sqrt(matcov[1][1])))
    plot(xfit,yfit,color='black',lw=3,ls='dashed')
    xlabel('Lyman limit shift (km/s)',fontsize=12)
    ylabel('DLA velocity dispersion (km/s)',fontsize=12)
    savefig('t%i_dispersion_vs_shift.pdf'%llabs.ntrans)
    clf()

def DLAwidth():

    # Read values from low resolution results
    data = numpy.genfromtxt('lowres.log',names=True,dtype=float,comments='!')
    idxs = numpy.where(numpy.logical_and(data['SNR']>10,data['DLAwidth']<2000))[0]
    xmin,xmax = min(data['DLAwidth'][idxs]),max(data['DLAwidth'][idxs])
    print(xmin,xmax)
    # Plot histogram
    fig = plt.figure(figsize=(12,7))
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0.15, wspace=0.2)
    ax = plt.subplot(111,xlim=[xmin,xmax])
    hist = ax.hist(data['DLAwidth'][idxs],bins=20,stacked=True,fill=True,alpha=0.4,edgecolor='black',range=[xmin,xmax])
    plt.title('%s identified DLA systems from SDSS-DR12 (SNR>10) - min=%i km/s, max=%i km/s'%(len(idxs),xmin,xmax))
    plt.xlabel('Velocity width of the DLA saturated region (km/s)')
    plt.ylabel('Count')
    plt.savefig('lowres')
