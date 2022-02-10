from typing import Union
from termcolor import colored
import pandas as pd
import numpy as np
from numpy.random import randint

class Player:
    @classmethod
    def __set_vocab__(self, path_to_vocabulary):

        with open(path_to_vocabulary,'r') as f:
            dictionary = [list(t) for t in f.readlines()[0].strip().split(",") if len(t) == 5]
        
        self.vocab = pd.DataFrame(dictionary)
        return

    def __init__(self, dictionary_path = "wordle.txt", verbose = True):
        self.word_length = 5
        self.guess_number = 0
        self.__set_vocab__(dictionary_path)

        self.verbose = verbose

        self._board_response = []

        self.information_gain_history = []

        return
    @property
    def board_response(self):
        return self._board_response

    # board_response function gets triggered whenever there is a change in value of board_response variable
    @board_response.setter
    def board_response(self, response: str)-> None:
        self._board_response = response
        if type(response) == int:
            if response == -1:
                return ('Game Over')
            else:
                return (f'win at turn {response}')
        
        # response = np.array(response)

        for index, res in enumerate(response):
            if res == 'G':
                # print(colored(self.guessed_word[index], "green"))
                self.vocab = self.vocab[self.vocab[index] == self.guessed_word[index]]
            elif res == 'B':
                if self.guessed_word[index] in self.guessed_word.iloc[np.where(response == 'G')]:
                    print("here")
                    continue
                # print(colored(self.guessed_word[index], "red"))
                self.vocab = self.vocab[self.vocab.apply(lambda x: (self.guessed_word[index] not in ''.join(x)), axis= 1)]
            elif res =='Y':
                # print(colored(self.guessed_word[index], "yellow"))
                self.vocab = self.vocab[self.vocab.apply(lambda x: ((self.guessed_word[index] in ''.join(x)) and (self.guessed_word[index] != x[index])), axis= 1)]
                
        self.vocab.reset_index(drop= True, inplace= True)
        return

    def information_gain(self):
        probability = self.vocab.apply(pd.value_counts)
        
        probability = probability/probability.sum()
        
        information = -probability*np.log2(probability)
        
        information = information.to_dict()

        information_df = pd.DataFrame(self.vocab.apply(lambda x: ([information[x.name][i] for i in x])).sum(axis=1), columns= ['information'])
        information_df['word'] = self.vocab.apply(lambda x: (''.join(x)), axis= 1)
        
        return information_df
        

    def guess(self):
        self.information_df = self.information_gain().sort_values(by= ['information'], ascending= False).reset_index(drop= True)

        if self.verbose:
            print(self.information_df)
        # if self.guess_number == 0:

        
        information, self.guessed_word = self.information_df.iloc[ self.information_df['information'].idxmax()].to_list()
        self.information_gain_history.append(np.round(information, 3))
        
        if self.verbose:
            print(f"information gain: {self.information_gain_history[-1]}")
        
        self.guess_number += 1
        self.guessed_word = pd.Series(list(self.guessed_word))
        return ''.join(self.guessed_word)
    
    def render(self):
        print('wordle:', ''.join(self.wordle))
        print('board:')
        for arr in self.board:
            for t in arr:
                print(t,end="")
            print()
        return
# %%
