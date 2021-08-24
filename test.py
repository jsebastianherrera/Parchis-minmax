from token import Token
from table import Table
from game import Game
from player import Player
from  os import system

p1=Player('Herrera','B')
p2=Player('CPU','G')
tokens=(Token('Home','B',1),Token('Home','B',2),Token('Home','G',3),Token('Home','G',4))
g=Game(tokens,('B','G'))
#Start the player who has the highest value

print('********Game started*********')
#print(p1.to_string())
while True:
    system('pause')
    #system('cls')
    g.print_game()
    r=int(input('Dice:'))
    id=int(input('ID:'))
    g.move(id,r)


