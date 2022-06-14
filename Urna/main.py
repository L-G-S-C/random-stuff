from typing import List, Dict, Any

def getIntFromUser(msg: str) -> int:
    while True:
        try:
            out: int = int(input(f'{msg}\n>>> '))
        except ValueError:
            print('Erro no sistema. Você inseriu um caractére não-númerico?\n'
                + 'Tente novamente.')
            continue
        else:
            return out

def stringHasNumber(target_str: str) -> bool:
    return any(char.isdigit() for char in target_str)

def stringHasSpecialChars(target_str: str) -> bool:
    return any(char for char in target_str if not char.isalnum() and not char.isspace())


class CandidatoNotInListError(Exception):
    pass

class AnswerNotInRangeError(Exception):
    pass

class SenhaInvalidaError(Exception):
    pass

class NotEnoughCandidatosError(Exception):
    pass

class NomeCandidatoInvalido(Exception):
    pass

class NomeCandidatoVazio(Exception):
    pass

class Candidato:

    def __init__(self, nome: str, digito: int):
        self.votos: int = 0
        self.nome = nome
        self.digito = digito

class Urna:
    def __init__(self, candidatos: List[Candidato], senha: int):
        self.list_candidatos = candidatos
        self.senha = senha
        self._votos_totais: int = 0
        self._votos_nulos: int = 0
        self._votos_brancos: int = 0
        self._votos_validos: int = 0
    
    def showCandidatos(self):
        for candidato in self.list_candidatos:
            print(f'Candidato: {candidato.nome}\n'
                + f'Digito: {candidato.digito}\n\n')

    def checkDigitoCadidato(self, digito: int) -> bool:
        for candidato in self.list_candidatos:
            if candidato.digito == digito:
                return True
        return False
    
    # Polish later
    def getCandidatoByDigito(self, digito: int) -> Candidato:
        for candidato in self.list_candidatos:
            if candidato.digito == digito:
                return candidato
        raise CandidatoNotInListError()

    @staticmethod # Usando isso como um staticmethod para eu não ter que converter isso numa função regular e refatorar o código todo.
    def confirmaAcaoUser(msg, respotaRange: List[int]) -> int:
        out = ''
        while out not in respotaRange:
            try:
                out = int(input(f'{msg}\n>>> '))
                if out not in respotaRange:
                    raise AnswerNotInRangeError()

            except ValueError:
                print('Erro no sistema. Você inseriu um caractére não-númerico?\n'
                + 'Tente novamente.')
            
            except AnswerNotInRangeError:
                print('Valor inválido. Tente novamente.')
        return out
    
    def validarVoto(self, voto: Any) -> bool:
        try:
            if type(voto) is str:
                confirmacao: int = self.confirmaAcaoUser('Você está prestes a votar em branco. Confirma? (1 = Sim | 2 = Não)', [1, 2])
                if confirmacao == 1:
                    self._votos_brancos += 1
                    self._votos_totais += 1
                    print('Obrigado por votar.')
                    return True
                else:
                    print('Voto cancelado.')
                    return False
            elif type(voto) is int:
                candidato: Candidato = self.getCandidatoByDigito(voto)
                if not self.checkDigitoCadidato(voto):
                    raise CandidatoNotInListError()

                # TERMINAR ESSA PARTE
                confirmacao: int = self.confirmaAcaoUser(f'Você está prestes a votar no cadidato {candidato.nome}. Confirma? (1 = Sim | 2 = Não)', [1, 2])
                if confirmacao == 1:
                    candidato.votos += 1
                    self._votos_totais += 1
                    self._votos_validos += 1
                    print('Obrigado por votar.')
                    return True
                else:
                    print('Voto cancelado.')
                    return False

        except CandidatoNotInListError:
            print(f'Candidato com o digito {voto} não existe no sistema.')
            confirmacao: int = self.confirmaAcaoUser('Você está prestes a votar nulo. Confirma? (1 = Sim | 2 = Não)', [1, 2])
            if confirmacao == 1:
                self._votos_nulos += 1
                self._votos_totais += 1
                print('Voto anulado.')
                return True
            else:
                return False
        except ValueError:
            print('Erro no sistema. Você inseriu um caractére não-númerico?\n'
                + 'Cancelando tentativa de voto atual, tente novamente.')
            return False
    
    def encerramentoEleicao(self) -> bool:
        input_senha: int = getIntFromUser('Qual foi a senha decidida para essa eleição?')
        try:
            if input_senha != self.senha:
                raise SenhaInvalidaError()
        except SenhaInvalidaError:
            print('Senha inválida. Processo de eleição continuara até a senha certa for inserida.')
            return False
        else:
            if self._votos_totais == 0:
                acao: int = self.confirmaAcaoUser('Não há nenhum voto no sistema. Encerrar mesmo assim? (1 = Sim | 2 = Não)', [1, 2])
                if acao == 2:
                    print('Encerramento abordado.')
                    return False
            self._gerarEstatisticaVotos()
            self._decidir_ganhador()
            return True

    def _gerarEstatisticaVotos(self):
        try:
            print(f'Votos Totais: {self._votos_totais}\n'
                + f'Votos Validos: {self._votos_validos} ({(100*(self._votos_validos / self._votos_totais)):.1f}%)\n'
                + f'Votos Nulos: {self._votos_nulos} ({(100*(self._votos_nulos / self._votos_totais)):.1f}%)\n'
                + f'Votos Brancos: {self._votos_brancos} ({(100*(self._votos_brancos / self._votos_totais)):.1f}%)\n'
                )
        except ZeroDivisionError:
            print('Essa eleição teve 0 votos registrados.')

    def _decidir_ganhador(self):
        if self._votos_totais == 0:
            print('Como essa eleição teve 0 votos registrados, não há ganhador.')
        elif self._votos_validos == 0:
            print('Essa eleição teve 0 votos não nulos/brancos registrados. Logo, não há ganhador.')
        else:
            votodict: Dict[str, int] = {}
            for candidato in self.list_candidatos:
                print(f'Candidato: {candidato.nome}\n'
                    + f'Votos: {candidato.votos}\n\n'
                    )
                votodict.update({str(candidato.digito): candidato.votos})
            
            ganhador: Candidato = self.getCandidatoByDigito(int(max(votodict, key=votodict.get)))
            print(f'Ganhador desse eleição foi o candidato {ganhador.nome} com {ganhador.votos} votos!')

def main():
    senha: int = getIntFromUser('Qual será a senha usada para essa eleição?')
    
    candidatos_list: List[Candidato] = []

    while True:
        option: int = Urna.confirmaAcaoUser('Deseja cadastrar um candidato? (1 = Sim | 2 = Não)', [1, 2])
        try:
            if option == 2 and len(candidatos_list) < 3:
                raise NotEnoughCandidatosError()
            elif option == 2:
                break
            else:
                cand_nome: str = input('Qual é o nome do candidado?\n>>> ')
                if stringHasNumber(cand_nome) == True or stringHasSpecialChars(cand_nome) == True:
                    raise NomeCandidatoInvalido()
                elif len(cand_nome.strip()) <=0:
                    raise NomeCandidatoVazio()
                cand_digito: int = getIntFromUser('Qual é o digito do candidato?')
                candidatos_list.append(Candidato(cand_nome, cand_digito))
                print(f'Candidato {cand_nome} com digito {cand_digito} cadastrado.')

        except NotEnoughCandidatosError:
            print(f'Você ainda tem que cadastrar pelo menos mais {3 - len(candidatos_list)} candidato(s)')
        
        except ValueError:
            print('Erro no sistema. Você inseriu um caractére não-númerico?\n'
                + 'Tente novamente.')
        
        except NomeCandidatoInvalido:
            print('Erro no sistema. Nome do candidato tem caractéres inválidos.\n'
                + 'Tente novamente.')
        
        except NomeCandidatoVazio:
            print('Erro no sistema. Nome do candidato não pode ser vazio.\n'
                + 'Tente novamente.')
    
    eleicao: Urna = Urna(candidatos_list, senha)
    eleicao_acabou: bool = False
    while eleicao_acabou != True:
        acao: int = eleicao.confirmaAcaoUser('Liberar novo voto ou encerrar eleição? (1 = Novo Voto | 2 = Encerrar)', [1, 2])

        if acao == 2:
            eleicao_acabou = eleicao.encerramentoEleicao()
        elif acao == 1:
            isVotoValido: bool = False
            while isVotoValido != True:
                eleicao.showCandidatos()
                voto: int | str = input('Qual é o digito do seu canditado? (Escreva BRANCO para votar branco)\n>>> ')
                try:
                    voto = int(voto)
                except ValueError:
                    if voto != 'BRANCO':
                        print('Voto inválido. Tente novamente.')
                        isVotoValido = False
                    else:
                        isVotoValido = eleicao.validarVoto(voto)
                else:
                    isVotoValido = eleicao.validarVoto(voto)
    print('Eleições encerradas.')

if __name__ == "__main__":
    main()