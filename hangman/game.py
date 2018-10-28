from .exceptions import *

import random 

class GuessAttempt(object):
    def __init__(self,char,hit=None,miss=None):
        self.char=char
        self.miss=miss
        self.hit=hit
        if self.miss==self.hit==True:
            raise InvalidGuessAttempt
        
    def is_hit(self):
        if self.hit==True:
            self.miss==False
            return True
        else:
            self.hit=True
            return False
    
    def is_miss(self):
        if self.miss==True:
            self.hit==False
            return True
        else:
            self.hit=True
            return False


class GuessWord(object):
    def __init__(self,answer):
        if answer:
            self.answer=answer
            self.masked='*'*len(answer)
        else:
            raise InvalidWordException

    def perform_attempt(self,char):
        if len(char)==1:
            if char.islower():
                word=self.answer.lower()
            elif char.isupper():
                word=self.answer.upper()
            lst=list(word)
            if char in lst:
                for x,y in enumerate(lst):
                    if y==char:
                        mask_lst=list(self.masked)
                        mask_lst[x]=y
                        self.masked=("".join(mask_lst))
                return GuessAttempt(char,hit=True)
            else:
                return GuessAttempt(char,miss=True)
                self.masked=("".join(mask_lst))
        else:
            raise InvalidGuessedLetterException


class HangmanGame(object):
    
    WORD_LIST=['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list=WORD_LIST,number_of_guesses=5):
        self.word_list=word_list
        self.number_of_guesses=number_of_guesses
        self.previous_guesses=[]
        self.remaining_misses=self.number_of_guesses
        self.word=GuessWord(self.select_random_word(word_list))
        
    def select_random_word(self,list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        else:
            self.word_list=list_of_words
            self.word= random.choice(self.word_list)
            return self.word
        
    def guess(self,char):
        self.previous_guesses.append(char)
        if GuessAttempt(char).is_miss==True:
            self.remaining_misses=self.number_of_guesses-1
        else:
            self.remaining_misses=self.remaining_misses
        if '*' in self.word.masked:
            return self.word.perform_attempt(char)
        else:
            raise GameWonException
                
    def is_finished(self):
        return True
    
    def is_won(self):
        if '*' not in self.word.masked:
            return True
        else:
            return False
    
    def is_lost(self):
        if '*' in self.word.masked:
            return True
        else:
            return False