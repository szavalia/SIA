import numpy as np

class Properties:
    beta = 0
    def __init__(self,neurons_per_layer,font,learning_rate,epochs,training_set,output_set):
        self.neurons_per_layer = neurons_per_layer
        self.font = font
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.training_set = training_set
        self.output_set = output_set
    
class Autoencoder:
    def __init__(self,weights,latent_index,training_set,output_set,neurons_per_layer):
        self.weights = weights
        self.latent_index = latent_index
        self.training_set = training_set
        self.output_set = output_set
        self.neurons_per_layer = neurons_per_layer
        self.functions = []
        for i in range(0,len(weights)):
            if i < latent_index:
                self.functions.append(self.linear)
            elif i == latent_index:
                self.functions.append(self.relu)
            else:
                self.functions.append(self.logistic)
        
    def relu(self,x):
        ret = []
        
        for value in x:
            ret.append(value)
            if(value <= 0):
                ret[-1] = 0
        
        return np.array(ret)
    
    def logistic(self, x):
        
        try:
            result = 1 / (1 + np.exp(-Properties.beta * x))
        except OverflowError:
            result = 1
        return result

    def linear(self,x):
        return x

    def get_output(self, input, weights):
        for (i,layer) in enumerate(weights):
            h = np.dot(layer, input)
            # Transform dot products into activations
            input = self.functions[i](h)
            #print(input)
        
        # Return results of last layer (network outputs)
        return input


    def error(self, weights):
        # print("Step: " + str(step))
        error = 0
        unflattened_weights = self.unflatten_weights(weights)
        for (i,entry) in enumerate(self.training_set):
            expected = np.array(self.output_set[i])
            output = np.array(self.get_output(entry, unflattened_weights))

            for (idx,output_value) in enumerate(output):
                error += (output_value - expected[idx])**2
                      
        #print("Error: " + str(error))
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
        self.weights = new_arr
        #print("After unflatten: " + str(self.weights))
        return new_arr
