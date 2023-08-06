#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


class Multi_Layer_NN:
    """
    A Neural Network that can be either trained on data, 
    or initialized with existing weights.
    
    Parameters
    ----------
    dimensions: dict, a dictionary containing the weight matrices and bias vectors.
    E.g. dimensions = {"W1": [[1, 0.5, 2],[0.25,0.75,1.5]], "b1":[1,2,1]} initializes a one 
    layer perceptron that takes three input elements and has two nodes.
    """
    
    def __init__(self, parameters={}):
        self.parameters = parameters #neural network parameters
    
    
    def init_params(self, hidden_dims, eps=0.01):
        """
        Initializes the weight matrices and bias vectors with appropriate dimensions with 
        random numbers in the intervall [-eps, +eps].
        
        Parameters
        ----------
        hidden_dims: list, contains the dimensions (number of nodes) for each layer.
        E.g. init_params([1,2,1])
        """
        
        #random parameter initialization
        for i in range(1, len(hidden_dims)):
            self.parameters["W" + str(i)] = np.random.randn(hidden_dims[i], hidden_dims[i-1]) * eps
            self.parameters["b" + str(i)] = np.random.randn(hidden_dims[i], 1) * eps

            
                                                            
    def forward_prop(self, A, W, b):
        """ Performs linear forward propagation (without activation function)"""
        Z = np.dot(W, A) + b
        cache = (A, W, b)
        
        return Z, cache
    
    
    def sigmoid(self, Z):
        """
        Sigmoid activation function
        returns the output of the sigmoid function and the input aswell (needed for backpropagation)
        """
    
        A = 1/(1 + np.exp(-Z))
        cache = Z
        
        return A, cache
    
    
    def relu(self, Z):
        """
        ReLu activation function
        returns output of the ReLu function and the input aswell (needed for backpropagation)
        """
        
        A = np.maximum(0, Z)
        cache = Z
        
        return A, cache
    
    
    def sigmoid_backward(self, dA, cache):
        """backward propagation for the sigmoid activation function"""
        Z = cache
        dZ = dA * self.sigmoid(Z)[0] * (1 - self.sigmoid(Z)[0])
        
        return dZ
    
    
    def relu_backward(self, dA, cache):
        """backward propagation for the ReLu activation function"""
        Z = cache
        dZ = np.array(dA, copy = True)
        dZ[Z<=0] = 0
        
        return dZ
    
    
    def forward_prop_activation(self, A_prev, W, b, activation = "relu"):
        """Performs linear forward propagation (with activation function)"""
        
        if activation == "sigmoid":
            Z, linear_cache = self.forward_prop(A_prev, W, b)
            A, activation_cache = self.sigmoid(Z)
            cache = (linear_cache, activation_cache)
            
        elif activation == "relu":
            Z, linear_cache = self.forward_prop(A_prev, W, b)
            A, activation_cache = self.relu(Z)
            cache = (linear_cache, activation_cache)
        
        return A, cache
    
    
    def total_forward(self, X):
        """Forward propagation through the whole network"""
        caches = []
        A = X
        L = len(self.parameters)//2 #total number of layers
        
        for i in range(1, L):
            A_prev = A
            A, cache = self.forward_prop_activation(A_prev, self.parameters["W{:d}".format(i)], self.parameters["b{:d}".format(i)], activation = "relu")
            caches.append(cache)
            
        AL, cache = self.forward_prop_activation(A, self.parameters['W%d' % L], self.parameters['b%d' % L], activation = "sigmoid")
        caches.append(cache)
        
        return AL, caches
    
    
    def compute_cost(self, AL, Y):
        """total cost of the batch"""
        m = Y.shape[1]#number of samples in the batch
        cost = -1 / m * np.sum(Y * np.log(AL) + (1-Y) * np.log(1-AL))
        cost = np.squeeze(cost) 

        return cost
    
    
    def back_prop(self, dZ, cache):
        """back propagation without activation"""
        A_prev, W, b = cache
        m = A_prev.shape[1] #number of samples in the batch


        dW = 1 / m * np.dot(dZ, A_prev.T)
        db = 1 / m * np.sum(dZ, axis=1, keepdims=True)
        dA_prev = np.dot(W.T, dZ)

        return dA_prev, dW, db
    
    
    def back_prop_activation(self, dA, cache, activation):
        """back propagation with activation"""
        linear_cache, activation_cache = cache

        if activation == "relu":
            dZ = self.relu_backward(dA, activation_cache)
            dA_prev, dW, db = self.back_prop(dZ, linear_cache)


        elif activation == "sigmoid":
            dZ = self.sigmoid_backward(dA, activation_cache)
            dA_prev, dW, db = self.back_prop(dZ, linear_cache)

        return dA_prev, dW, db
    
    
    def total_backprop(self, AL, Y, caches):
        """back propagation through the entire neural network"""
        
        grads = {} #dictionary containing the gradient values for the parameters
        L = len(caches)
        m = AL.shape[1] #number of samples in the batch
        Y = Y.reshape(AL.shape)

        dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

        current_cache = caches[L-1]
        grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = self.back_prop_activation(dAL, current_cache, 'sigmoid')

        for l in reversed(range(L-1)):

            current_cache = caches[l]
            dA_prev_temp, dW_temp, db_temp = self.back_prop_activation(grads["dA" + str(l + 1)], current_cache, 'relu')
            grads["dA" + str(l)] = dA_prev_temp
            grads["dW" + str(l + 1)] = dW_temp
            grads["db" + str(l + 1)] = db_temp


        return grads
        
        
    def update_parameters(self, grads, learning_rate):
        """updates the parameters"""

        L = len(self.parameters) // 2 

        for l in range(0, L):
            self.parameters["W" + str(l+1)] = self.parameters["W" + str(l+1)] - learning_rate * grads["dW" + str(l+1)]
            self.parameters["b" + str(l+1)] = self.parameters["b" + str(l+1)] - learning_rate * grads["db" + str(l+1)]
        
        
        
    def train_model(self, X, Y, learning_rate = 0.0075, num_iterations = 1000, print_cost = False, plot = False):
        """Trains the model on the training data X and the labels Y"""
        
        costs = []                     

        # Loop (gradient descent)
        for i in range(0, num_iterations):

            # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
            AL, caches = self.total_forward(X)
            
            cost = self.compute_cost(AL, Y)
            grads = self.total_backprop(AL, Y, caches)
            self.update_parameters(grads, learning_rate)
            # Print the cost every 100th training example
            if print_cost and i % 100 == 0:
                print ("Cost after iteration %i: %f" %(i, cost))
            if print_cost and i % 100 == 0:
                costs.append(cost)

        if plot:
            plt.plot(np.squeeze(costs))
            plt.ylabel('cost')
            plt.xlabel('iterations (per tens)')
            plt.title("Learning rate =" + str(learning_rate))
            plt.show()


    def predict(self, X, Y, print_acc = False):
        """
        Predicts the outcome of feature vectors using the trained Neural Network model.

        Arguments:
        X: input feature vectors

        Returns:
        p: predictions for the given feature vectors
        """

        m = X.shape[1]
        n = len(self.parameters) // 2 # number of layers in the neural network
        p = np.zeros((1,m))

        # Forward propagation
        probas, caches = self.total_forward(X)


        # convert probas to 0/1 predictions
        for i in range(0, probas.shape[1]):
            if probas[0,i] > 0.5:
                p[0,i] = 1
            else:
                p[0,i] = 0

        if print_acc:
            print("Accuracy: "  + str(np.sum((p == Y)/m)))

        return p


# In[ ]:




