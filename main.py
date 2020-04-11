from random import randrange, shuffle, randint
import operator


class Dice(object):
    _faces: int = 0

    def __init__(self, faces: int = 6):
        self._faces = faces

    def row(self) -> int:
        """
        Lança o dado e retorna um valor entre 0 e _faces
        :return: int
        """
        return randrange(0, self._faces)


class Player(object):
    _name: str = ""
    _manner: str = ""
    _money: float = 300  # Os jogadores sempre começam uma partida com saldo de 300
    _position: int = 0

    def __init__(self, name: str, manner: str):
        self._name = name
        self._manner = manner

    def __repr__(self) -> str:
        return f"<{self._name} - {self._manner}>"

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, position: int) -> None:
        self._position = position

    @property
    def money(self) -> float:
        return self._money

    @property
    def manner(self) -> str:
        return self._manner

    def should_buy(self, price: float) -> bool:
        if self._manner == 'impulsive':
            # O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
            return True
        elif self._manner == 'demanding':
            # O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
            return bool(price > 50)
        elif self._manner == 'cautious':
            """
            O jogador cauteloso compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando
            depois de realizada a compra.
            """
            return bool(self._money - price > 80)
        elif self._manner == 'random':
            # O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50%.
            return bool(randint(0, 1))

    def receive(self, amount: float) -> None:
        self._money += amount

    def pay(self, amount: float) -> None:
        self._money -= amount


class Property(object):
    """
    Cada propriedade tem um custo de
    venda, um valor de aluguel, um proprietário caso já estejam compradas, e seguem uma determinada ordem no
    tabuleiro.
    """
    _name: str = "None"
    _price: float = 0
    _rent: float = 0
    _owner: Player = None

    def __init__(self, name: str):
        self._name = name
        self._price = randrange(1, 100)
        self._rent = randrange(1, 50)

    def __repr__(self):
        return f"<{self._name} - {self._owner}>"

    def has_owner(self) -> bool:
        return bool(self._owner)

    @property
    def price(self) -> float:
        return self._price

    @property
    def rent(self) -> float:
        return self._rent

    @property
    def owner(self) -> Player:
        return self._owner

    @owner.setter
    def owner(self, owner: Player) -> None:
        self._owner = owner


class Board(object):
    _sequence: int = 0
    _properties: list = []

    def __init__(self, sequence: int = 20):
        self._sequence = sequence

        for index in range(0, sequence):
            #  o tabuleiro é composto por 20 propriedades em sequência
            self._properties.append(Property(f"Property_{index}"))

    def get_property(self, position: int) -> Property:
        return self._properties[position]

    def get_player_properties(self, player: Player) -> list:
        return list(filter(lambda building: building.owner == player, self._properties))

    def move_player(self, player: Player, moves: int) -> None:
        position = player.position + moves

        if position > self._sequence:
            position = position % self._sequence
            player.receive(100)  # Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo

        player.position = position

        building = self.get_property(position - 1)
        if building.has_owner():
            """
            Ao cair em uma propriedade que tem proprietário, ele deve pagar ao proprietário o valor do aluguel da
            propriedade
            """
            player.pay(building.rent)
            building.owner.receive(building.rent)
        else:
            """
            Ao cair em uma propriedade sem proprietário, o jogador pode escolher entre comprar ou não a
            propriedade. Esse é a única forma pela qual uma propriedade pode ser comprada
            """
            if player.should_buy(building.price):
                if building.price <= player.money:
                    """
                    Jogadores só podem comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro 
                    da venda
                    """

                    # Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.
                    player.pay(building.price)
                    building.owner = player


class Game(object):
    _turns = 0
    _winner = Player
    _players_order = []
    _board = None

    def __init__(self):
        dice = Dice()
        self._board = Board()

        player1 = Player("player1", "impulsive")
        player2 = Player("player2", "demanding")
        player3 = Player("player3", "cautious")
        player4 = Player("player4", "random")

        self._players_order = [player1, player2, player3, player4]
        self._shuffle_players_order()

        while True:
            self._turns += 1
            players = []

            for player in self._players_order:
                if player.money >= 0:
                    players.append(player)
                else:
                    """
                    Um jogador que fica com saldo negativo perde o jogo, e não joga mais. 
                    Perde suas propriedades e portanto podem ser compradas por qualquer outro jogador.
                    """
                    buildings = self._board.get_player_properties(player)
                    for building in buildings:
                        building.owner = None

            for player in players:
                moves = dice.row()  # o jogador joga um dado equiprovável de 6 faces
                self._board.move_player(player, moves)

            if len(players) == 1:
                """
                Termina quando restar somente um jogador com saldo positivo, a qualquer momento da partida. Esse jogador
                é declarado o vencedor
                """
                self._winner = players[0]
                break
            elif len(players) < 1:
                # O critério de desempate é a ordem de turno dos jogadores nesta partida.
                self._winner = self._players_order[0]
                break

            if self._turns >= 1000:
                """
                Caso o jogo demore muito, como é de costume em jogos dessa natureza, o jogo termina na milésima rodada
                com a vitória do jogador com mais saldo.
                """
                players.sort(key=lambda x: x.money, reverse=True)
                self._winner = players[0]

                # O critério de desempate é a ordem de turno dos jogadores nesta partida.
                if players[0].money == players[1].money:
                    self._winner = self._players_order[0]
                break

    def _shuffle_players_order(self) -> None:
        """
        Numa partida desse jogo, os jogadores se alteram em rodadas, numa ordem definida
        aleatoriamente no começo da partida.
        """
        shuffle(self._players_order)

    @property
    def winner(self) -> Player:
        return self._winner

    @property
    def summary(self) -> dict:
        return {
            'turns': self._turns,
            'timeout': bool(self._turns == 1000),
            'winner': self._winner.manner,
        }


if __name__ == '__main__':
    turns = 0
    timeout = 0
    winners = {
        'impulsive': 0,
        'demanding': 0,
        'cautious': 0,
        'random': 0
    }
    rounds = 500
    for i in range(0, rounds):
        game = Game()
        turns += game.summary.get('turns')
        timeout += 1 if game.summary.get('timeout') is True else 0
        winners[game.summary['winner']] += 1

    print(f"Média de turnos: {int(turns / rounds)}")  # Quantos turnos em média demora uma partida;
    print()
    print(f"Quantidade de timeouts: {timeout}")  # Quantas partidas terminam por time out (1000 rodadas)
    print()

    # Qual a porcentagem de vitórias por comportamento dos jogadores
    print("Porcentagem de vitórias por comportamento dos jogadores:")
    for winner, total in winners.items():
        print(f"{winner.capitalize()}: {round((total / rounds) * 100, 2)}%")
    print()

    # Qual o comportamento que mais vence.
    print(f"Melhor jogador: {max(winners.items(), key=operator.itemgetter(1))[0].capitalize()}")
