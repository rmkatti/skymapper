def gen_lambda(R, lambda_min, lambda_max):
    ''' This function takes a minimum lambda, a maximum lambda, and a
    sensitivity R= lambda/del_lambda and returns a list of lambda values beginning
    at lambda_min and ending at lambda_max '''
    
    lambda_now=lambda_min
    lambda_list=[]
    

    while lambda_now < lambda_max:
        lambda_list.append(lambda_now)
        lambda_next = R_rule(R, lambda_now)   
        lambda_now=lambda_next        

    return lambda_list

def R_rule(R, lambda_in):

    return lambda_in*(1.0+1.0/R)

if __name__=='__main__':
    lambda_list2=gen_lambda(lambda_min=.75, lambda_max=1.32, R=41.5)
    print lambda_list2, len(lambda_list2)

    lambda_list3=gen_lambda(lambda_min=1.32, lambda_max=2.34, R=41.5)
    print lambda_list3, len(lambda_list3)
