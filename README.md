# Desafio Unbox Culture

O desafio consiste em uma simulação de um banco imobiliário simplificado,
composta por 4 jogadores com perfis únicos.


## Visão Geral

Cada jogador começa com saldo de 300, podendo ganhar dinheiro com o recebimento
de aluguéis de seus imóveis e por uma volta total no tabuleiro.

Para gastar-se dinheiro o jogador pode comprar uma casa, desde de que não possua
dono e tenha-se dinheiro suficiente para a compra, ou cair em uma propriedade 
que possua inquilino, neste caso ele deva pagar o valor do aluguel.

O jogo inicia-se com o embaralhamento da ordem dos jogadores.
Cada jogador começa jogando o dado, que possui 6 faces, e move as casas de
acordo com o valor retornado pelo dado. Estando em uma casa o jogador pode
efetuar duas ações: compra ou pagamento de aluguel, como explicado acima.

A cada novo início de rodada somente os que tiverem saldo positivo continuam
jogando. Quando somente um restar, este é declarado campeão. Caso ao início
da rodada todos os jogadores estejam com saldo negativo, é declarado campeão
o primeiro na ordem de jogo.

Outra forma de se vencer, é o jogo passar de 1000 rodadas. Neste caso, o que
tiver mais dinheiro é declarado campeão.

## Perfil dos Jogadores

Cada jogador possuía uma peculiaridade que altera o seu comportamento na hora
da compra de propriedades:
- O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
- O jogador exigente compra qualquer propriedade, desde que o valor do aluguel
   dela seja maior do que 50.
- O jogador cauteloso compra qualquer propriedade desde que ele tenha uma 
reserva de 80 saldo sobrando depois de realizada a compra.
- O jogador aleatório compra a propriedade que ele parar em cima com 
probabilidade de 50%.

## Resultado

Como resultado da execução do programa, são ditas estas 4 informações:

- Quantas partidas terminam por time out (1000 rodadas);
- Quantos turnos em média demora uma partida;
- Qual a porcentagem de vitórias por comportamento dos jogadores;
- Qual o comportamento que mais vence.

Essas informações são agregadas de acordo com 300 simulações de jogos.

Um exemplo de saída:
```
Média de turnos: 21

Quantidade de timeouts: 1

Porcentagem de vitórias por comportamento dos jogadores:
Impulsive: 22.6%
Demanding: 24.6%
Cautious: 26.8%
Random: 26.0%

Melhor jogador: Cautious
```

## Informações Técnicas

O programa requer Python 3.6+ para sua execução.

Para rodar bastar chamar ``python3 main.py``.

