from os import system
from random import randint
from pawn import Pawn
import copy
import sys
import math
from table import Table


class Game:
    __change: bool
    __colors = ()
    __table = Table()

    def __init__(self, pawn, colors):
        self.__pawn = pawn
        self.__colors = colors
        self.__init_game(colors)
        self.__change = False

    def get_pawns(self):
        return self.__pawn

    def get_table(self):
        return self.__table.table

    def dice_value():
        return randint(1, 6)

    def __get_pawn_same_pos(self, pos):
        rt = []
        for i in self.__pawn:
            if i.get_position() == pos:
                rt.append(i)
        return rt

    def make_move(self, id, dice):
        system("cls")
        print("Possible mov")
        tmp = self.__available_movements(
            self.__pawn[self.__get_pawn_pos(id)].get_colour()
        )
        for i in tmp:
            print(i)
        # self.__minimax_val(self.__pawn[id].get_colour(), 0)
        # system("pause")

        self.__check_winner()
        pawn = self.__pawn[self.__get_pawn_pos(id)]
        if dice == 5:
            home = self.__check_take_out(pawn.get_colour())
            if len(home) != 0:
                self.__take_out_home(self.__pawn[home[0]])
            else:
                self.__move(pawn.get_id(), dice)
        elif dice == 6:
            if len(self.__get_pawns_by_colour(pawn.get_colour())) == 2:
                self.__move(pawn.get_id(), dice + 1)
            else:
                self.__move(pawn.get_id(), dice)
            print("Roll the dice again")
            self.move(dice=int(input("Dice:")), id=int(input("Id:")))
        else:
            self.__move(pawn.get_id(), dice)
            self.__can_eat(id, pawn.get_position())

    def __check_wall(self, colour, pos) -> bool:
        tok = self.__get_pawn_same_pos(pos)
        c = 0
        for i in tok:
            if i.get_colour() != colour:
                c += 1
        if c == 2:
            return True
        return False

    def __check_hallway(self, pawn, dice):
        index = self.__pos_move(pawn.get_position() + dice)
        if pawn.get_colour() == "Y":
            if index == 0:
                return True, 68
            elif index >= 63 and index <= 68:
                return True, index - 63
            elif index == 1:
                return True, index
            else:
                return False, None

        elif pawn.get_colour() == "B" and index >= 17 and index <= 22:
            index = pawn.get_position() + dice - 17
            return True, index
        elif pawn.get_colour() == "R" and index >= 34 and index <= 39:
            index = pawn.get_position() + dice - 34
            return True, index
        elif pawn.get_colour() == "G" and index >= 51 and index <= 56:
            index = pawn.get_position() + dice - 51
            return True, index

        return False, None

    def __get_rival_pawns(self, colour: str):

        rt = []
        for i in self.__pawn:
            if i.get_colour() != colour:
                if i.get_state() == "InGame" or i.get_state() == "Safe":
                    rt.append(i)
        return rt

    def __can_eat(self, id: int, pos: int) -> bool:
        pawn = self.__pawn[self.__get_pawn_pos(id)]
        rivals = self.__get_rival_pawns(pawn.get_colour())
        if len(rivals) >= 0:
            for i in rivals:
                if (
                    pawn.get_position() == i.get_position()
                    and pawn.get_state() != "Safe"
                ):
                    self.__table.table[i.get_position() - 1].remove((i, i.get_id()))
                    system("cls")
                    i.set_position(0)
                    i.set_state("Home")
                    return True
        return False

    def __pos_move(self, pos) -> int:
        if pos >= 68:
            index = pos - 68
            if index == 0:
                index = 68
        else:
            index = pos

        return index

    def __update_table(self, pawn, state, mov):
        self.__table.table[pawn.get_position() - 1].remove((pawn, pawn.get_id()))
        pawn.set_position(mov)
        pawn.set_state(state)
        if state != "Hallway":
            self.__table.table[mov - 1].append((pawn, pawn.get_id()))

    def __move(self, id: int, dice):
        pawn = self.__pawn[self.__get_pawn_pos(id)]
        if (
            pawn.get_state() == "InGame"
            or pawn.get_state() == "Safe"
            or pawn.get_state() == "Home"
        ):
            index = self.__pos_move(pawn.get_position() + dice)
            if (
                not self.__check_wall(pawn.get_colour(), index)
                and len(self.__get_pawn_same_pos(index)) < 2
            ):
                check, mov = self.__check_hallway(pawn, dice)
                if check:
                    self.__update_table(pawn, "Hallway", mov)
                    return 50
                else:
                    if index in self.__table.get_safe_zone():
                        self.__update_table(pawn, "Safe", index)
                        return 25
                    else:
                        self.__update_table(pawn, "InGame", index)
                        return -5
            else:
                tmp = self.__get_pawn_in_game_by_colour(pawn.get_colour())
                print(tmp)
                if len(tmp) > 1:
                    tmp.remove(pawn)
                    self.__move(tmp[0].get_id(), dice)
                else:
                    print("U cant move any pawn")
                    return -100

        elif pawn.get_state() == "Hallway":
            if pawn.get_position() + dice < 7:
                pawn.set_position(pawn.get_position() + dice)
            elif pawn.get_position() + dice == 8:
                pawn.set_state("Completed")
                pawn.set_position(-1)
            else:
                print("Excedido")

    def __get_pawn_in_game_by_colour(self, colour):
        rt = []
        for i in self.__pawn:
            if i.get_colour() == colour:
                if i.get_state() == "InGame" or i.get_state() == "Safe":
                    rt.append(i)
        return rt

    def __get_pawn_pos(self, id) -> int:
        pos = 0
        for i in self.__pawn:
            if i.get_id() == id:
                return pos
            pos += 1
        return -1

    def __init_game(self, colors):
        for i in colors:
            pawns = self.__get_pawns_by_colour(i)
            self.__take_out_home(pawns[0])

    def __get_pawns_by_colour(self, colour: str):
        rt = []
        for i in self.__pawn:
            if i.get_colour() == colour:
                rt.append(i)
        return rt

    def __take_out_home(self, pawn):
        check = self.__check_take_out(pawn.get_colour())
        if len(check):
            pawn.set_position(self.__init_pawn(pawn))
            aux = list(self.__table.table[pawn.get_position() - 1])
            aux.append((pawn, pawn.get_id()))
            pawn.set_state("Safe")
            self.__table.table[pawn.get_position() - 1] = aux

    def __init_pawn(self, pawn):
        positions = self.__table.get_init_position()
        for i, j in positions:
            if i == pawn.get_colour():
                return j
        return -1

    def print_hallway(self):
        for i in self.__in_hallway:
            print(i)

    def print_game(self):
        for i in self.__pawn:
            print(i.to_string())
        system("pause")

        for i in range(1, 25):
            print("*", end="*")
        print()
        for i in self.__table.table:
            print(i)
        for i in range(1, 25):
            print("*", end="*")
        print()

    def __check_take_out(self, colour):
        rt = []
        for i in self.__pawn:
            if i.get_colour() == colour and i.get_state() == "Home":
                rt.append(self.__get_pawn_pos(i.get_id()))
        return rt

    def _read_dice(self):
        self.change = True
        value = int(input("Dice:"))
        if value >= 1 and value <= 6:
            return value
        exit()

    def dice_result(self):
        return randint(1, 6)

    def __check_winner(self):
        c1 = []
        c2 = []
        for i in self.__pawn:
            if i.get_colour() == "B" and i.get_state() == "Completed":
                c1.append(i)
            elif i.get_colour() == "G" and i.get_state() == "Completed":
                c2.append(i)

        if len(c1) == 2 or len(c2) == 2:
            return True
        return False

    # Max IA -> Min_ person
    def __minimax(self, colour, depth, isMaximizing):
        winner = self.__check_winner()
        if winner:
            print("Someone has won")
            return
        if isMaximizing:
            movements = self.__available_movements(colour)
            bestScore = -math.inf
            id = []
            dice = self.dice_result()
            for i in movements:
                id.append(i.pop(0))
            if len(id) > 1:
                if self.__evaluate(id[0], dice) > self.__evaluate(id[1], dice):
                    if self.__evaluate(id[0], dice) > bestScore:
                        bestScore = self.__evaluate(id[0], dice)
                    else:
                        bestScore = self.__evaluate(id[1], dice)

                else:
                    if self.__evaluate(id[0], dice) > bestScore:
                        bestScore = self.__evaluate(id[0], dice)
                    else:
                        bestScore = self.__evaluate(id[1], dice)
            else:
                self.__move(id[0], dice)
            self.__minimax("G", depth + 1, False)
        else:
            movements = self.__available_movements(colour)
            bestScore = -math.inf
            id = []
            dice = self.dice_result()
            for i in movements:
                id.append(i.pop(0))
            if len(id) > 1:
                if self.__evaluate(id[0], dice) > self.__evaluate(id[1], dice):
                    if self.__evaluate(id[0], dice) > bestScore:
                        bestScore = self.__evaluate(id[0], dice)
                    else:
                        bestScore = self.__evaluate(id[1], dice)

                else:
                    if self.__evaluate(id[0], dice) > bestScore:
                        bestScore = self.__evaluate(id[0], dice)
                    else:
                        bestScore = self.__evaluate(id[1], dice)
            else:
                self.__move(id[0], dice)
            self.__minimax("G", depth + 1, False)

    # *****************************************************************
    def __top_pawn(self, colour):
        mov = []
        pawns = self.__get_pawns_by_colour(colour)
        if len(pawns) >= 1:
            for i in pawns:
                if i.get_state() == "Hallway":
                    return i.get_id()
                elif i.get_state() == "InGame":
                    mov.append(i)
        else:
            return pawns[0].get_id()

    def __evaluate(self, pawn, dice):
        index = self.__pos_move(pawn.get_position() + dice)
        score = 0
        # All the pawnw with the same colour
        if self.__check_wall(colour=pawn.get_colour(), pos=index):
            score += -1
        if self.__can_be_eaten(index):
            score += -5
        if index in self.__table.get_safe_zone:
            score += 2
        elif pawn._get_state() == "InGame":
            score += 1
        elif pawn.get_state() == "InHallway" or self.__check_hallway(pawn, dice)[0]:
            score += 8
        elif pawn.get_state() == "Completed":
            score += 10

    def __can_be_eaten(self, pawn) -> bool:
        rivals = self.__get_rival_pawns(pawn.get_colour())
        for i in rivals:
            for j in range(1, 6):
                if self.__pos_move(i.get_position() + j) == pawn.get_position():
                    return True

        return False

    def __available_movements(self, colour):
        poss_mov = []
        id = self.__get_pawns_by_colour(colour)
        c = 0
        for i in id:
            pawn = i
            aux = []
            aux.append(pawn.get_id())
            for j in range(1, 6):
                if pawn.get_state() == "InGame" or pawn.get_state() == "Safe":
                    index = self.__pos_move(pawn.get_position() + j)
                    if (
                        not self.__check_wall(pawn.get_colour(), index)
                        and len(self.__get_pawn_same_pos(index)) < 2
                    ):
                        aux.append(j)
                    else:
                        break
                elif pawn.get_state() == "Home" and j == 5:
                    if len(self.__check_take_out(pawn.get_colour())) != 0:
                        aux.append(j)
                elif pawn.get_state() == "Hallway":
                    if pawn.get_position() + j <= 8:
                        aux.append(j)

            poss_mov.append(aux)
            c += 1
        return poss_mov
