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
1. Structure of the ANN

   The structure of the neural network is configurable by the user, but for the results presented below we used three-layer ANN with     3 ⋅inputs, 5 hidden units and 1 output.
2. Learning algorithm used

   The algorithm used for learning is backpropagation – basically it is iterative algorithm and on each iteration the inputs are     forwarded though the network and the outputs are calculated. Then the error of each output is calculated and weights are modified. The first iteration uses random small weights. 
3. Performance
   ![alt text](https://github.com/mishless/LearningSystems/blob/master/a1/ann.png "ANN Perfomance")

   On the vertical axis is the error and on the horizontal axis there is the number of iterations that have passed. 
4. Performance on training data

   Error on whole training data set: 0.00591729466547751
5. Performance on test data

   Test data error is 0.004609162462734982

### Assignment 2
---
Classification of Irsi data is a well known benchmark problem in machine learning research. This data set is downloadable from a2 folder. The assignment is to implement this fuzzy classifier in a computer program that has to be applied to classify all the iris data and examine the classification accuracy of your fuzzy system.

#### Results

1. What is the AND operator in your implementation?

   In our solution we allow the user to specify which operator should be used in calculations when intersection between fuzzy sets      occurs. The possible values are two – min or prod. The “min” option means that the built-in function for minimum will be used and     the “prod” option means that “product” implementation will be used – which is in fact multiplication.
2. What is the OR operator in your implementation? 

   In our solution we allow the user to specify which operator should be used in calculations when union between fuzzy sets occurs.      The possible values are two – max or probor. The “max” option means that the built-in function for maximum will be used and the       “probor” option means that “probability or” implementation will be used.
3. What is the data flow from inputs to decision given the normalized attribute values as (0.3, 0.8, 0.2, 0.7)? 

   |0.3|0.5|0.8|
   |---|---|---|
   |μ_short(0.3)=0.5|μ_short(0.8)=0|μ_short(0.2)=0.67|μ_short(0.7)=0|
   |μ_middle(0.3)=0.5|μ_middle(0.8)=0.5|μ_middle(0.2)=0.33|μ_middle(0.7)=0.75|
   |μ_long(0.3)=0|μ_long(0.8)=0.5|μ_long(0.2)=0|μ_long(0.7)=0.25|

   Rule #1: min(max(0.5, 0.5), max(0.5, 0.5), max(0.33, 0), 0.65) = min(0.5, 0.5, 0.33, 0.75) = 0.33

   Rule #2: min(max(0.67, 0.33), 0) = 0

   Rule #3: min(max(0, 0.5), 0, 0.25) = 0

   Rule #4: min(0.5, max(0, 0.5), 0.67, 0.25) = 0.25

   The example is classified as iris setosa.
4. What is the accuracy of your implemented fuzzy classifier on the Iris data?

   ~ 78% using min/max
   ~ 69% using prod/probor
  
### Assignment 3
------
The	Travelling	Salesman	Problem	(TSP)	is	one	of	the	most well	know	optimization	problems. This problem originally	is	described	as	follows: Given	a	list	of	cities	and	the	distance between	each	other,	which	is	the	shortest route	to	travel	across	 all	the	cities?,	such	that,	you	visit	all	the	cities	once	and	you	start	and	finish	in	the	same	city. We	now	consider	the	problem	with	a	set	of locations inside a	city available at a3 folder.	These locations are	represented	by two	coordinates	(x and	y) as	illustrated	in	the	table	below.

| Location ID | X | Y |
|---|---|---|
| 1 | 565 | 575 |
| 2 | 25 | 185 |
| 3 | 345 | 750 |
| ... | ... | ... |

The	distance	between	two	locations is	the	Euclidean	Distance.
The	assignment	is	to	apply an	optimization	algorithm,	e.g.	Genetic	Algorithm	(GA)	to	search	for	the	shortest	route.	You	need	to	visit	all	the	locations	once	and	the	starting	and	end	points must	be the	location	number	1.

#### Results

1. Explain the important operations of the employed algorithm (e.g. GA) to solve this problem:

   One of the most important decisions that need to be made when using GA is the representations of individual because the success of    the algorithm depends on this. Fortunately, for the problem we are solving this is quite intuitive and is described in details        below. Another aspect that is of great importance is the definition of the fitness function which is also intuitive in our case. GA    manages to solve the problem because of its evolutionary approach - an initial population of individuals is generated randomly and    is evaluated. After that few of the best individual (fittest) are transferred to the next population. Using a selection mechanism     few of the rest individual are chosen to be parent and to crossover between each other to create the rest of the next population.     After that mutation operator is executed that mutates the children and brings diversity to the population. This prevents the          algorithm from getting into a local minimum or over-fit. Eventually after the error has become small or after a maximum number of     iterations have passed the algorithm terminates and gives the best solution found so far.
   
2. Explain the representation of the individual solutions in your algorithm.

   The individual is represented as an array containing the IDs of the cities that will be visited. In index 0 is the ID of the city     that will be visited first and is always equal to 1. In index 1 is the seconds city, in index 2 is the third city, etc. and the       last index in the array is the city where we will finish, which is always equal to 1.
   
3. Give the parameters used in your algorithm. Examples: population size, crossover rate...

   The population size that we used is 500. The elitism rate is 0.1 which means that 10% of the best individuals will be inherited in the next generation without any change. The tournament rate is 0.1 which means that whenever a parent is to be chosen 10% of the population will be chosen randomly and the parent will be the fittest one, according to the formula above. The  parent rate is 0.2 which 
   
4. Performance
   ![alt text](https://github.com/mishless/LearningSystems/blob/master/a3/ga.png "GA Perfomance")

5. Best results obtained

   Best result is 8228.576874458458 with path 1 - 18 - 3 - 17 - 21 - 42 - 7 - 2 - 30 - 29 - 16 - 46 - 35 - 49 - 32 - 45 - 19 - 41 - 8 - 9 - 10 - 43 - 33 - 51 - 28 - 27 - 26 - 47 - 13 - 14 - 52 - 11 - 12 - 25 - 4 - 15 - 5 - 6 - 48 - 24 - 38 - 37 - 40 - 39 - 36 - 34 - 44 - 50 - 20 - 23 - 31 - 22 - 1
   
### Assignment 4
-----
Given  is a map of 26 cities (named as A, B, C, D,..., X, Y, Z respectively). The document for this map is available in a4 folder. Every road connection is represented by a row in the table below, where the first and the second columns correspond to the two cities that are directly connected and the third column denotes the distance of the road that connect the two cities.

| From | To | Distance |
|----|----|----|
| A |	B |	2 |
| A |	E	| 2 |
| A |	W	| 1 |
| ... | ... | ... |

The assignment is to write a computer program based on the principle of dynamic programming to realize the following two functions:
1)	Calculate the optimal values of all cities given that the destination is city F using the Bellman equation
2)	Find the shortest path from each city to F using the optimal values

#### Results
TODO
