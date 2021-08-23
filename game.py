from os import system
from random import randint 
from token import Token
from table import Table
class Game:
   __table=Table()
   __in_hallway=[]
   
   
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
      token=self.__token[self.__get_token(id)]
      if dice == 5:
         home=self.__check_take_out(token.get_colour())
         if len(home)!=0:
            self.__take_out_home(home[0][0])
         else:
            self.__move(token.get_id(),dice)
      else:
         self.__move(token.get_id(),dice)
         
   def __safe_zone(self,pos) -> bool:
      if pos in self.__table.get_safe_zone():
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
           
      elif token.get_colour()=='B' and index>=12 and index<=18:
         index=token.get_position()+dice-12
         return True,index    
      elif token.get_colour()=='R' and index>=29 and index<=35:
         index=token.get_position()+dice-29
         return True,index
      elif token.get_colour()=='G' and index>=46 and index<=52:
         index=token.get_position()+dice-46
         return True,index      
              
      return False,None
   
            
   def __move(self,id:int,dice):
     token=self.__token[self.__get_token(id)]
     if token.get_state()=='InGame' or token.get_state()=='Safe' or token.get_state()=='Home':
         if token.get_position()+ dice>=68:
            index=(token.get_position()+dice)-68
            if index==0:
               index=68
            check,mov=self.__check_hallway(token,dice)
            if check:
               self.__table.table[token.get_position()-1].remove((token,token.get_id()))
               token.set_position(-1)
               token.set_state('Hallway')
               self.__in_hallway.append((token,mov))
            else:
               self.__table.table[token.get_position()-1].remove((token,token.get_id()))
               token.set_state('InGame')
               token.set_position(index)
               self.__table.table[index-1].append((token,token.get_id()))
                     
         else:
               index=token.get_position()+dice
               check,mov=self.__check_hallway(token,dice)
               print(check)
               #The token is in the hallway
               if check:
                  self.__table.table[token.get_position()-1].remove((token,token.get_id()))
                  token.set_position(-1)
                  token.set_state('Hallway')
                  self.__in_hallway.append((token,mov))
               else:
                  self.__table.table[token.get_position()-1].remove((token,token.get_id()))
                  token.set_state('InGame')
                  token.set_position(index)
                  self.__table.table[index-1].append((token,token.get_id()))
     elif token.get_state()=='Hallway':
        #Check hallway
        print('aaaa')
                
                  
   def __get_token(self,id) :
      pos=0
      for i in self.__token:
         if i.get_id() == id:
            return pos
         pos+=1 

   def __init_game(self,colors):
     for i in colors:
        aux=self.__check_take_out(i)
        if len(aux)!=0:
            pos=self.__get_token(aux[0][1]) 
            self.__token[pos].set_state('Safe')
            self.__token[pos].set_position(self.__init_token(aux[0][0]))
            pnt=self.__token[pos]
            self.__table.table[pnt.get_position()-1].append((pnt,pnt.get_id())) 
         

   def __check_take_out(self,colour):
      rt=[]
      for i in self.__token: 
         if i.get_colour()==colour and i.get_state()=='Home':
            rt.append((i,i.get_id()))      
      return rt              
   
   def __take_out_home(self,token):
           token.set_position(self.__init_token(token))
           aux=list(self.__table.table[token.get_position()-1])
           aux.append((token,token.get_id()))
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
   