import numpy as np
import pandas as pd

class Die():
     """
     This class creates a Die object, changes it's weight, 
     rolls it, and returns it's current state.
     """
    def __init__(self, faces):
        """
        initializes faces, weights, and die attributes
        """  
        if type(faces) != np.ndarray:
            raise TypeError("Faces input must be a NumPy array")
        
        if len(faces) != len(np.unique(faces)):
            raise ValueError("Array values must be distinct")
        
        self.faces = faces
        self.weights = [1 for i in faces]
        self._die = pd.DataFrame({
            'weights' : self.weights
        }).set_index(self.faces)
    
    def change_weight(self, face_value, new_weight):
        """
        method to change the weight of a single side
        """
        if face_value not in self.faces:
            raise IndexError("face_value input is not a valid value")
        
        try:
            float(new_weight)
        except:
            raise TypeError("new_weight input is not a valid type")
        
        self._die.loc[face_value] = new_weight
    
    def roll_die(self, num_rolls=1):
        """
        method to roll the die one or more times
        """
        outcomes = []
        for i in range(num_rolls):
            outcome = self._die.sample(weights=self._die.weights).index[0]
            outcomes.append(outcome)
        return outcomes
    
    def current_state(self):
        """
        method to show the die's current state
        """
        return self._die

class Game():
    def __init__():
        pass

class Analyzer():
    def __init__():
        pass