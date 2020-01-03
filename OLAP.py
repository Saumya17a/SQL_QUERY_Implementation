#!/usr/bin/env python3

import argparse
import os
import sys
import csv


def main():
    #The following code sets up the Parser Arguements from the 
    #argparse imported 
    #This helps us to parse the arguemnts in an orderly manner
    #The variables to store content are also initialised here
    my_args = parse_args()
    header_list_verify = []
    dict_out = {}
    context_list = []
    other_ = []
    number_of_lines = 0
    
    header = []
    
    group = []
    f = False
    cmin = cmax = cmean = csum = ctop = 0
    key = ""
    
    #Adding each line of the csv in a list
    with open(my_args.input[0], encoding = 'utf-8-sig') as csv_f:
        text= csv.DictReader(csv_f)
        for i in text:      
            number_of_lines += 1  
            context_list+= [i]
            header_list_verify = [i for i in context_list[0]]
        
    
    # for il in range(1,len(sys.argv)+1):
    #     flag = True
    #     atr = getattr(my_args,sys.argv[il].strip('--'))
    #     print(atr)
        
    #     # flag, value = exists(atr, header_list_verify)
    #     if flag == False:
    #         print("Error: "+sys.argv[0]+": no field with name '"+value+"'",file = sys.stderr)
    #         exit(8)

    for argument in range(len(sys.argv)):
        
        if(sys.argv[argument] == '--group-by'):
            group,other_,f = do_group_by(context_list, header, dict_out, my_args.group_by[0],my_args)
            if(f == True):
                print("Error:  "+sys.argv[0]+": "+my_args.group_by[0]+" has been capped at 20 distinct values", file = sys.stderr)
            dict_out[my_args.group_by[0]] = group
        if(sys.argv[argument] == '--min'):
            key = "min_"+ sys.argv[argument+1]
            if(my_args.group_by != None):
                header += [key]
                dict_out[key] = do_min(context_list, header, dict_out, sys.argv[argument+1],my_args)
            else:
                header+= [key]
                dict_out[key] = do_min(context_list, header, dict_out, my_args.min[cmin],my_args)
                cmin+=1


        if(sys.argv[argument] == '--max'):
            key = "max_"+ sys.argv[argument+1]
            if(my_args.group_by != None):
                header += [key]
                dict_out[key] = do_max(context_list, header, dict_out, sys.argv[argument+1],my_args)
            else:
                header+= [key]
                dict_out[key] = do_max(context_list, header, dict_out, my_args.max[cmax],my_args)
                cmax+=1


        if(sys.argv[argument] == '--sum'):
            key = "sum_"+ sys.argv[argument+1]
            if(my_args.group_by != None):
                header += [key]
                dict_out[key] = do_sum(context_list, header, dict_out, sys.argv[argument+1],my_args)
            else:
                header+= [key]
                dict_out[key] = do_sum(context_list, header, dict_out, my_args.sum[csum],my_args)
                csum+=1
        

        
        if(sys.argv[argument] == '--mean'):
            key = "mean_"+ sys.argv[argument+1]
            if(my_args.group_by != None):
                header += [key]
                dict_out[key] = do_mean(context_list, header, dict_out, sys.argv[argument+1],my_args)
            else:
                header+= [key]
                dict_out[key] = do_mean(context_list, header, dict_out, my_args.mean[cmean],my_args)
                cmean+=1
   

        
        if(sys.argv[argument] == '--count'):
            key = "count"
            if(my_args.group_by != None):
                header += [key]
                dict_out[key] = do_count(context_list,my_args)
            else:
                header+= [key]
                dict_out[key] = number_of_lines



        if(sys.argv[argument] == '--top'):
            key = "top_"+sys.argv[argument+2]
            topkey = key
            dict_out[key] = do_topk(context_list, header, dict_out,sys.argv[argument+2],my_args, sys.argv[argument+1])
            
            header+= [key]
                
           
    
    k = 0
    if((my_args.max == None and my_args.min == None and my_args.sum == None and my_args.mean == None and my_args.top_k == None) and my_args.group_by != None ):
        header += ["count"]
        dict_out["count"] = do_count(context_list,my_args)
    
        for i in dict_out.keys():
            dict_out[i].insert(0, i)
        for key in dict_out.keys():
            vals_len = len(dict_out[key])
            break
        for i in range(0, vals_len):
            for j in dict_out.values():
                if k == len(dict_out)-1:
                    print(j[i], end="")
                else:
                    print(j[i], end=",")
                k += 1
            k = 0
            print()
        # other(my_args, other_,dict_out)
        exit(0)
    
    #Print if group by is not alone
    if(my_args.top_k == None):
        for i in dict_out.keys():
        
            dict_out[i].insert(0, i)
        for key in dict_out.keys():
            vals_len = len(dict_out[key])
            break
        k = 0
        for i in range(0, vals_len):

            for j in dict_out.values():
            
                if len(dict_out) == 1:
                    print(j[i], end="")
                else:
                    if k == len(dict_out)-1:
                        print(j[i], end="")
                    else:
                        print(j[i], end=",")
                    k += 1
            k = 0
            print()
    k = 0
    if(my_args.top_k != None):
        print(str([m for m in dict_out.keys()])[1:-1].strip("'"))
        for i in dict_out.values():
            
            for j in i:
                if i.index(j) == 0 and len(i) == 1:
                    print("'"+j+"'")
                elif(i.index(j) == 0):
                    print("'"+j, end = ",")
                elif(i.index(j) == len(i)-1):
                    print(j+"'",end='')
                else:
                    print(j,end=',')
    
        
# def other(my_args, other_,dict_out):
   
# def exists(list_args, header):
#     flag = False
#     for i in list_args:
#         for j in header:
#             if list_args == header :
#                 flag == True
#                 return flag, i
#     return flag,i
          

#The following code computes the max
def do_max(context_list, header, dict_out, name,my_args):
    dict_max = {}
    list_max = []
    list1 = []
    list_values=[]
    non_numeric = 0
    fval = 0.00
    
    if(my_args.group_by != None):
        for i in context_list:
            if i[my_args.group_by[0]] not in list1:
                list1 += [i[my_args.group_by[0]]]
        
        for j in list1: 
            new_array = [i for i in context_list if i[my_args.group_by[0]] == j]
            for value in new_array:
                try:
                    fval = float(value[name])
                except:
                    non_numeric+=1
                    if(non_numeric >= 100):
                        print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.max[0]+"'", file =sys.stderr)
                        exit(7)
                    else:
                        continue
                else:
                    list_values += [value[name]]
            
            dict_max[j] = max(list_values, key = lambda  f:float(f) )
            list_values =[]
        for key in dict_max:
            list_max+=[dict_max[key]]
        return list_max


    else:
        maximum = 0
        for number in context_list:
            try:
                fval = float(number[name])
            except:
                
                non_numeric+=1
                if(non_numeric >= 100):
                    print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.max[0]+"'", file =sys.stderr)
                    exit(7)
                else:
                    pass
            
            else:
                list_values +=[number[name]]
        
        for k,number in enumerate(list_values):
            if float(number)>float(maximum):
                maximum=number
        
        return [maximum]

#The following code computes the group by
def do_group_by(context_list, header, dict_out,name,my_args):
    dis_count = 0 
    other_ = []
    flag = False
    context_list.sort(key = lambda argument: argument[(name)])
    header.append(my_args.group_by)
    mylist = []
    
    if(my_args.group_by != None):
        for i in context_list:
            if ((i[name]) in mylist ) == False:
                dis_count += 1
                if(dis_count > 20):
                    other_ += [i[name]]
                    flag = True
                else:
                    mylist += [i[name]]
            
            
         
    return mylist, other_, flag



#The following code computes the min
def do_min(context_list, header, dict_out, name,my_args):
    
    list1 = []
    dict_min = {}
    list_min = []
    list_values = []
    non_numeric = 0
    fval = 0.0
    if(my_args.group_by != None):
        for i in context_list:
            if i[my_args.group_by[0]] not in list1:
                list1+=[i[my_args.group_by[0]]]
        for j in list1: 
            new_array = [i for i in context_list if i[my_args.group_by[0]] == j]
            for value in new_array:
                try:
                    fval = float(value[name])
                except:
                    non_numeric+=1
                    if(non_numeric >= 100):
                        print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.max[0]+"'", file =sys.stderr)
                        exit(7)
                    else:
                        continue
                else:
                    list_values += [value[name]]
        
            dict_min[j] = min(list_values, key = lambda  f:float(f) )
            list_values= []
        for key in dict_min:
            list_min+=[dict_min[key]]
        return list_min

    else:
        
        for number in context_list:
            try:
                fval = float(number[name])
            except:
                non_numeric+=1
                if(non_numeric >= 100):
                    print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.max[0]+"'", file =sys.stderr)
                    exit(7)
                else:
                    pass
            else:
                list_values += [number[name]]
           
        list_min += [min(list_values)]
        return list_min

#The following code computes the sum
def do_sum(context_list, header, dict_out, name,my_args):
    
    list1 = []
    dict_sum = {}
    list_sum = []
    list_values = []
    non_numeric = 0
    fval = 0.0
    if(my_args.group_by != None):
        for i in context_list:
            if i[my_args.group_by[0]] not in list1:
                list1.append(i[my_args.group_by[0]])

        listint=[]
        for j in list1: 
            new_array = [i for i in context_list if i[my_args.group_by[0]] == j]
            list_values = [num[my_args.sum[0]] for num in new_array]
            sum1 =0
            for k in list_values:

                try:
                    fval = float(k)
                except:
                    non_numeric+=1
                    if(non_numeric >= 100):
                        print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.sum [0]+"'", file =sys.stderr)
                        exit(7)
                    else:
                        pass
                sum1=sum1+float(k)
                
                listint.append(float(k))
            # print(sum1)
            # print(sum(listint))
            dict_sum[j] = sum1
        for key in dict_sum:
            list_sum+=[dict_sum[key]]
            
        return list_sum

    else:
        for number in context_list:
            list_values += [number[name]]
        listint = []
        for value in list_values:
            try:
                fval = float(value)
            except:
                non_numeric+=1
                if(non_numeric >= 100):
                    print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.sum[0]+"'", file =sys.stderr)
                    exit(7)
                else:
                    pass
            else:
                listint+=[float(value)]
        sum_value = sum(listint) 
        return [sum_value] 


#The following code computes the mean
def do_mean(context_list, header, dict_out, name,my_args):
    context_list
    list1 = []
    dict_mean = {}
    list_mean = []
    list_values = []
    non_numeric = 0
    fval = 0.0
    if(my_args.group_by != None):
        for i in context_list:
            if i[my_args.group_by[0]] not in list1:
                list1.append(i[my_args.group_by[0]])
        listint=[]
        lenj =0
        for j in list1: 
            new_array = [i for i in context_list if i[my_args.group_by[0]] == j]
            for num in new_array:
                list_values += [num[name]]
                lenj += 1
            sum1 = 0
            
            for k in list_values:
                try:
                    fval = float(k)
                except:
                    non_numeric+=1
                    if(non_numeric >= 100):
                        print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.mean[0]+"'", file =sys.stderr)
                        exit(7)
                    else:
                        pass
                
                listint+=[float(k)]
                sum1 += float(k)
                lenj += 1
            
            dict_mean[j] = (sum1/(lenj))
        for key in dict_mean:
            list_mean.append(dict_mean[key])
        return list_mean

    else:
        list_values = []
        for number in context_list:
            list_values += [number[name]] 
        listint = []
        for value in list_values:
            try:
                fval = float(value)
                listint+=[float(value)]
            except:
                non_numeric+=1
                if(non_numeric >= 100):
                    print("​Error: "+sys.argv[0]+":more than 100 non-numeric values found in aggregate column  ‘"+my_args.mean[0]+"'", file =sys.stderr)
                    exit(7)
                else:
                    continue
            
        mean_value = sum(listint)/float(len(listint)) 
        
        return [mean_value] 



#The following code computes the count
def do_count(context_list, my_args ):
    list1 = []
    list_values = []
    list_count = []
    dict_count = {}
    count = 0
    if(my_args.group_by != None):
        for i in context_list:
            if i[my_args.group_by[0]] not in list1:
                list1 += [i[my_args.group_by[0]]]
    
        for j in list1: 
            new_array = [i for i in context_list if i[my_args.group_by[0]] == j]
        
            for value in new_array:
                count+=1
                list_values += [value[my_args.group_by[0]]]
            dict_count[j] = count
            list_count+=[dict_count[j]]
            list_values =[]
            count = 0
        
    return list_count
            

#The following code computes the top<k><field>

def do_topk(context_list, header, dict_out,name,my_args, num):
    list_values = []
    list1 = []
    if(my_args.group_by == None):
        my_args.group_by = [name]
        list_values, other_,f = do_group_by(context_list, [], dict_out, name,my_args)
        if(int(num)> len(list_values) ):
            sys.stderr.write("Error: "+sys.argv[0]+": the <k> is bigger than expected")
            exit(6)
        if(f == True):
            sys.stderr.write(sys.argv[0] +": "+name+" has been capped at 20 distinct values")
        count_values = do_count(context_list, my_args)
        
        top_list = []
        cm = 0
        l = len(count_values)
        a = [(i,j) for j,i in zip(list_values, count_values)]
        a.sort(reverse=True)
        
        while(cm!=int(num)):
            top_list+= [str(a[cm][1])+":"+ str(a[cm][0])]
            cm+=1
        return top_list

    




def parse_args():
    myparser = argparse.ArgumentParser()
    myparser.add_argument('--input', nargs = 1,help ="Please input file name here",required = True)
    myparser.add_argument('--group-by', nargs=1,type=str,default=None)
    myparser.add_argument('--min',action ="append")
    myparser.add_argument('--max', action ="append")
    myparser.add_argument('--mean', action ="append")
    myparser.add_argument('--sum', action ="append")
    myparser.add_argument('--count',action = "store_false")
    myparser.add_argument('--top-k', nargs = 2,action = "append")
    my_args = myparser.parse_args()
    return my_args
    
if __name__ == '__main__':
    main()
