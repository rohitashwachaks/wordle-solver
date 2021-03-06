from typing import Union
from termcolor import colored
import pandas as pd
import numpy as np

#%%
class Wordle:
    @classmethod
    def __set_riddle__(self, path_to_vocabulary):

        with open(path_to_vocabulary,'r') as f:
            self.dictionary = {t.strip() for t in f.readlines()[0].split(",")}
        
        rand_pick = np.random.randint(low = 0, high = (len(self.dictionary)))
        
        self.wordle = list(self.dictionary)[rand_pick]
        return

    def __init__(self, dictionary_path = "wordle.txt", verbose = True):
        self.word_length = 5
        self.num_tries = 6

        self.guess_number = -1
        self.board = [['.'] * self.word_length] * self.num_tries

        self.verbose = verbose

        self.__set_riddle__(dictionary_path)
        return

    @classmethod
    def alphabet(self,x: Union[str,int])->Union[int,str]:
        if type(x) == str:
            return ord(x) - ord('A')
        elif type(x) == int:
            return chr(x+ord('A'))
        else:
            return None

    def play(self, guess: str)-> None:
        guess = guess.upper()
        self.guess_number += 1
        
        if guess not in self.dictionary:
            if self.verbose:
                print("Invalid word")
            self.guess_number -= 1
            return []

        if self.guess_number >= self.num_tries:
            if self.verbose:
                print(colored("GAME OVER","red"))
            return -1

        if guess == ''.join(self.wordle):
            board_entry = [colored(" "+x+" ",'grey',"on_green") for x in guess];
            if self.verbose:
                [print(x,end="") for x in board_entry];
                print()
                print(colored("GAME OVER","green"))
            self.board[self.guess_number] = board_entry
            return self.guess_number+1

        response = []
        board_entry = []
        for index, ch in enumerate(guess):
            # green
            if ch == self.wordle[index]:
                board_entry.append(colored(" "+ch+" ",'grey',"on_green"))
                response.append('G')
            
            # yellow
            elif ch in ''.join(self.wordle):
                board_entry.append(colored(" "+ch+" ",'grey','on_yellow'))
                response.append('Y')
            else:
                board_entry.append(" "+ch+" ")
                response.append('B')

        self.board[self.guess_number] = board_entry
        if self.verbose:
            [print(x,end="") for x in board_entry];
            print()
        return response
    
    def render(self):
        print('wordle:', ''.join(self.wordle))
        print('board:')
        for arr in self.board:
            for t in arr:
                print(t,end="")
            print()
        return
