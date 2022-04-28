import numpy as np
import math
#The parameters for the running of perceptron
class Perceptron:
    def __init__(self,type,learning_rate,max_iterations,problem,function,sigmoid_type=None,dfunction=None,neurons_per_layer=None):
        self.type = type
        self.max_iterations = max_iterations
        self.problem = problem
        self.function = function
        self.learning_rate = learning_rate
        self.sigmoid_type = sigmoid_type
        self.d_function = dfunction
        self.neurons_per_layer = neurons_per_layer

class Neuron:
    function = None
    d_function = None
    
    def __init__(self, w, learning_rate):
        self.w = w
        self.learning_rate = learning_rate
        self.excitement = 0
        

    def get_activation(self, entry):
        self.excitement = np.dot(self.w, entry)
        return Neuron.function(self.excitement)
        
    # Calculates the error for a neuron in the output layer using the expected_output and the neuron's activation value
    def calculate_output_delta(self,expected_output,activation):
        print(self.w) 
        return Neuron.d_function(self.excitement)*(expected_output[0]-activation[0]) #FIX
        
    # Calculates the error for a neuron in a hidden layer using the error of a superior layer
    def calculate_delta(self, superior_error):
        return Neuron.d_function(self.excitement) * np.dot(self.w, superior_error)
    
    def update_w(self,delta,activation):
        self.w += self.learning_rate*delta*activation


class Layer:
    def __init__(self, neurons):
        self.neurons = neurons
    
    def get_activations(self, entry):
        activations = []
        for neuron in self.neurons:
            activations.append(neuron.get_activation(entry))
        return activations
    
    # Returns the deltas for the neurons
    def get_deltas(self, superior_error, activation=None):
        deltas = []
        for neuron in self.neurons:
            if(activation != None):
                # If the activation value is set, it means that it's an output layer
                deltas.append(neuron.calculate_output_delta(superior_error,activation))
            else:
                deltas.append(neuron.calculate_delta(superior_error))
        return deltas

    def update_neurons(self,deltas,activations):
        for (idx,neuron) in enumerate(self.neurons):
            neuron.update_w(deltas[idx],activations[idx])


class Properties:
    beta = 0
    def __init__(self,perceptron:Perceptron,training_set,output_set):
        self.perceptron = perceptron
        self.training_set = training_set
        self.output_set = output_set


class Observables:
    def __init__(self,w,error):
        self.w = w
        self.error = error