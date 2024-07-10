import numpy as np
import pandas as pd

import unittest
from montecarlo.montecarlo import Die, Game, Analyzer

class MonteCarloTestSuite(unittest.TestCase):

    def test_1_Die_init(self):
        '''
        initialize a die with 3 faces. 
        test whether faces is an array with distinct values.
        '''
        faces = np.array(['a','b','c'])
        die1 = Die(faces)
        
        expected = (type(faces) == np.ndarray) & (len(faces) == len(np.unique(faces)))
        self.assertTrue(expected)
   
    def test_2_change_weight(self):
        '''
        change the weight of one face. 
        test if the new weight is in the dataframe.
        '''
        die1 = Die(np.array([1,2,3]))
        die1.change_weight(1,5)
        
        expected = die1.current_state().weights.isin([5]).sum()
        self.assertTrue(expected)
    
    def tests_3_roll_die(self):
        '''
        roll the die twice. 
        test if the method returns a list of length 2.
        '''
        die1 = Die(np.array(['x','y','z']))
        
        expected = isinstance(die1.roll_die(2), list) and len(die1.roll_die(2))==2
        self.assertTrue(expected)
    
    def test_4_current_state(self):
        '''
        initialize a die with 6 faces. 
        test if the dataframe returned by current_state() has an index of length 6
        '''
        die1 = Die(np.array(['this','die','has','six','total','faces']))
        
        actual = len(die1.current_state())
        expected = 6
        self.assertEqual(actual, expected)
    
    def test_5_Game_init(self):
        '''
        initialize a Game objects. 
        test if die_list input is a list.
        '''
        die1 = Die(np.array(['1','2','3']))
        die2 = Die(np.array(['1','2','3']))
        game1 = Game([die1, die2])
        
        expected = type(game1.die_list) == list
        self.assertTrue(expected)
    
    def test_6_play_game(self):
        '''
        play a game with 5 rolls.
        test if results are properly stored in a dataframe with an index length of 5
        '''
        die1 = Die(np.array(['1','2','3']))
        die2 = Die(np.array(['1','2','3']))
        game1 = Game([die1, die2])
        game1.play_game(5)
        
        expected = (isinstance(game1.game_results(), pd.DataFrame)) & (len(game1.game_results())==5)
        self.assertTrue(expected)
    
    def test_7_game_results(self):
        '''
        return the game_results in both wide and narrow form.
        test if the dataframes are different shapes.
        '''
        die1 = Die(np.array(['1','2','3']))
        die2 = Die(np.array(['1','2','3']))
        game1 = Game([die1, die2])
        game1.play_game(5)
        
        wide = game1.game_results(form = "wide")
        narrow = game1.game_results(form = "narrow")
        
        expected = (wide.shape == narrow.shape)
        self.assertFalse(expected)
    
    def test_8_Analyzer_init(self):
        '''
        initialize an Analyzer object.
        test if outcomes attribute is formatted as a data frame.
        '''
        die1 = Die(np.array(['1','2','3']))
        die2 = Die(np.array(['1','2','3']))
        game1 = Game([die1, die2])
        game1.play_game(5)
        analyzer1 = Analyzer(game1)
        
        expected = isinstance(analyzer1.outcomes, pd.DataFrame)
        self.assertTrue(expected)
    
    def test_9_jackpot(self):
        '''
        compute the number of jackpots.
        test if resulting output is an numpy integer.
        '''
        die1 = Die(np.array(['1','2','3']))
        die2 = Die(np.array(['1','2','3']))
        game1 = Game([die1, die2])
        game1.play_game(1000)
        analyzer1 = Analyzer(game1)
        
        expected = isinstance(analyzer1.jackpot(), np.int64)
        self.assertTrue(expected)
    
    def test_10_face_counts(self):
        '''
        compute the face counts.
        test if the resulting dataframe has a column for every die.
        '''
        die1 = Die(np.array([1,2,3]))
        die2 = Die(np.array([1,2,3]))
        game1 = Game([die1, die2])
        game1.play_game(1000)
        analyzer1 = Analyzer(game1)
        
        expected = analyzer1.face_counts().columns.isin([1,2,3]).all()
        self.assertTrue(expected)
    
    def test_11_combo_count(self):
        '''
        compute the combinations.
        test if the resulting dataframe is multi-indexed.
        '''
        die1 = Die(np.array([1,2,3]))
        die2 = Die(np.array([1,2,3]))
        game1 = Game([die1, die2])
        game1.play_game(1000)
        analyzer1 = Analyzer(game1)
        
        expected = isinstance(analyzer1.combo_count().index, pd.MultiIndex)
        self.assertTrue(expected)
    
    def test_12_perm_count(self):
        '''
        compute the permutations.
        test if the sum of all the permutation counts is equal to the number of rolls.
        '''
        die1 = Die(np.array([1,2,3]))
        die2 = Die(np.array([1,2,3]))
        game1 = Game([die1, die2])
        game1.play_game(1000)
        analyzer1 = Analyzer(game1)
        
        self.assertEqual(analyzer1.perm_count()['count'].sum(),1000)

if __name__ == '__main__':
    
    unittest.main(verbosity=3)