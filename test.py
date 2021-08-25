from pawn import Pawn
from table import Table
from game import Game
from player import Player
from os import system

p1 = Player("Herrera", "B")
p2 = Player("CPU", "G")
pawns = (
    Pawn("Home", "B", 1),
    Pawn("Home", "B", 2),
    Pawn("Home", "G", 3),
    Pawn("Home", "G", 4),
)
g = Game(pawns, ("B", "G"))
# Start the player who has the highest value
print("********Game started*********")
# print(p1.to_string())
while True:
    system("pause")
    # system('cls')
    g.print_game()
    r = int(input("Dice:"))
    id = int(input("ID:"))
    g.make_move(id, r)
