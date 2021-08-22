class Player:
    __name:str
    __colour:str
    def __init__(self,name,colour):
        self.__name=name
        self.__colour=colour
    def get_colour(self):
        return self.__colour
    def get_name(self):
        return self.__name
    def to_string(self):
        return '('+self.__name + ','+self.__colour+')'
