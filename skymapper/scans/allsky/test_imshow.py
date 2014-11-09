import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from numpy.random import randn
from matplotlib.pyplot import imshow

def make_fig():
#    fig_sub, ax_sub= plt.subplots(1,4, figsize=(20,20), subplot_kw=dict(projection="mollweide"))
    fig_sub, ax_sub= plt.subplots(1,4, subplot_kw=dict(projection="mollweide"))

    for i in range(4):
        print i
        axi=ax_sub[i]
        scat=axi.scatter([0,1,2],[0,1,2], c=[4,5,6])
        axi.set_aspect(.6)
        axi.tick_params(axis='both', labelsize=10)
        #plt.annotate(fontsize='xx-small')
        #xtick= axi.get_xticklabels()
        #xtick.set_fontsize(20)
        #ytick= axi.get_yticklabels()
        #ytick.set_fontsize(20)
           
    fig_sub.subplots_adjust(right=0.8)
    cbar_ax = fig_sub.add_axes([0.85, 0.3, 0.01, 0.4])
    fig_sub.colorbar(scat, cax=cbar_ax)
    fig_sub.subplots_adjust(top=.75, bottom=.25)

    #ax_sub.set_aspect('auto')
    fig_sub.set_size_inches(60.0,40.0)
    #fig_sub.set_figheight(2)
    #fig_sub.set_figwidth(20)
  

    plt.savefig("example_im.png")

if __name__=='__main__':
    make_fig()
