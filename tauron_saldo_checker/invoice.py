class Invoice:

    def __init__(self, name, saldo, date):
        self.name = name
        self.saldo = saldo
        self.date = date

    def __str__(self) -> str:
        return f'{self.name}: {self.saldo} ({self.date})'

    def __repr__(self) -> str:
        return f'({self.__str__()})'



