from onibus import Onibus

class NotInRangeException(Exception):
    pass

def main():
    bus = Onibus()
    while True:
        try:
            print('Escolha uma das seguintes opções:\n'
                + '0 - Sair\n'
                + '1 - Comprar Acento;\n'
                + '2 - Gerar relatório;\n')
            option = input('>>> ')
            if int(option) not in range(0, 3):
                raise NotInRangeException(option)
            match int(option):
                case 0:
                    print('Encerrando sistema.')
                    return
                case 1:
                    print('* | 0  1  2  3  4\n'
                        + '——+——————————————')
                    for index, row in enumerate(bus.matrix_seats):
                        print(f'{index} |{row}')
                    print('\nEscolha, de acordo com a matriz, a posição X e Y do acento que deseja comprar, divididas por um espaço.\n'
                        + '(Exemplo: "1 2")\n'
                        + 'Legenda:\n'
                        + '0 — Corredor (não é um acento);\n'
                        + '1 — Acento do motorista;\n'
                        + '2 — Acento indisponível;\n'
                        + '3 — Acento disponível.\n')
                    acento = list(map(int, input('>>> ').split(' ')))
                    bus.sellSeat(acento[0], acento[1])
                case 2:
                    bus.generateRelatorio()            
        except NotInRangeException as e:
            print(f'{e} não está entre as opções disponíveis.')
        except ValueError:
            print(f'Opção(ões) não é um número.')


if __name__ == "__main__":
    main()