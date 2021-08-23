from token import Token
from table import Table
from game import Game
from player import Player
from  os import system

p1=Player('Herrera','B')
p2=Player('CPU','G')
tokens=(Token('Home','B',1),Token('Home','B',2),Token('Home','G',3),Token('Home','G',4))
g=Game(tokens,('B','G'))
table=g.get_table()
tokens=g.get_tokens()
#Start the player who has the highest value
system('cls')
print('********Game started*********')
#print(p1.to_string())
while True:
    system('pause')
    #system('cls')
    g.print_game()
    id=int(input('ID:'))
    r=int(input('Dice:'))
    g.move(id,r)


