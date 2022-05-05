import sys
import numpy as np
import random
from models import Observables, Properties,Perceptron,Neuron,Layer,ThresholdNeuron

def execute(properties:Properties):
    
    (perceptron, layers) = build_perceptron(properties)
    # Add threshold to training set
    training_set = np.insert(properties.training_set, 0, -1, axis=1)


    error = sys.maxsize
    min_error = sys.maxsize
    min_w = []
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

def build_perceptron(properties:Properties, test_w=None):
    
    perceptron:Perceptron = properties.perceptron
    BIAS = -1
    Neuron.function = perceptron.function
    Neuron.d_function = perceptron.d_function
    layers = []

   

    hidden_neuron_count = 0
    # Add hidden layer layers
    for layer_index, neurons_count in enumerate(perceptron.neurons_per_layer):  
        neurons = [ThresholdNeuron()]
        for index in range(0, neurons_count):
            if test_w is None:
                if (layer_index == 0):
                    # First layer uses length of entry value plus the bias
                    w = np.random.randn(len(properties.training_set[0])+1)
                else:
                    w = np.random.randn(len(layers[layer_index-1].neurons))
                w[0] = BIAS

            else:
                w = test_w[layer_index][index]
                hidden_neuron_count += 1

            neurons.append(Neuron(w,perceptron.learning_rate))
        layers.append(Layer(neurons))

    # Add output layer
    # Number of neurons in output layer depends on number of camps in expected output values
    neurons = []
    for i in range(len(properties.output_set[0])):
        if test_w is None:
            w = np.random.randn(len(layers[-1].neurons))
            w[0] = BIAS

        else:
            w = test_w[-1][i]

        neurons.append(Neuron(w, perceptron.learning_rate))
    layers.append(Layer(neurons))

    return (perceptron, layers)

def get_results(properties:Properties, w):
    (perceptron, layers) = build_perceptron(properties, w)
    results = []
    input_set = np.insert(properties.training_set,0,1,axis=1)
        
    activations = []
    results = []

    # Calculate activations (and save them)
    for entry in input_set:
        activations.append(entry)
        for (idx, layer) in enumerate(layers):
            activations.append(layer.get_activations(activations[idx]))
            
            if layer == layers[-1]: # I'm in the outer layer
                results.append(activations[-1])
                activations.clear()
    
    return results

def test(properties:Properties, w, metrics_function):

    results = get_results(properties, w)

    metrics = metrics_function(properties.output_set, results, properties.perceptron.problem)

    return metrics

def cross_validate(properties:Properties, TEST_PROPORTION):
    execute(properties)
    # Split input into chunks
    # ATTENTION! This product should be an integer in order not to lose entries
    segment_members = int(len(properties.training_set)*TEST_PROPORTION)
    segment_count = int(1/TEST_PROPORTION)
    sets = np.array_split(properties.training_set, segment_count)

    max_accuracy = -1
    best_run = None
    original_input = properties.training_set.copy()
    original_output = properties.output_set.copy()
    
    for k in range(0, segment_count-1):
        # Build datasets by splitting into testing and training segments
        test_set = sets[k]
        test_output_set = properties.output_set[k*segment_members:(k+1)*segment_members]
        training_set = []
        training_output_set = []
        for i in range(0, segment_members*segment_count):
            if not (i >= k*segment_members and i < (k+1)*segment_members):
                training_set.append(properties.training_set[i])
                training_output_set.append(properties.output_set[i])  
        
        # Train the neural network
        properties.training_set = training_set
        properties.output_set = training_output_set
        observables = execute(properties)
        

        # Test the neural network
        properties.training_set = test_set
        properties.output_set = test_output_set
        observables.metrics = test(properties, observables.w, properties.metrics_function)

        # Update best run
        if observables.metrics[0].accuracy > max_accuracy:
            max_accuracy = observables.metrics[0].accuracy
            best_run = observables
        
        # Reset data
        properties.training_set = original_input
        properties.output_set = original_output

    return best_run
