import numpy as np
import random
from metrics import get_continuous_metrics, get_discrete_metrics

def normalize_function(function_max,function_min,output_max,output_min,value):
    return (((output_max-output_min)*(value-function_min)) / (function_max-function_min)) + output_min

def normalize_identity(function_max,function_min,output_max,output_min,value):
    return value

def generate_noise_test_set(training_set, prob):
    noise_test_set = []
    print(prob)
    for entry in training_set:
        noise_test_set.append([])
        for value in entry:
            p = random.random()
            if(p >= prob):
                noise_test_set[-1].append(value)
            else:
                noise_test_set[-1].append(1-value)
    return noise_test_set

def parse_simple_entry_file(entry_file):
    training_set = []
    file = open(entry_file)
    lines = file.readlines()

    for i in range(0,len(lines)):
        tokens = lines[i].replace("\n", "").split("   ")
        training_set.append([])
        for token in tokens[1:len(tokens)]:
            training_set[i].append(float(token))
    
    return training_set

def parse_multilayer_entry_file(entry_file):
    training_set = []
    file = open(entry_file)
    lines = file.readlines()

    i = 0
    k = 0
    while i < len(lines):
        training_set.append([])
        for j in range(0,7):
            if(i != len(lines) -1):
                tokens = lines[i].replace(" \n", "").split(" ")
            else:
                tokens = lines[i].split(" ")[:-1]
            for token in tokens[0:len(tokens)]:
                training_set[k].append(int(token))
            i+=1
        k+=1 
    return training_set

def parse_entry_file(entry_file,type,problem):
    if(type == "linear" or type == "non_linear"):
        return parse_simple_entry_file(entry_file)
    elif(type == "multilayer"):
        if(problem == "numbers" or problem == "odd_number"):
            return parse_multilayer_entry_file(entry_file)


def parse_output_file(output_file, type):
    output_set = []
    file = open(output_file)
    lines = file.readlines()

    if(type == "non_linear"):
        normalized_func = normalize_function
    else:
        normalized_func = normalize_identity

    for i in range(0,len(lines)):
        replaced_line = lines[i].replace("   ","")
        output_set.append(float(replaced_line))
    
    return (output_set,normalized_func)

def get_problem_sets(type,problem,entry_file=None,output_file=None):
    if (type == "step"):
        if (problem == "AND"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [-1,-1,-1,1], normalize_identity, get_discrete_metrics)
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [1,1,-1,-1], normalize_identity, get_discrete_metrics)
        else:
            print("No problem found")
            exit(-1)
    elif(type == "multilayer"):
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [[1],[1],[-1],[-1]], normalize_identity, get_discrete_metrics)
        if(problem == "odd_number"):
            output_set = []
            for i in range(0,10):
                if( i%2 == 0):
                    output_set.append([1])
                else:
                    output_set.append([0])
            return(parse_entry_file(entry_file,type,problem),output_set,normalize_identity, get_discrete_metrics)
        if(problem == "numbers"):
            output_set = []
            for i in range(0,10):
                output_set.append(np.zeros(10,int))
                output_set[i][i] = 1
            return(parse_entry_file(entry_file,type,problem),output_set,normalize_identity, get_discrete_metrics)
        else:
            print("No problem found")
            exit(-1)
    elif(type == "linear" or type == "non_linear"):
        (output_set,normalize_func) = parse_output_file(output_file,type)
        return (parse_entry_file(entry_file,type,problem),output_set,normalize_func, get_continuous_metrics)
    else:
        return (None,None)