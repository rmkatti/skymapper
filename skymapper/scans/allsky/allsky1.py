"""
First allsky survey

"""

def allsky_survey(pointing_file, save_suffix):

    # FOV Dimensions
    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    Nstrip=21 # Number of strips on each band of FOV 

    pointings1 = read_in_allsky(pointing_file)
    pointings1=pointings1
    print len(pointings1)
    skymap = SkyMap(nside=2**8,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=pi, Nstrips=Nstrip, lambda_min1=.75, lambda_min2=1.25) 

    skyplot1=SkyPlots2()
    for i,tuple_point in enumerate(pointings1):
        print i
        skymap.make_dicts(i, tuple_point)
        
        if i in np.floor(np.linspace(1000,len(pointings1)-1,15)):
            for j,tupler in enumerate([(.75,5),(.75,.76),(1.25,1.26),(1.98,2.00)]):
                skyplot1.redundancy_plot(skymap.lambda_dict, radius_line=theta_cap1, lambda_min=tupler[0] ,lambda_max=tupler[1],plot_type='allsky', plot_title="All Sky Hits Map: [%s, %s]" %(tupler[0], tupler[1]) )        
                savename2="allsky_fullsky_%s_%s" %(i,j)
                plt.savefig( "/home/rmkatti/skymapper4/allsky_run3/%s.png" %(savename2) )   
                
   
    skymap.save_lambda_dict(save_suffix)

 
