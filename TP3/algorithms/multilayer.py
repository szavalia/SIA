import sys
import numpy as np
import random
from models import Observables, Properties,Perceptron,Neuron,Layer,ThresholdNeuron

def execute(properties:Properties):
    
    perceptron:Perceptron = properties.perceptron
    BIAS = -1
    Neuron.function = perceptron.function
    Neuron.d_function = perceptron.d_function

    # Add threshold to training set
    training_set = np.insert(properties.training_set, 0, -1, axis=1)

    layers = []

    # Add hidden layer layers
    for idx, neurons_count in enumerate(perceptron.neurons_per_layer):  
        neurons = [ThresholdNeuron()]
        for index in range(0, neurons_count):
            if (idx == 0):
                # First layer uses length of entry value
                w = np.random.randn(len(training_set[0]))
            else:
                w = np.random.randn(len(layers[idx-1].neurons))
            w[0] = BIAS
            neurons.append(Neuron(w,perceptron.learning_rate))
        layers.append(Layer(neurons))

    # Add output layer
    # Number of neurons in output layer depends on number of camps in expected output values
    neurons = []
    for i in range(len(properties.output_set[0])):
        w = np.random.randn(len(layers[-1].neurons))
        w[0] = BIAS
        neurons.append(Neuron(w, perceptron.learning_rate))
    layers.append(Layer(neurons))

    error = sys.maxsize
    min_error = sys.maxsize
    min_w = w
    i = len(training_set)
    pos = 0
    epochs = -1
    indexes = []
    while error > perceptron.min_error and epochs < perceptron.max_epochs:

        # Always pick at random or random until covered whole training set and then random again?
        if(i == len(training_set)):
            epochs+=1
            indexes = random.sample(list(range(len(training_set))),len(list(range(len(training_set)))))
            i = 0
        
        pos = indexes[i]
        entry = training_set[pos]
        
        activations = []
        activations.append(entry)
        
        # Calculate activations (and save them)
        for (idx, layer) in enumerate(layers):
            activations.append(layer.get_activations(activations[idx]))
        
        deltas = []
        # Calculate error in output and one below output
        deltas.append(layer.get_deltas(properties.output_set[pos%(len(training_set))],None, activations[-1]))
        deltas.insert(0, layers[-2].get_deltas(deltas[0],layers[-1], None, True))

        # Calculate deltas (and save them)
        for (idx, layer) in reversed(list(enumerate(layers[:-2]))):
            deltas.insert(0, layer.get_deltas(deltas[0],layers[idx+1]))
        
        # Update all ws (incremental)
        for(idx,layer) in enumerate(layers):
            isOutput = (idx == len(layers) -1)
            layer.update_neurons(deltas[idx],activations[idx],isOutput)
        
        # Calculate error
        error = calculate_error(training_set, properties.output_set, layers)
        i+=1
        if error < min_error:
            min_error = error
            min_w = []
            for (idx,layer) in enumerate(layers):
                min_w.append([])
                if(idx == len(layers)-1):
                    for neuron in layer.neurons:
                        min_w[-1].append(neuron.w.copy())
                else:
                    for neuron in layer.neurons[1:]:
                        min_w[-1].append(neuron.w.copy())

    return Observables(min_w, min_error,epochs)


def calculate_error(training_set, output_set, layers):
    error = 0
    for (i,entry) in enumerate(training_set):
        activations = []
        activations.append(entry)
        for (j, layer) in enumerate(layers):
            activations.append(layer.get_activations(activations[j]))
        for (idx,output_value) in enumerate(output_set[i]):
            error += (output_value - activations[-1][idx])**2
    return error*(1/2)
        