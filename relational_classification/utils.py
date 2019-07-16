#####################################################################
# Dependencies
#####################################################################
import matplotlib.pyplot as plt
import seaborn as sns

#####################################################################
# Functions
#####################################################################

    
###################################################
# ROCAUC - Bias
###################################################

def plot_rocauc_bias(df_results):
    fig,axes = plt.subplots(df_results.m.nunique(), df_results.B.nunique(), sharex=True, sharey=True, figsize=(3*df_results.B.nunique(),2*df_results.m.nunique()))

    for r,m in enumerate(sorted(df_results.m.unique())):
        for c,b in enumerate(sorted(df_results.B.unique())):

            data = df_results.query("B==@b & m==@m")

            axes[r,c].set_title("B={} | m={}".format(b,m))

            color = 'red'
            metric = 'bias'
            _ = data.plot.scatter(x='H', y='bias1', ax=axes[r,c], color=color, label=metric)        
            axes[r,c].set_ylabel(metric, color=color)
            axes[r,c].tick_params('y', colors=color)
            axes[r,c].get_legend().remove()
            axes[r,c].axhline(0.5, color=color, ls='--', lw=0.5)
            axes[r,c].set_ylim((-0.1,1.1))

            color = 'blue'
            metric = 'rocauc'
            ax = axes[r,c].twinx()
            _ = data.plot.scatter(x='H', y='rocauc', ax=ax, color=color, label=metric)
            ax.axhline(0.5, color=color, ls='--', lw=0.5)
            ax.set_ylim((-0.1,1.1))
            ax.set_ylabel(metric, color=color)
            ax.tick_params('y', colors=color)
            ax.get_legend().remove()

    plt.subplots_adjust(wspace=0.2, hspace=0.2)
    plt.tight_layout()    
    plt.show()
    plt.close()
    
###################################################
# BIAS / bias (ind)
###################################################
SCORES = ['rocauc', 'bias1']
def plot_results(df_results,score='rocauc'):

    if score not in SCORES:
        raise Exception("score ({}) not found".format(score))
                                  
    fg = sns.catplot(data=df_results,
                kind='swarm',
                col='H',row='B',
                x='pseeds',y=score,
                hue='m',
                height=1.2,
                aspect=1,
                sharex=True,sharey=True,
                legend_out=True,legend=True,
                margin_titles=True)

    nrows = df_results.B.nunique()
    ncols = df_results.H.nunique()
    for cell,ax in enumerate(fg.axes.flatten()):

        ax.axhline(0.5,ls='--',c='grey',lw=0.5, label='uniform' if score=='rocauc' else 'unbiased')

        row = int(cell/ncols)
        col = cell - (ncols*row)

        if col == 0:
            if row != int(nrows/2):
                ax.set_ylabel('')

        if ax.get_xlabel() == 'pseeds':
            
            length = len(ax.get_xticklabels())
            if length > 5:
                ax.set_xticklabels([l if i in [1,int(length/2),length-1] else '' for i,l in enumerate(ax.get_xticklabels()) ])
            
            if row == nrows-1:
                # it is last row
                if col != int(ncols/2):
                    # only middle column gets xlabel
                    ax.set_xlabel('')

    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.show()
    plt.close()

def plot_compact(df_results, score='rocauc'):    
                                  
    if score not in SCORES:
        raise Exception("score ({}) not found".format(score))
                                  
    fg = sns.catplot(data=df_results,
                kind='swarm',
                col='B',row='m',
                x='H',y=score,
                hue='pseeds',
                height=2,
                aspect=1,
                sharex=True,sharey=True,
                legend_out=True,legend=True,
                margin_titles=True)

    nrows = df_results.m.nunique()
    ncols = df_results.B.nunique()
    for cell,ax in enumerate(fg.axes.flatten()):

        ax.axhline(0.5,ls='--',c='grey',lw=0.5, label='uniform' if score=='rocauc' else 'unbiased')
        ax.set_ylim((0,1.1))

        row = int(cell/ncols)
        col = cell - (ncols*row)

        if col == 0:
            if row != int(nrows/2):
                ax.set_ylabel('')

        if ax.get_xlabel() == 'H':

            ax.set_xticklabels([l if i in [1,5,9] else '' for i,l in enumerate(ax.get_xticklabels()) ])

            if row == nrows-1:
                # it is last row
                if col != int(ncols/2):
                    # only middle column gets xlabel
                    ax.set_xlabel('')

    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.show()
    plt.close()
    

    
    
    