import numpy as np
import math
import scipy.optimize as sco

class Properties:
    beta = 0
    def __init__(self,neurons_per_layer,font,font_chars,epochs,training_set,output_set,mode,noise_prob):
        self.neurons_per_layer = neurons_per_layer
        self.font = font
        self.font_chars = font_chars
        self.epochs = epochs
        self.training_set = training_set
        self.output_set = output_set
        self.mode = mode
        self.noise_prob = noise_prob

class Observables:
    def __init__(self,errors_per_step,latent_outputs):
        self.errors_per_step = errors_per_step
        self.latent_outputs = latent_outputs
    
class Autoencoder:
    def __init__(self,weights,latent_index,training_set,output_set,neurons_per_layer):
        self.weights = weights
        self.latent_index = latent_index
        self.training_set = training_set
        self.output_set = output_set
        self.neurons_per_layer = neurons_per_layer
        self.curr_epoch = 0
        self.functions = []
        self.set_functions()
        self.errors_per_step = []
    
    def set_functions(self):
        for i in range(0,len(self.weights)):
            if i < self.latent_index:
                self.functions.append(self.linear)
            elif i == self.latent_index:
                self.functions.append(self.relu)
            else:
                self.functions.append(self.logistic)

    def callback(self,x):
        self.errors_per_step.append(self.error(x))
        self.curr_epoch += 1
        print("Epoch: {1}. Error: {0}".format(self.errors_per_step[-1], self.curr_epoch))

    def relu(self,x):
        return np.where(x <= 0, 0, x)
    
    def logistic(self,x):
        ret = []
        for value in x:
            try:
                ret.append(1 / (1 + math.exp(-2 * Properties.beta * value)))
            except:
                ret.append(1)
        return np.array(ret)

    def linear(self,x):
        return x

    def get_output(self, input, weights):
        for (i,layer) in enumerate(weights):
            h = np.dot(layer, input)
            # Transform dot products into activations
            input = self.functions[i](h)
        
        # Return results of last layer (network outputs)
        return input

    def get_latent_output(self,input):
        for(i,layer) in enumerate(self.weights[:self.latent_index+1]):
            h = np.dot(layer, input)

            # Transform dot products into activations
            input = self.functions[i](h)
        
        # Return results of latent layer
        return input

    def error(self, weights):
        error = 0
        unflattened_weights = self.unflatten_weights(weights)
        for (i,entry) in enumerate(self.training_set):
            expected = np.array(self.output_set[i])
            output = np.array(self.get_output(entry, unflattened_weights))

            for (idx,output_value) in enumerate(output):
                error += (output_value - expected[idx])**2
                      
        return error*(1/2)


    # For DAE where we need to pass new noised data
    def error_given_sets(self, weights, input_set):
        error = 0
        unflattened_weights = self.unflatten_weights(weights)
        for (i,entry) in enumerate(input_set):
            expected = np.array(self.output_set[i])
            output = np.array(self.get_output(entry, unflattened_weights))

            for (idx,output_value) in enumerate(output):
                error += (output_value - expected[idx])**2
                      
        return error*(1/2)

    # Converts from 1D array back to 3D structure
    def unflatten_weights(self, array):
        new_arr = []
        i = 0
        for layer in self.weights:
            curr_size = layer.size
            flatted = np.array(array[i:i+curr_size])
            new_arr.append(flatted.reshape(layer.shape))
            i += curr_size
        new_arr = np.array(new_arr, dtype=object)
        #self.weights = new_arr
        return new_arr
