import numpy as np
import pandas as pd
import math
from random import randint
import dataset_generation
import timeit
import concurrent.futures
import threading
import copy
from csv import writer



for no_of_agents in range(15,28):
    for instances in range(1,4):
        ########### Preprocessing ############
        file_name = str(no_of_agents) + '/' + str(instances) + ".txt"
        v , file_name = dataset_generation.reading_file(file_name)

        coalition = []
        dataset_generation.coalition_strutures(coalition , v)

        k = len(coalition)
        list_of_agents = coalition[k-1]
        #print("List of agents : ",list_of_agents)
        k = k + 1
        n = int(math.log(k,2))
        #print("No of agents : ",n)
        ######################################

        file_name_1 = file_name[0:1] + "_" + "parallel" + ".csv"       #creating a csv file for each probabilty distribution

        def find_bestCS_worstCS(neighbourhood):
            max_value = 0
            min_value = 0
            count = 0
            pos1 = 0
            pos2 = 0
            for i in neighbourhood:
                value = 0
                if len(i)==n and type(i[0]) is not list:
                    value = v[k-1]
                else:
                    for j in i:
                        j.sort()
                        value = value + v[coalition.index(j)]
                if value > max_value:
                    max_value = value
                    pos1 = count
                count = count + 1
            min_value = max_value
            count = 0
            for i in neighbourhood:
                value = 0
                if len(i)==n and type(i[0]) is not list:
                    value = v[k-1]
                else:
                    for j in i:
                        j.sort()
                        value = value + v[coalition.index(j)]
                if value < min_value:
                    min_value = value
                    pos2 = count
                count = count + 1
            return neighbourhood[pos1] , neighbourhood[pos2] , max_value , min_value

        def random_cs_generator():
            dp = copy.deepcopy(list_of_agents)
            rcs = list()
            while(len(dp)>0):
                r = randint(1,len(dp))
                m = list()
                for i in range(0,r):
                    sr = randint(0,len(dp)-1)
                    m.append(dp[sr])
                    del dp[sr]
                m.sort()
                rcs.append(m)
                rcs.sort()
            return rcs

        def extract(dummy , l):
            a = 0
            b = 0
            count = 0
            if len(dummy)==n and type(dummy[0]) is not list:
                for i in list_of_agents:
                    l.append([i])
            else:
                for i in dummy:
                    if len(i)>b:
                        b = len(i)
                        a = count
                    count = count + 1
                c = dummy[a].copy()
                del dummy[a]
                for j in c:
                    dummy.insert(a,[j])
                l.append(dummy)

        def shift(cs , l):
            if len(cs)==n and type(cs[0]) is not list:
                return l
            elif len(cs) == 1 and type(cs[0]) is list:
                pass
            else:
                if len(cs[1])>1:
                    cs[0].append(cs[1][0])
                    del cs[1][0]
                    cs_dummy =  copy.deepcopy(cs)
                    l.append(cs_dummy)
                    shift(cs , l)
                elif len(cs[1])==1:
                    cs[0].append(cs[1][0])
                    del cs[1]
                    cs_dummy = copy.deepcopy(cs)
                    l.append(cs_dummy)
                    shift(cs , l)

        def generate_neighbourhood(cs):
            l = []
            dummy_cs = copy.deepcopy(cs)
            extract(cs , l)
            shift(dummy_cs , l)
            return l

        def value_of_coalition(coalition_struture):
            value = 0
            if len(coalition_struture)==n and type(coalition_struture[0]) is not list:
                value = v[k-1]
            else:
                for i in coalition_struture:
                    i.sort()
                    value = value + v[coalition.index(i)]
            return value


        def tacos(list_of_agents , k , tabuList , max_iterations , start_time):
            myresult = list()
            CS = random_cs_generator()
            currentBest = copy.deepcopy(CS)
            for i in range(max_iterations):
                cs = copy.deepcopy(CS)
                #print("Coalition structure generated : ",cs,"\n")
                neighbourhood = generate_neighbourhood(cs)
                '''for neighbour in neighbourhood:
                    print(neighbour)'''
                bestCS , worstCS , max_value , min_value = find_bestCS_worstCS(neighbourhood)
                '''print("BestCS : ",bestCS)
                print("WorstCS : ",worstCS)
                print("max value : ",max_value)
                print("min value : ",min_value)
                print("\n")'''
                
                if worstCS not in tabuList:
                    tabuList.append(worstCS)
                
                if value_of_coalition(bestCS) > value_of_coalition(currentBest):
                    currentBest = bestCS

                if bestCS not in tabuList:
                    tabuList.append(bestCS)
                    CS = bestCS
                else:
                    CS = random_cs_generator()
                    while CS in tabuList:
                        CS = random_cs_generator()

            myresult.append(str(no_of_agents) + '_' + str(instances))
            myresult.append(value_of_coalition(currentBest))
            myresult.append(timeit.default_timer() -  start_time)
            with open(file_name_1 , 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(myresult)
                f_object.close()


        if __name__=="__main__":

            tabuList = []

            #max_iterations = int(input("Enter max iterations : "))
            max_iterations =10
            #no_of_threads = int(input("No of threads to be generated : "))
            no_of_threads=3
            threads = []

            #start_time = timeit.default_timer()

            for _ in range(no_of_threads):
                start_time = timeit.default_timer()
                t = threading.Thread(target = tacos , args = (list_of_agents , k , tabuList , max_iterations , start_time))
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()
            
