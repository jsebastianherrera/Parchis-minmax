from os import system
from random import randint 
from token import Token
from table import Table
class Game:
   __table=Table()
   
   
   def __init__(self,token,colors):
      self.__token=token
      self.__init_game(colors)

   def get_tokens(self):
      return self.__token

   def get_table(self):
      return self.__table.table

   def dice_value():
      return randint(1,6)

   def move(self,id,dice):
      token=self.__token[self.__get_token_pos(id)]
      if dice == 5:
         home=self.__check_take_out(token.get_colour())
         if len(home)!=0:
            self.__take_out_home(self.__token[home[0]])
         else:
            self.__move(token.get_id(),dice)
      elif dice==6:
            if len(self.__get_tokens_by_colour(token.get_colour()))== 2:
               self.__move(token.get_id(),dice+1)
            else:
               self.__move(token.get_id(),dice)
            print('Roll the dice again')
            self.move(dice=int(input('Dice:')),id=int(input('Id:')))
      else:
         self.__move(token.get_id(),dice)
         self.__can_eat(id,token.get_position())
 
   def __check_wall(self,colour,pos)->True:
      tok,id=self.__table.table[pos-1]
      rt=[]
      for i in tok:
         c=0
         for j in tok:
            if i.get_colour()!=colour and j.get_colour()!=colour:
               c+=1
         rt.append(c)
      if i in rt == 2:
         return True
      return False
      
      
      
   def __check_hallway(self,token,dice):
      index=0
      if token.get_position()+dice>=68:
         index=token.get_position()-68+dice
      else:
         index=token.get_position()+dice
   
      if token.get_colour()=='Y':
           if index==0:
                 return True,68
           elif index>=63  and index<=68:
                  return True,index-63
           elif index==1:
              return True,index
           else: 
                 return False,None        
           
      elif token.get_colour()=='B' and index>=17 and index<=22:
         index=token.get_position()+dice-17
         return True,index  
      elif token.get_colour()=='R' and index>=34 and index<=39:
         index=token.get_position()+dice-34
         return True,index
      elif token.get_colour()=='G' and index>=51 and index<=56:
         index=token.get_position()+dice-51
         return True,index      
              
      return False,None
 
   def __get_rival_tokens(self,colour:str):
        
      """
      Parameters
      __________
      param1:str
         Receive the current player's colour
      Returns
      _______
      list 
         Return a list with the tokens in game that can be eaten
      """ 
      rt=[]
      for i in self.__token:
         if i.get_colour()!=colour:   
            if i.get_state() =='InGame':
               print('Vallll')
               rt.append(i)
      return rt
   def __can_eat(self,id:int,pos:int):
      token=self.__token[self.__get_token_pos(id)]
      rivals=self.__get_rival_tokens(token.get_colour())
      if len(rivals) >=0:
         for i in rivals:
            if token.get_position() == i.get_position():
               self.__table.table[i.get_position()-1].remove((i,i.get_id()))
               system('cls')
               i.set_position(0)
               i.set_state('Home')
               
      
   def __move(self,id:int,dice):
     token=self.__token[self.__get_token_pos(id)]
     if token.get_state()=='InGame' or token.get_state()=='Safe' or token.get_state()=='Home':
         
         if token.get_position()+ dice>=68:
            index=(token.get_position()+dice)-68
            if index==0:
               index=68
            check,mov=self.__check_hallway(token,dice)
            if check:
               self.__table.table[token.get_position()-1].remove((token,token.get_id()))
               token.set_position(mov)
               token.set_state('Hallway')
            else:
               self.__table.table[token.get_position()-1].remove((token,token.get_id()))
               if index in self.__table.get_safe_zone():
                  token.set_state('Safe')
               else:  
                  token.set_state('InGame')
               token.set_position(index)
               self.__table.table[index-1].append((token,token.get_id()))
                     
         else:
               index=token.get_position()+dice
               check,mov=self.__check_hallway(token,dice)
               #The token is in the hallway
               if check:
                  self.__table.table[token.get_position()-1].remove((token,token.get_id()))
                  token.set_position(mov)
                  token.set_state('Hallway')
               else:
                  self.__table.table[token.get_position()-1].remove((token,token.get_id()))
                  if index in self.__table.get_safe_zone():
                     token.set_state('Safe')
                  else:
                     token.set_state('InGame')
                  token.set_position(index)
                  self.__table.table[index-1].append((token,token.get_id()))
     elif token.get_state()=='Hallway':
         if token.get_position()+dice<7:
            token.set_position(token.get_position()+dice)
         elif token.get_position()+dice==8:
            token.set_state('Completed')
            token.set_position(-1)
         else:
            print('Excedido')
   def __get_token_in_game_by_colour(self,colour):
      rt=[]
      for i in self.__token:
         if i.get_colour()==colour and i.get_state()=='InGame':
            rt.append(i)
      return rt
            
            
   def __get_token_pos(self,id) -> int:
      pos=0
      for i in self.__token:
         if i.get_id() == id:
            return pos
         pos+=1 
      return -1
   def __init_game(self,colors):
     for i in colors:
        tokens=self.__get_tokens_by_colour(i)
        self.__take_out_home(tokens[0])
   def __get_tokens_by_colour(self,colour:str):
      rt=[]
      for i in self.__token:
         if i.get_colour()==colour:
            rt.append(i)
      return rt
   def __take_out_home(self,token):
          check=self.__check_take_out(token.get_colour())
          if len(check):   
            token.set_position(self.__init_token(token))
            aux=list(self.__table.table[token.get_position()-1])
            aux.append((token,token.get_id()))
            token.set_state('Safe')
            self.__table.table[token.get_position()-1]=aux 
            
   def __init_token(self,token):
      positions=self.__table.get_init_position()
      for i,j in positions:
            if i == token.get_colour():
                return j         
      return -1
   
   def print_hallway(self):
      for i in self.__in_hallway:
         print(i)
   
   def print_game(self):
      for i in self.__token:
         print(i.to_string())
      system('pause')
      
      for i in range(1,25):
         print('*',end='*')
      print()
      for i in self.__table.table:
         print(i)
      for i in range(1,25):
         print('*',end='*')
      print()
   
   def __check_take_out(self,colour):
      rt=[]
      for i in self.__token: 
         if i.get_colour()==colour and i.get_state()=='Home':
            rt.append(self.__get_token_pos(i.get_id()))      
      return rt              
   