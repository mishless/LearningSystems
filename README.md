# Laboratory work for Learning Systems
Laboratory work for Learning Systems course at MDH during spring semester 2015/2016
### Assignment 1
-----
Reactive-Ion-Etching (RIE) machines are used in some company for removal of thin layers in the production of magnetic heads. The task of a RIE machine is to etch a specified surface of some mm depth into sliders. The etch depths of sliders are regarded as indicators for process stability. It would be easy to control the process if the etch depth could be monitored online. Unfortunately such a depth can only be measured at the end of the etching process. 

In order to enhance process stability and reliability, attempts have been made to analyse data from process observations and to detect correlation between sensor data and process result, i.e. etch depth. At present, however, there is no explicit mathematical model to calculate etch depth from process parameters. As alternative artificial neural network may be constructed to predict etch depth based on sensor information.

The 21 features extracted from sensor signals are illustrated in the table below. But not all of them are relevant for the underlying problem. A pre-step of feature selection has been performed to select the most critical features as inputs. The results of feature selection recommend that features 2, 19, and 20 be selected for etch process modelling (selected features are in bold text in the table).

  
| Number | Features extracted | Original signals|
| ------------- |:-------------:| -----:|
| 1 | Run time | |
| **2** | **HF energy (integral of HF power)** | **HF power delivered** |
| 3 | Start time | Start time |
| 4 | Peak to peak value | HF power delivered |
| 5 | Integral | DC voltage |
| 6 | Start time | DC voltage |
| 7 | Integral | Gas flow 1 |
| 8 | Mean value | Gas flow 1 |
| 9 | Standard deviation | Gas flow 1 |
| 10 | Integral | Gas flow 2 |
| 11 | Mean value | Gas flow 2 |
| 12 | Standard deviation | Gas flow 2 |
| 13 | Integral | Gas flow 3 |
| 14 | Mean value | Gas flow 3 |
| 15 | Standard deviation | Gas flow 3 |
| 16 | Integral | Chamber pressure |
| 17 | Mean value | Chamber pressure |
| 18 | Peak to peak value | Chamber pressure |
| **19** | **Integral** | **Throttle position** |
| **20** | **Mean value** | **Throttle position** |
| 21 | Peak to peak value | Throttle position |


Two data sets are available to be downloaded in a1 forlder - Data_Training and Data_Test. Data_Training contains the examples that are available for learning, while Data_Test includes test examples that represent unseen examples and are not involved in the learning procedure. Every case in both data sets consists of 21 features listed in the above table  and the associated etch depth as output. The first 21 columns in the files represent the 21 features and the last column represents the output.

The task is to develop a competent neural network to predict etch depth based on Data_Training. Then you should examine the performance of the learned neural network on Data_Test. Only the three features selected need to be used as inputs to the neural network (you just use the results of feature selection here). As learning algorithm you can use GA or BP as your free choice.

#### Results
1. STtructure of the ANN
The structure of the neural network is configurable by the user, but for the results presented below we used three-layer ANN with 3 inputs, 5 hidden units and 1 output.
2. Learning algorithm used
The algorithm used for learning is backpropagation – basically it is iterative algorithm and on each iteration the inputs are forwarded though the network and the outputs are calculated. Then the error of each output is calculated and weights are modified. The first iteration uses random small weights. 
3. Performance
![alt text](https://github.com/mishless/LearningSystems/blob/master/a1/ann.png "ANN Perfomance")

On the vertical axis is the error and on the horizontal axis there is the number of iterations that have passed. 
4. Performance on training data
Error on whole training data set: 0.00591729466547751
5. Performance on test data
Test data error is 0.004609162462734982

