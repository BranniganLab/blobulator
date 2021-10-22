import pandas as pd
import numpy as np
from amino_acids import (
    properties_charge,
    THREE_TO_ONE,
    properties_type,
    properties_hydropathy,
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from random import random
import matplotlib.gridspec as gridspec
import math


import os 


# acessing the properties of the given sequence

counter_s = 0  # this is global variable used for annotating domains in f3
counter_p = 0  #
counter_h = 0

s_counter = 0 # this is global variable used for annotating domains in f4

# character naming of domain names
ch = "a"
counter_domain_naming = ord(ch)

cmap = LinearSegmentedColormap.from_list(
    "mycmap", [(0.0 / 1, "red"), ((0.5) / 1, "whitesmoke"), (1.0, "blue")]
)

vmax=2.5
cmap_enrich = LinearSegmentedColormap.from_list('mycmap', [(0/ vmax, 'red'), (1./vmax, 'whitesmoke'), (vmax / vmax, 'blue')])

cNorm_enrich = matplotlib.colors.Normalize(vmin=0, vmax=2) #re-wrapping normalization
scalarMap_enrich = matplotlib.cm.ScalarMappable(norm=cNorm_enrich, cmap=cmap)


cmap_disorder = plt.get_cmap('PuOr')
cmap_u = plt.get_cmap('PuOr')
#This is when you want to change the scale of colormap
cNorm = matplotlib.colors.Normalize(vmin=-0.3, vmax=0.3) #re-wrapping normalization
scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap=cmap_u)
cval = scalarMap.to_rgba(0)



def compute(
    seq, cutoff, domain_threshold, window=3, my_plot=False, disorder_residues=[]):
    blob_length_cutoff_enrichment = pd.read_csv('./Table_S1.csv')

    dict_enrich = dict(zip(zip(blob_length_cutoff_enrichment['Hydrophobicity cutoff'], blob_length_cutoff_enrichment['Blob length']), blob_length_cutoff_enrichment['Enrichment ']))
    #print (blob_length_cutoff_enrichment)
    window_factor = int((window - 1) / 2)
    seq_start = 1  # starting resid for the seq
    resid_range = range(seq_start, len(seq) + 1 + seq_start)

    seq_name = []
    resid = []
    for i, j in zip(seq, resid_range):

        seq_name.append(str(i))
        resid.append(j)

    df = pd.DataFrame({"seq_name": seq_name, "resid": resid,})
    df["disorder"] = df["resid"].apply(lambda x: 1 if x in disorder_residues else 0 )
    df["hydropathy"] = [ properties_hydropathy[x] for x in df["seq_name"]] 
    df["charge"] = [properties_charge[x] for x in df["seq_name"]]           
    df["charge"] = df["charge"].astype('int')
    df["window"] = window
    df["m_cutoff"] = cutoff
    df["domain_threshold"] = domain_threshold

    #........................calcutes three residue moving window mean............................#

    df["hydropathy_3_window_mean"] = (df["hydropathy"].rolling(window=window).mean())

    if window_factor > 0:

        mean_list = df["hydropathy_3_window_mean"].tolist()
        mean_list_modified = mean_list[window_factor::] + mean_list[-window_factor::]
        df["hydropathy_3_window_mean"] = mean_list_modified

    for i in range(0,window_factor):
                resid_start = i - window_factor
                resid_end = i + window_factor
                resid_start_true = max(0, resid_start)
                true_resid_end  = min(resid_end, df.shape[0]-1)
                window_resid_list = range(resid_start_true, (true_resid_end+1))
                df['hydropathy_3_window_mean'].iloc[i] = sum([df["hydropathy"].iloc[x] for x in  window_resid_list])/len(window_resid_list)
    for i in range(df.shape[0]-window_factor,df.shape[0]):
                resid_start = i - window_factor
                resid_end = i + window_factor
                resid_start_true = max(0, resid_start)
                true_resid_end  = min(resid_end, df.shape[0]-1)
                window_resid_list = range(resid_start_true, (true_resid_end+1))
                df['hydropathy_3_window_mean'].iloc[i] = sum([df["hydropathy"].iloc[x] for x in  window_resid_list])/len(window_resid_list)
    
    

    df["hydropathy_digitized"] = [ 1 if x > cutoff else 0 if np.isnan(x)  else -1 for x in df["hydropathy_3_window_mean"]]
    #define continous stretch of residues
    df["domain_pre"] = (df["hydropathy_digitized"].groupby(df["hydropathy_digitized"].ne(df["hydropathy_digitized"].shift()).cumsum()).transform("count"))
    df["hydropathy_digitized"] = [ 1 if x > cutoff else 0 if np.isnan(x)  else -1 for x in df["hydropathy_3_window_mean"]]    

    # ..........................Define domains.........................................................#


    df["domain"] = ['h' if (x >= domain_threshold and y == 1) else 't' if y==0  else 'p' for x, y in zip(df['domain_pre'], df["hydropathy_digitized"]) ]    
    #df_g1 = df["domain"].groupby(df["domain"].ne(df["domain"].shift()).cumsum())
    df["domain_pre"] = (df["domain"].groupby(df["domain"].ne(df["domain"].shift()).cumsum()).transform("count"))  
    df["domain"] = ['t' if y=='t' else y if (x >= domain_threshold) else 's' for x, y in zip(df['domain_pre'], df["domain"]) ]
    df['blobtype'] = df['domain']

    def domain_to_numbers(x):
        """convert domains to bar height for javascript display"""
        if x[0][0] == "p":
            return 0.2
        elif x[0][0] == "h":
            return 0.6
        elif x[0][0] == "s":
            return 0.3

    df["domain_to_numbers"] = df[["domain", "hydropathy"]].apply(
        lambda x: domain_to_numbers(x), axis=1

    )

    def domain_to_skyline_numbers(x):
        """convert domains to skyline height for javascript display"""
        if x[0][0] == "p":
            return 0.2
        elif x[0][0] == "h":
            return 0.6
        else:
            return 0.3


    df["domain_for_skyline"] = df[["domain", "hydropathy"]].apply(
        lambda x: domain_to_skyline_numbers(x), axis=1

    )

    # ..........................Define domain names.........................................................#

    # give the numeric values to each domain
    def f3(x):
        global counter_s
        global counter_p
        global counter_h
        if x.name == 1:
            counter_s=0  #intitialising the global value of counter to 0
            counter_p=0
            counter_h=0
            if x.iloc[0] == 'h':
                counter_h+=1
                return x + str(counter_h)
            elif x.iloc[0] == 'p':
                counter_p+=1
                return x + str(counter_p)
            else:
                counter_s+=1
                return x + str((counter_s))


        elif len(x) >= domain_threshold:
            if x.iloc[0] == 'h':
                counter_h+=1
                return x + str(counter_h)
            else:
                counter_p+=1
                return x + str(counter_p)
        else:
            counter_s+=1
            if counter_h>=1:
                counter_h=counter_h-1
                return x + str((counter_s))
            else:
                return x + str(counter_s)#

    df['domain'] =  df['domain'].groupby(df['domain'].ne(df['domain'].shift()).cumsum()).apply(lambda x: f3(x))
    #df.loc[0,'domain']='s'
    counts_group_length = df['domain'].value_counts().to_dict()#
    

    # gives the alphabetic names to each domain
    def f4(x):
            global counter_domain_naming
            global s_counter
            if x[1][0] == 'p':
                counter_domain_naming = 0
                s_counter = 0
                return x[1]
            elif x[0] < domain_threshold:
                if x[1] == 's':
                    counter_domain_naming = 0
                    s_counter = 0
                else:
                    s_counter = s_counter + 1
                    if s_counter == x[0]:
                        counter_domain_naming = counter_domain_naming + 1
                        return x[1]
                    else:
                        return x[1]
            else:
                if counts_group_length[x[1]] != x[0]:
                    s_counter = 0
                    return x[1] + chr(ord('a')+int(counter_domain_naming))
                else:
                    s_counter = 0
                    return x[1]#

    df['domain'] = df[['domain_pre', 'domain']].apply(lambda x: f4(x),axis=1)
    df['domain'].fillna(value='s', inplace=True)

    # ..........................Define phase diagram.........................................................#
    def phase_diagram(x):
        fcr = x[1]
        ncpr = x[0]
        fp = x[2]
        fn = x[3]

        # if we're in region 1
        if fcr < 0.25:
            return "rgb(138.0,251.0,69.0)"

            # if we're in region 2
        elif fcr >= 0.25 and fcr <= 0.35:
            return "rgb(254.0,230.0,90.0)"

            # if we're in region 3
        elif fcr > 0.35 and abs(ncpr) < 0.35:
            return "mediumorchid"

            # if we're in region 4 or 5
        elif fp > 0.35:
            if fn > 0.35:
                raise SequenceException(
                    "Algorithm bug when coping with phase plot regions"
                )
            return "blue"

        elif fn > 0.35:
            return "red"

        else:  # This case is impossible but here for completeness\
            raise SequenceException(
                "Found inaccessible region of phase diagram. Numerical error"
            )


    def phase_diagram_class(x):
        fcr = x[1]
        ncpr = x[0]
        fp = x[2]
        fn = x[3]

        # if we're in region 1
        if fcr < 0.25:
            return "1"

            # if we're in region 2
        elif fcr >= 0.25 and fcr <= 0.35:
            return "2"

            # if we're in region 3
        elif fcr > 0.35 and abs(ncpr) < 0.35:
            return "3"

            # if we're in region 4 or 5
        elif fp > 0.35:
            if fn > 0.35:
                raise SequenceException(
                    "Algorithm bug when coping with phase plot regions"
                )
            return "5"

        elif fn > 0.35:
            return "4"

        else:  # This case is impossible but here for completeness\
            raise SequenceException(
                "Found inaccessible region of phase diagram. Numerical error"
            )

    # ..........................Define phase diagram.........................................................#
    def uversky_diagram(x):
        h = x[1]*1.0
        ncpr = abs(x[0])
        c = 0.413 # intercept of diagram
        a = (1/2.785)
        b=-1
        distance = abs(a*ncpr + b*h +c)/math.sqrt(a**2+b**2)
        rel_line = h-(ncpr*a) - c
        if rel_line >= 0:
            return distance * -1.0
        else:
            return distance 

    # ..........................Define NCPR.........................................................#

    def NCPR_color(x):
        ncpr = x[0]
    #Setting the limts of the ncpr graph to 0.5 and -0.5, any number higher or lower will be considered max
        if ncpr > 0.5:
            ncpr = 1
        elif ncpr < -0.5:
            ncpr = -1
        else:
            ncpr = ncpr*2
        ncpr_normalized = (ncpr + 1.0) / 2
        m_color = cmap(ncpr_normalized)

        return "rgb" + str(tuple([255 * x for x in m_color[:-1]]))

    def disorder_color(x):
        ncpr = x[0]
        m_color = cmap_disorder(ncpr)
        return "rgb" + str(tuple([255 * x for x in m_color[:-1]]))
    def uversky_color(x):
        ncpr = x[0]
        m_color = scalarMap.to_rgba(ncpr)
        return "rgb" + str(tuple([255 * x for x in m_color[:-1]]))

    def h_blob_enrichments(x):
        cutoff_prec = round(x[1], 2)
        if x[2] == 'h':
            try:
                enirch_value = dict_enrich[(cutoff_prec, x[0])]
                #m_color = cmap(enirch_value)
                #m_color = cmap_enrich(0.9)
                #m_color = scalarMap_enrich.to_rgba(2)
                m_color = scalarMap_enrich.to_rgba(enirch_value)
                return "rgb" + str(tuple([255 * x for x in m_color[:-1]]))

            except KeyError:
                return "grey"
        else:
            return "grey"


    def h_blob_enrichments_numerical(x):
        cutoff_prec = round(x[1], 2)
        if x[2] == 'h':
            try:
                enirch_value = dict_enrich[(cutoff_prec, x[0])]
                return enirch_value
            except KeyError:
                return 0
        else:
            return 0

        #ncpr = x[0]
        #m_color = cmap_disornder(ncpr)
        #return "rgb" + str(tuple([255 * x for x in m_color[:-1]]))

    # ..........................Define the properties of each identified domain.........................................................#
    domain_group = df.groupby(["domain"])

    def count_var(x, v):

        return x.values.tolist().count(v) / (x.shape[0] * 1.0)

    df["N"] = domain_group["resid"].transform("count")
    df["H"] = domain_group["hydropathy"].transform("mean")
    df["NCPR"] = domain_group["charge"].transform("mean")
    df["disorder"] = domain_group["disorder"].transform("mean")
    df["f+"] = domain_group["charge"].transform(lambda x: count_var(x, 1))
    df["f-"] = domain_group["charge"].transform(lambda x: count_var(x, -1))
    df["fcr"] = df["f-"] + df["f+"]
    df['h_blob_enrichment'] = df[["N", "m_cutoff", "blobtype"]].apply(lambda x: h_blob_enrichments(x), axis=1)
    df['h_numerical_enrichment'] = df[["N", "m_cutoff", "blobtype"]].apply(lambda x: h_blob_enrichments_numerical(x), axis=1)

    df["P_diagram"] = df[["NCPR", "fcr", "f+", "f-"]].apply(
        lambda x: phase_diagram(x), axis=1
    )
    df["blob_charge_class"] = df[["NCPR", "fcr", "f+", "f-"]].apply(
            lambda x: phase_diagram_class(x), axis=1
        )
    df["U_diagram"] = df[["NCPR", "H"]].apply(
        lambda x: uversky_diagram(x), axis=1
    )
    df["NCPR_color"] = df[["NCPR", "fcr"]].apply(
        lambda x: NCPR_color(x), axis=1
    )
    df["uversky_color"] = df[["U_diagram", "fcr"]].apply(
        lambda x: uversky_color(x), axis=1
    )

    df["disorder_color"] = df[["disorder", "fcr"]].apply(
        lambda x: disorder_color(x), axis=1
    )

    
    #print (df[["U_diagram", "NCPR", "f+", "f-", "N", "H"]].to_string())

    #--------------------------------makes matplotlib plot for download-------------------------------------#
    def make_plot (df):
        def phase_diagram_plot(x):
            fcr = x[1]
            ncpr = x[0]
            fp = x[2]
            fn = x[3]   

            # if we're in region 1
            if fcr < 0.25:
                return (0.541,0.984,0.27)   

                # if we're in region 2
            elif fcr >= 0.25 and fcr <= 0.35:
                return (0.99,0.901,0.352)   

                # if we're in region 3
            elif fcr > 0.35 and abs(ncpr) < 0.35:
                return "mediumorchid"   

                # if we're in region 4 or 5
            elif fp > 0.35:
                if fn > 0.35:
                    raise SequenceException(
                        "Algorithm bug when coping with phase plot regions"
                    )
                return "blue"   

            elif fn > 0.35:
                return "red"    

            else:  # This case is impossible but here for completeness\
                raise SequenceException(
                    "Found inaccessible region of phase diagram. Numerical error"
                )   

        # ..........................Define NCPR.........................................................#   

        def NCPR_color_plot(x):
            ncpr = x[0]
            ncpr_normalized = (ncpr + 1.0) / 2
            m_color = cmap(ncpr_normalized)
            return m_color  

        df["P_diagram"] = df[["NCPR", "fcr", "f+", "f-"]].apply(
            lambda x: phase_diagram_plot(x), axis=1
        )

        df["NCPR_color"] = df[["NCPR", "fcr"]].apply(
            lambda x: NCPR_color_plot(x), axis=1
        )
    
        ncol = 1
        nrow = 3        

        #fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(12, 4))  
        fig = plt.figure()

        gs = gridspec.GridSpec(3, 2, figure=fig, width_ratios=[3, 0.1])
        ax0 = plt.subplot(gs[0,0])
        ax1 = plt.subplot(gs[1,0])
        ax2 = plt.subplot(gs[2,0])
        ax_nc = plt.subplot(gs[2,1])
        ax_pd = plt.subplot(gs[1,1])

        #df.plot.bar(x='resid', y='hydropathy_3_window_mean', rot=0, ax= ax[0], width=1, color='dimgrey')
        ax0.set_title("Smoothed hydropathy per residue")
        ax0.bar(x=df['resid'].values[2::], height=df['hydropathy_3_window_mean'].values[2::], width = 0.9, color='dimgrey')
        ax0.axhline(y=0.37, lw=1,c='black')
        ax0.set_ylabel("Mean hydropathy\n<H>")
        ax0.set_ylim([0,1])
        #ax0.set_xlim([0,1])
        #ax0.legend()
        ax0.set_xticks(np.arange(1, df.shape[0], int(df.shape[0]/10.0)+1))    
    

        ax1.set_title("Blobs colored according to globular tendency")
        ax1.bar(x=df['resid'].values[2::], height=df['domain_to_numbers'].values[2::], width = 0.9 , color=df['P_diagram'].values[2::])
        ax1.set_ylabel("h                 p              ")
        ax1.set_ylim([0,1])
        ax1.set_xticks(np.arange(1, df.shape[0], int(df.shape[0]/10.0)+1))    

        ax2.set_title("Blobs colored according to net charge per residue")
        ax2.bar(x=df['resid'].values[2::], height=df['domain_to_numbers'].values[2::], width = 0.9 , color=df['NCPR_color'].values[2::])
        ax2.set_ylabel("h                 p             ")
        ax2.set_ylim([0,1])
        ax2.set_xticks(np.arange(1, df.shape[0], int(df.shape[0]/10.0)+1))  


        #gs23 = gridspec.GridSpecFromSubplotSpec(1, 2, f= fig[3])
        #ax1 = f.add_subplot(gs23[-1, -1])

        import matplotlib as mpl
        
        norm = mpl.colors.Normalize(vmin=-1, vmax=1)        

        # ColorbarBase derives from ScalarMappable and puts a colorbar
        # in a specified axes, so it has everything needed for a
        # standalone colorbar.  There are many more kwargs, but the
        # following gives a basic continuous colorbar with ticks
        # and labels.
        cb1 = mpl.colorbar.ColorbarBase(ax_nc, cmap=cmap,
                                        norm=norm,
                                        orientation='vertical')
        cb1.set_label('NCPR')

        #cb = matplotlib.colorbar.ColorbarBase(ax_nc, orientation='horizontal', cmap='RdBu')

        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Globular',
                          markerfacecolor=(0.541,0.984,0.27), markersize=15),
        Line2D([0], [0], marker='o', color='w', label='Janus/Boundary',
                          markerfacecolor=(0.99,0.901,0.352) , markersize=15),
        Line2D([0], [0], marker='o', color='w', label='Strong polyelectrolyte',
                          markerfacecolor="mediumorchid", markersize=15),
        Line2D([0], [0], marker='o', color='w', label='Negatively charged \n strong polyelectrolyte',
                          markerfacecolor="red", markersize=15),
        Line2D([0], [0], marker='o', color='w', label='Positively charged \n strong polyelectrolyte',
                          markerfacecolor="blue", markersize=15)
]


        ax_pd.legend(handles=legend_elements, loc='center')
        ax_pd.spines['top'].set_visible(False)
        ax_pd.spines['right'].set_visible(False)
        ax_pd.spines['bottom'].set_visible(False)
        ax_pd.spines['left'].set_visible(False)
        ax_pd.get_xaxis().set_ticks([])
        ax_pd.get_yaxis().set_ticks([])

        fig.set_size_inches(16, 4*3)
        
        #plt.savefig(figname)
        return fig

    if my_plot == False:

        return df
    else:
        figname = make_plot(df)
        return figname
        

if __name__ == "__main__":
        df = compute("MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATV", 0.4, 4)
        #df = df.rename(columns={'seq_name': 'res_name', 'm_cutoff': 'hydrophobicity_cutoff', 'domain_threshold':'minimum_blob_length', 'blobtype':'blob_hydrophobicty_class', 'N':'blob_length'})
        #print ("Writing output file")
        #df[['res_name', 'hydrophobicity_cutoff', 'minimum_blob_length', 'blob_hydrophobicty_class', 'blob_charge_class','blob_length']].to_csv("./blobulated.csv", index=False)


