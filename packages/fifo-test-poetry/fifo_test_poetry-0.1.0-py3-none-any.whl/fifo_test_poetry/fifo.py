class Fifo:
    def __init__(self):
        self.__fifo = list()

    def insert(self, to_insert: object) -> None:
        self.__fifo.append(to_insert)

    def pop(self):
        return self.__fifo.pop(0)

    def __len__(self):
        return len(self.__fifo)
