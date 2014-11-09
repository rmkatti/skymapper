import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import skymapper.visualize.radial_hist as rhist
import cPickle as pickle
import os

def run_rad_hist(lambda_dict_name, lambda_min1, lambda_max1, savename):
    print "Unpickling"
    lambda_dict1= pickle.load(open(lambda_dict_name, "rb"))
    print "Unpickle Finished"

    rhist.lambda_radial_histogram(lambda_dict1, lambda_min1, lambda_max1, savename)

if __name__=='__main__':

    lambda_dict_name_path='../analyze/lambda_dict_deep_date2'
    savename_in='./deep_date2'

    dir = os.path.dirname(__file__)
    lambda_dict_name1= os.path.join(dir, lambda_dict_name_path )   
    savename1=os.path.join(dir, savename_in)

    lambda_list=[(.75,2.34),(.75,.76),(1.30,1.33),(2.26,2.34)]

    for lambda_tuple in lambda_list:

        lambda_min1=lambda_tuple[0]
        lambda_max1=lambda_tuple[1]    

        run_rad_hist(lambda_dict_name1, lambda_min1, lambda_max1, savename1)
  
