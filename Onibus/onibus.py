from logging import generateLog


class Onibus:
    """
    Bus seats' layout follow these guidelines:
    
    0 — Corridor (not a seat);\n
    1 — Driver's seat;\n
    2 — Unavailable seat.\n
    3 — Available seat;\n
    """
    
    def __init__(self):
        self.matrix_seats: list[list[int]] = self._createBusLayout()
        generateLog('Instancia do onibus criada.')

    def _createBusLayout(self) -> list[list[int]]:
        """
        Create layout of bus' seats following these guidelines:
        
        0 — Corridor (not a seat);\n
        1 — Driver's seat;\n
        2 — Unavailable seat;\n
        3 — Available seat.\n
        """
        driver_row = [[1, 0, 0, 0, 0]]
        passenger_rows = [[3, 3, 0, 3, 3] for row in range(0, 7)]
        bus_seats = driver_row + passenger_rows
        generateLog('Layout de acentos gerado com sucesso.')
        return bus_seats
    
    def sellSeat(self, X: int, Y: int) -> None:
        try:
            match self.matrix_seats[X][Y]:
                case 0:
                    print('Campo escolhido não é um acento.')
                    generateLog(f'Tentativa de comprar acento no local X: {X} Y: {Y} falhou.')
                case 1:
                    print('Você não pode comprar o acento do motorista!')
                    generateLog(f'Tentativa de comprar acento no local X: {X} Y: {Y} falhou.')
                case 2:
                    print('Acento já foi vendido.')
                    generateLog(f'Tentativa de comprar acento no local X: {X} Y: {Y} falhou.')
                case 3:
                    self.matrix_seats[X][Y] = 2
                    print('Acento vendido com sucesso.')
                    generateLog(f'Tentativa de comprar acento no local X: {X} Y: {Y} bem-sucedida.')
        except IndexError:
                print('Escolha um acento dentro da matriz.')
        
    
    def generateRelatorio(self):
        vendidos = 0
        abertos = 0
        for row in range(0, len(self.matrix_seats)):
            for col in range(0, len(self.matrix_seats[row])):
                if self.matrix_seats[row][col] == 3:
                    abertos += 1
                elif self.matrix_seats[row][col] == 2:
                    vendidos += 1
        msg = f'Onibus vendeu {vendidos} acentos, deixando {abertos} sem vender.'
        generateLog(msg=msg, file='relatorio', timestamp=False)
        generateLog('Relatorio gerado sobre venda de acentos')
        print('Relatório gerado com sucesso, cheque "relatorio.txt" na pasta raiz do programa.')