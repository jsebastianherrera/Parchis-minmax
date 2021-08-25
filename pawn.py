class Pawn:
    __position = 0

    def __init__(self, state, colour, id: int):
        self.__state = state
        self.__colour = colour
        self.__id = id

    def get_id(self):
        return self.__id

    def to_string(self):
        return (
            self.__colour
            + " "
            + str(self.__position)
            + " "
            + self.__state
            + " "
            + str(self.__id)
        )

    # Getters
    def get_state(self):
        return self.__state

    def get_colour(self):
        return self.__colour

    def get_position(self):
        return self.__position

    # setter
    def set_state(self, val):
        self.__state = val

    def set_colour(self, val):
        self.__colour = val

    def set_position(self, val):
        self.__position = val
