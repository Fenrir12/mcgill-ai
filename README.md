# mcgill-ai
This repository contains the code I developed during the introductory course of artificial intelligence at MCGill university

# Multilayer Perceptron

Last version of MLP contains a class for building and running a complete custom artificial neural. Works by pairing it with numtofeature script which has the methods for encoding MNIST digits onto a one hot vector for neural network inputs.

# Run it now

Simply import and call MLP class into your program and define the structure of your network into the parameters of the network.
For instance, [784, 135, 10] specifies a neural network with an input layer of 784 neurons, one hidden layer of 135 neurons and an output layer of 10 neurons. You can put as many hidden layers with custom number of neurons as you want like so : 
[I, H1, H2, H3, ..., Hn, O].

This custom implementation contains many parmeters to tweak performances of  the network and add capacities. At its core, the network is initialized with following capacities :
- Learning Rate = 0.1, 
- Batch Size = 10,  
- Number of epochs for learning = 10,
- Activation function of hidden layers  = 'sigmoid',
- Activation function of output layers='sigmoid', 
- Cost function used for gradient descent='Squared euclidean distance',
- Regularization method for learning ='dropout', 
- Dropout rate = 0.2, 
- Momentum = 1

Class definition:
 '''Initializes weight matrices with respect to specified number of neurons
        for input, hidden and output layer. Also specifies the number of hidden layer
        of the network. Provides accessibility to the insides of the network with
        object variables of weights (W), activations(A), errors(E)
        and partial derivatives of errors (D)
        lyrNodes: list of ints specifying number of Nodes(neurons), in each layer
                    order of [layer input, hidden0,hidden1...hiddenN,Output]
        lrnRate = learning rate, alpha, for weight updates in backprops
        batch_size = number of training examples into each batch
        
        n_epochs = number of training iterations to use with backprop
        costFunc : 'xentropy' or 'sqrdEuc'    
        outputActv : 'softmax' or 'softplus' or 'sigmoid'
        hiddenActv : 'softmax' or 'softplus' or 'sigmoid'
        regMethd : 'weightedDst' or 'dropout'
        regParam : regularization parameter used for weighted distance, if using dropout
                    set to zero can be any int, but higher number may degrade accuracy
        dropPrtn : portion of neurons in hidden layer to dropout for regularization. 
                    Not used in weightedDist, must be a decimal recomended .1=.5 
        momentum : momentum factor to change learning rate in back prop
                    based on magnitude of last error.  If don't want to use set
                    to zero. Any int.
