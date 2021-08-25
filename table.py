class Table:
    __safeZone = (5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 68)
    __init_position = [("Y", 5), ("B", 22), ("R", 39), ("G", 56)]
    __exit_hall = [("Y", 68), ("B", 17), ("R", 34), ("G", 51)]

    table = []

    def __init__(self):
        for i in range(1, 69):
            if i in self.__safeZone:
                self.table.append(["Secure"])
            else:
                self.table.append([i])

    def get_init_position(self):
        return self.__init_position

    def get_safe_zone(self):
        return self.__safeZone

    def get_exit_halls(self):
        return self.__exit_hall
