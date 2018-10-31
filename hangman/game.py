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
            word=self.answer.lower()
            char=char.lower()
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
        self.remaining_misses=number_of_guesses
        self.word=GuessWord(self.select_random_word(word_list))
        self.isfinished=self.is_finished()
        self.iswon=self.is_won()
        self.islost=self.is_lost()

    @classmethod    
    def select_random_word(cls,list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        else:
            word_list=list_of_words
            word= random.choice(word_list)
            return word
        
    def guess(self,char):
        char=char.lower()
        self.previous_guesses.append(char)
        self.number_of_guesses-=1    
        if self.isfinished==True:
            raise GameFinishedException
        else:
            if self.word.perform_attempt(char).is_hit()==True:
                self.remaining_misses=self.remaining_misses
                if '*' not in self.word.masked:
                    self.isfinished=True
                    self.iswon=True
                    raise GameWonException
            else:
                self.remaining_misses-=1
                if self.remaining_misses==0:
                    self.isfinished=True
                    self.islost=True
                    raise GameLostException
            return self.word.perform_attempt(char)
        
        
    def is_finished(self):
        if self.is_won()==True or self.is_lost()==True or self.number_of_guesses==0:
            self.isfinished=True
            return True
        else:
            return False
    
    def is_won(self):
        if '*' not in self.word.masked:
            self.iswon=True
            return True
        else:
            return False
    
    def is_lost(self):
        if self.remaining_misses==0:
            self.islost=True
            return True
        else:
            return False