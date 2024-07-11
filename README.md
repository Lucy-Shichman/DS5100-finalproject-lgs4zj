# Monte Carlo Simulator
Lucy Shichman \
DS5100 Final Project
## Synopsis
Install the montecarlo package. Do something like this:
```
pip install .
```
Import the three classes:
```
from montecarlo.montecarlo import Die, Game, Analyzer
```
Import Pandas and NumPy:
```
import pandas as pd
import numpy as np
```
Generate dice by passing an array of faces to the Die class:
```
die1 = Die(np.array(['1','2','3','4','5','6']))
die2 = Die(np.array(['1','2','3','4','5','6']))
```
To execute a game, first create a Game class object by passing a list of similar Die objects. Use the play_game() method to run a game:
```
game1 = Game([die1, die2])
```
```
game1.play_game(1000)
```
Create an Analyzer object from the Game object, and use the jackpot(), face_counts(), combo_count(), and perm_count() methods to analyze the results of the game:
```
analyzer1 = Analyzer(game1)
```
```
# analyze number of jackpots in game1
analyzer1.jackpot()
```
## API description
### <ins>Die class:</ins> 
This class creates a Die object, changes it's weight, rolls it, and returns it's current state.
#### \_\_init__(self, faces): 
* Initializes faces and weight attributes of die object.
* Takes a "faces" input argument that must be a NumPy array of distinct values (array's data type may by a string, integer, or float).
* Internally initializes the weights to 1.0 for each face. 
#### change_weight(self, face_value, new_weight):
* Changes the weight of a single face of the die object.
* Takes two input arguments: the face value (string, integer, or float) to be changed and the new weight (integer or float)
#### roll_die(self, num_rolls=1):
* Rolls the die object one or more times.
* Takes one input argument, num_rolls (integer), which specifies the number of times the die object is rolled. Defaults to 1.
* Returns a list of subsequent outcomes.
#### current_state(self):
* Shows the die object's current state.
* Returns a data frame of the object's faces and weights.
### <ins>Game class:</ins>
This class creates a game object. A game consists of rolling one or more similar dice (Die objects) one or more times.
#### \_\_init__(self, die_list):
* Initializes list of die objects.
* Takes argument die_list (list of Die class objects) of already instantiated similar dice.
#### play_game(self,game_rolls):
* Rolls all dice a specified number of times.
* Takes argument game_rolls (integer) to specify how many times the die should be rolled.
#### game_results(self, form="wide"):
* Returns game results data frame in a specified format.
* Takes argument form (string, "wide" or "narrow") that specifies the format of the returned data frame. Defaults to wide format.
### <ins>Analyzer class:</ins>
This class creates an analyzer object which takes the results of a single game and computes various descriptive statistical properties about it.
#### \_\_init__(self, game_object):
* Initializes an Analyzer object.
* Takes argument game_object (Game class object), an already instantiated game.
* Initializes a game_object attribute to store the Game object and a outcomes attribute to store the Game object's results.
#### jackpot(self):
* Computes how many times the game resulted in a jackpot(a result in which all faces are the same).
* Returns the number of jackpots as an integer.
#### face_counts(self):
* Computes how many times a given face is rolled in each event.
* Returns a wide format data frame of the results.
#### combo_counts(self):
* Computes the distinct combinations (order independent) of faces rolled, along with their counts.
* Returns a multi-indexed data frame of the distinct combinations and their associated counts.
#### perm_counts(self):
* Computes the distinct permutations (order dependent) of faces rolled, along with their counts.
* Returns a multi-indexed data frame of the distinct combination and their associated counts.
