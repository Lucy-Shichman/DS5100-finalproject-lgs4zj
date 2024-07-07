import numpy as np
import pandas as pd

class Die():
    """
    This class creates a Die object, changes it's weight, 
    rolls it, and returns it's current state.
    """
    def __init__(self, faces):
        """
        Initializes faces and weight attributes of die object.
        
        Takes a "faces" input argument that must be a NumPy array
        of distinct values (array's data type may by a string, integer, 
        or float).
        
        Internally initializes the weights to 1.0 for each face. 
        """  
        if type(faces) != np.ndarray:
            raise TypeError("Faces input must be a NumPy array")
        
        if len(faces) != len(np.unique(faces)):
            raise ValueError("Array values must be distinct")
        
        self.faces = faces
        self.weights = [1 for i in faces]
        self.__die = pd.DataFrame({
            'weights' : self.weights
        }).set_index(self.faces)
    
    def change_weight(self, face_value, new_weight):
        """
        Changes the weight of a single face of the die object.
        
        Takes two input arguments: the face value (string or numeric) 
        to be changed and the new weight (integer or float)
        """
        if face_value not in self.faces:
            raise IndexError("face_value input is not a valid value")
        
        try:
            float(new_weight)
        except:
            raise TypeError("new_weight input is not a valid type")
        
        self.__die.loc[face_value] = new_weight
    
    def roll_die(self, num_rolls=1):
        """
        Rolls the die object one or more times.
        
        Takes one input argument, num_rolls (integer), which specifies
        the number of times the die object is rolled. Defaults to 1.
        
        Returns a list of subsequent outcomes.
        """
        outcomes = []
        for i in range(num_rolls):
            outcome = self.__die.sample(weights=self.__die.weights).index[0]
            outcomes.append(outcome)
        return outcomes
    
    def current_state(self):
        """
        Shows the die object's current state.
        
        Returns a data frame of the object's faces and weights.
        """
        return self.__die

class Game(Die):
    """
    This class creates a game object. A game consists of rolling one 
    or more similar dice (Die objects) one or more times.
    """
    def __init__(self, die_list):
        """
        Initializes list of die objects.
        
        Takes argument die_list (Die class objects) of already
        instantiated similar dice.
        """
        self.die_list = die_list
    
    def play_game(self,game_rolls):
        """
        Rolls all dice a specified number of times.
        
        Takes argument game_rolls (integer) to specify how many times
        the die should be rolled.
        
        Results are saved to a private dataframe.
        """
        outcomes = []
        for die in self.die_list:
            outcome = die.roll_die(game_rolls)
            outcomes.append(outcome)
            
        self.__outcome_df = pd.DataFrame(outcomes,
                                      columns = ("Roll " + str(i+1) for i in range(0, game_rolls)),
                                      index = ("Die " + str(i+1) for i in range(len(self.die_list)))).T
    
    def game_results(self, form="wide"):
        """
        Returns game results data frame in a specified format.
        
        Takes argument form ("wide" or "narrow") that specifies the
        format of the returned data frame. Defaults to wide format.
        """
        if form.lower() != "wide" and form.lower() != "narrow":
            raise ValueError("form input must be 'wide' or 'narrow'")
        
        if form.lower() == "wide":
            return self.__outcome_df
        
        if form.lower() == "narrow":
            narrow_df = self.__outcome_df.reset_index().melt(id_vars='index',
                                                             var_name='Die Number',
                                                             value_name='Outcome')
            narrow_df = narrow_df.set_index(['index','Die Number']).sort_index()
            return narrow_df
    
    def game_results(self, form="wide"):
        """
        method to return game results in specified format
        """
        if form.lower() != "wide" and form.lower() != "narrow":
            raise ValueError("form input must be 'wide' or 'narrow'")
        
        if form.lower() == "wide":
            return self.__outcome_df
        
        if form.lower() == "narrow":
            narrow_df = self.__outcome_df.reset_index().melt(id_vars='index',
                                                             var_name='Die Number',
                                                             value_name='Outcome')
            narrow_df = narrow_df.set_index(['index','Die Number']).sort_index()
            return narrow_df

class Analyzer(Game):
    """
    This class creates an analyzer object which takes the 
    results of a single game and computes various descriptive
    statistical properties about it.
    """
    def __init__(self, game_object):
        """
        Initializes an Analyzer object.
        
        Takes argument game_object (Game class object).
        
        Initializes a game_object attribute to store the Game object
        and a outcomes attribute to store the Game object's results.
        """
        if not isinstance(game_object, Game):
            raise ValueError("game_object input must be a Game object")
        
        self.game_object = game_object
        self.outcomes = game_object.game_results()
        
    def jackpot(self):
        """
        Computes how many times the game resulted in a jackpot
        (a result in which all faces are the same).
        
        Returns the number of jackpots as an integer.
        """
        num_jackpots = self.outcomes.apply(lambda x: len(x.unique()) == 1, axis = 1).sum()
        
        return num_jackpots
    
    def face_counts(self):
        """
        Computes how many times a given face is rolled in each event.
        
        Returns a wide format data frame of the results.
        """
        face_counts_df = self.outcomes.apply(lambda x: x.value_counts(), axis = 1).fillna(0)
        
        face_counts_df.index = ["Roll " + str(i+1) for i in range(0, len(face_counts_df))]
        face_counts_df.columns = face_counts_df.columns.sort_values()
        
        return face_counts_df
    
    def combo_count(self):
        """
        Computes the distinct combinations (order independent) of faces rolled, 
        along with their counts.
        
        Returns a multi-indexed data frame of the distinct combinations and
        their associated counts.
        """
        combo_df = self.outcomes.apply(lambda x: x.sort_values(), axis=1, result_type = "broadcast")
        combo_df = combo_df.groupby([i for i in combo_df.columns]).size().reset_index(name = "count")
        combo_df = combo_df.set_index([i for i in combo_df.columns])#.sort_values(["Count"], ascending=False)
        
        return combo_df
        
    def perm_count(self):
        """
        Computes the distinct permutations (order dependent) of faces rolled, 
        along with their counts.
        
        Returns a multi-indexed data frame of the distinct combination and 
        their associated counts.
        """
        perm_df = self.outcomes.groupby([i for i in self.outcomes.columns]).size().reset_index(name = "count")
        perm_df = perm_df.set_index([i for i in self.outcomes.columns])#.sort_values(["Count"], ascending=False)
        
        return perm_df
 

