import numpy as np
from numpy import pi

def gen_lambda(R, lambda_min, lambda_max):
    ''' This function takes a minimum lambda, a maximum lambda, and a
    sensitivity R= lambda/del_lambda and returns a list of lambda values beginning
    at lambda_min and ending at lambda_max '''
    
    lambda_now=lambda_min
    lambda_list=[]

    while lambda_now <= lambda_max:
        lambda_list.append(lambda_now)
        lambda_next = R_rule(R, lambda_now)   
        lambda_now=lambda_next        

    return lambda_list

def phi2_band(phi_Max, lambda_list3):

    lam3_arr=np.asarray(lambda_list3)
    lam3_min= lam3_arr[0]
    lam3_max=lam3_arr[-1]

    phi_max=phi_Max

    phi3_arr=(phi_max/(lam3_max-lam3_min))*(lam3_arr-lam3_min)
    
    return phi3_arr

def phi1_band(phi_Min, lambda1_list):

    lam1_arr=np.asarray(lambda1_list)
    lam1_min= lam1_arr[0]
    lam1_max=lam1_arr[-1]

    phi_min=phi_Min

    m = (2*pi-phi_min)/(lam1_max-lam1_min)

    phi1_arr= m*(lambda1_list-lam1_min) + phi_min
    
    return phi1_arr
   

def R_rule(R, lambda_in):

    return lambda_in*(1.0+1.0/R)

if __name__=='__main__':
    lambda_list2=gen_lambda(lambda_min=.75, lambda_max=1.32, R=41.95625926211772)
    print lambda_list2, len(lambda_list2)

    lambda_list3=gen_lambda(lambda_min=1.32, lambda_max=2.34, R=41.95625926211772)
    print lambda_list3, len(lambda_list3)

#    phi2=phi2_band(3.52*pi/180.0, lambda_list3)
#    print phi2, len(phi2)

#    phi1= phi1_band(6.2217, lambda_list2)
#    print phi1, len(phi1)

#    print "Band2", lambda_list3[1]-lambda_list3[0], lambda_list3[-1]-lambda_list3[-2]
#    print "Band1", lambda_list2[1]-lambda_list2[0], lambda_list2[-1]-lambda_list2[-2]

#    print "phi Band2", (phi2[1]-phi2[0])*180.0/pi, (phi2[-1]-phi2[-2])*180/pi
#    print "phi Band1", (phi1[1]-phi1[0])*180/pi, (phi1[-1]-phi1[-2])*180/pi


