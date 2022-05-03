import numpy as np
#The parameters for the running of perceptron
class Perceptron:
    def __init__(self,type,learning_rate,max_epochs,min_error,problem,function,sigmoid_type=None,dfunction=None,neurons_per_layer=None):
        self.type = type
        self.max_epochs = max_epochs
        self.min_error = min_error 
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
        return Neuron.d_function(self.excitement)*(expected_output-activation)
        
    # Calculates the error for a neuron in a hidden layer using the error of a superior layer
    def calculate_delta(self, superior_delta,w_aux):
        return (Neuron.d_function(self.excitement) * np.dot(w_aux,superior_delta))
    
    def update_w(self,delta,activations):
        increments = []
        for activation in activations:
            increments.append(self.learning_rate*activation*delta)
        self.w += increments

class ThresholdNeuron:

    def get_activation(self,entry):
        return -1


class Layer:
    def __init__(self, neurons):
        self.neurons = neurons
    
    def get_activations(self, entry):
        activations = []
        for neuron in self.neurons:
            activations.append(neuron.get_activation(entry))
        return activations
    
    # Returns the deltas for the neurons
    def get_deltas(self, superior_error,superior_layer=None,activations=None,isBelowOutput=False):
        deltas = []
        superior_weights = []
        if(superior_layer != None):
            if (isBelowOutput):
                for neuron in superior_layer.neurons[:]:
                    superior_weights.append(neuron.w)
            else:
                for neuron in superior_layer.neurons[1:]:
                    superior_weights.append(neuron.w)
        for (idx,neuron) in enumerate(self.neurons):
            if(activations != None):
                # If the activation value is set, it means that it's an output layer
                deltas.append(neuron.calculate_output_delta(superior_error[idx],activations[idx]))
            else:
                if(idx != 0):
                    w_aux = []
                    for w in superior_weights:
                        w_aux.append(w[idx])
                    deltas.append(neuron.calculate_delta(superior_error,w_aux))
        return deltas

    def update_neurons(self,deltas,activations,isOutput):
        for (idx,neuron) in enumerate(self.neurons):
            if(idx == 0 and not isOutput):
                continue
            if isOutput:
                neuron.update_w(deltas[idx],activations)
            else:
                neuron.update_w(deltas[idx-1],activations)


class Properties:
    beta = 0
    def __init__(self,perceptron:Perceptron,training_set,output_set,normalized_function):
        self.perceptron = perceptron
        self.training_set = training_set
        self.output_set = output_set
        self.normalized_function = normalized_function
        self.output_max = 0
        self.output_min = 0
        self.sigmoid_max = 0
        self.sigmoid_min = 0


class Observables:
    def __init__(self,w,error,epochs,predictions=None):
        self.w = w
        self.error = error
        self.epochs = epochs
        self.predictions = predictions