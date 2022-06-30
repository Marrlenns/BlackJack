import random

class Player:
    def __init__(self, name):
        self.name = name
        self.bet = None
        self.point = 0
        self.cards = []
        self.win = 1
        self.is_double = 0

    def hit(self):
        pass

    def stand(self):
        pass

    def split(self):
        pass

    def double(self):
        pass

    def surrender(self):
        pass

calculator = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10,
            'A': [1, 11],
}

def calc_point(a, b):
    point  = 0
    if a == 'A':
        point += 11
        if b == 'A':
            point += 1
        else:
            point += calculator[b]
    elif b == 'A':
        point += 11
        if a == 'A':
            point += 1
        else:
            point += calculator[a]
    else:
        point  = calculator[a] + calculator[b]
    return point

class Diller:

    def __init__(self, deck, players):
        self.deck = deck
        self.players = players

    def dd(self):
        self.players.append(Player('Дилер'))
        diller = self.players[len(self.players) - 1]
        diller.cards.append(self.deck[0])
        diller.cards.append(self.deck[1])
        diller.point = calc_point(self.deck[0], self.deck[1])
        print(f"Карты Дилера: {self.deck[0]}-?")
        if diller.point == 21:
            print(f"Карты Дилера: {self.deck[0]}-{self.deck[1]}")
            self.deck.pop(0)
            self.deck.pop(0)
            return 1
        self.deck.pop(0)
        self.deck.pop(0)





class Deck:

    def __init__(self, quantity):
        self.quantity = quantity
        self.deck = ['A', 'K', 'Q', 'J', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.sh_deck = []
        for i in range(self.quantity):
            self.sh_deck += self.deck

    def get_decks(self):
        return self.sh_deck

    def get_shuffled_deck(self):
        random.shuffle(self.sh_deck)
        return self.sh_deck

class BlackJack(Diller):
    pass

class Game:
    def play(self):
        deck_num = int(input("Определите количетсво колод: "))
        deck = Deck(deck_num).get_shuffled_deck()
        players_num = int(input("Определите количество игроков: "))
        players = []
        for i in range(players_num):
            name = input(f"Введите имя {i + 1} игрока: ").title()
            players.append(Player(name))
        # print(players[0].name)
        for player in players:
            bet = int(input(f"{player.name}, сделайте ставку: "))
            player.bet = bet

        for player in players:
            print(f"{player.name}: {deck[0]}-{deck[1]}")
            player.cards.append(deck[0])
            player.cards.append(deck[1])
            if deck[0] == 'A':
                player.point += 11
                if deck[1] == 'A':
                    player.point += 1
                else:
                    player.point += calculator[deck[1]]
            elif deck[1] == 'A':
                player.point += 11
                if deck[0] == 'A':
                    player.point += 1
                else:
                    player.point += calculator[deck[0]]
            else:
                player.point += calculator[deck[0]] + calculator[deck[1]]

            deck.pop(0)
            deck.pop(0)

        buffer = Diller(deck, players).dd()

        if buffer:
            for player in players:
                if player.point != 21:
                    print(f"{player.name} проиграл партию, так как у Дилера 'BlackJack'\nДилер получает ставку: {player.bet}$")
                else:
                    print(f"{player.name} получил свою ставку {players.bet}$")
            return

        for player in players:
            print()
            cmd = ''
            flag, cnt = 0, 0
            if player.name == 'Дилер':
                break
            while cmd != '2':
                cmd = input(f"{player.name} - количество ваших очков: {player.point}\nСделайте ход:\n\t1 - Hit\n\t2 - Stand\n\t3 - Split\n\t4 - Double\n\t5 - Surrender\n")
                if cmd == '1':
                    a = calculator[deck[0]]
                    if deck[0] == 'A':
                        player.point += 1
                        if player.point + 10 <= 21:
                            player.point += 10
                    else:
                        player.point += a
                    print(f"Ваша новая карта: {deck[0]}, общая сумма: {player.point}")
                    if player.point > 21:
                        print(f"{player.name} покидает игру")
                        player.win = 0
                        break
                    player.cards.append(deck[0])
                    deck.pop(0)
                    if flag == 1:
                        break
                elif cmd == '2':
                    print(f"{player.name} - количество ваших очков: {player.point}")
                elif cmd == '3' and not cnt:
                    if player.cards[0] == player.cards[1] and player.cards[0] != 'A':
                        cnt = 1
                        print(f"Ставка удвоена!")
                        player.cards[0] = [player.cards[0], deck[0]]
                        player.cards[1] = [player.cards[1], deck[1]]
                        player.bet = [player.bet, player.bet]
                        player.point = [player.point // 2 + calculator[deck[0]], player.point // 2 + calculator[deck[1]]]

                        deck.pop(0)
                        deck.pop(0)
                    else:
                        print("Вы не можете пользоваться командой Split")

                elif cmd == '4' and not cnt:
                    if len(player.cards) == 2:
                        print(f"{player.name}, ваша ставка удвоена!!!")
                        player.bet *= 2
                        flag = 1
                    else:
                        print("double эс ал")

                elif cmd == '5':
                    print(f"Дилер получил половину вашей ставки - {round(player.bet / 2, 1)}$.\n{player.name} покидает игру!")
                    player.win = 0
                    break
        d = len(players) - 1
        print(players[d].point, '\n')
        for i in range(len(players)):
            if players[i].name == 'Дилер':
                break
            print()
            if players[i].point < players[d].point or not players[i].win:
                print(f"{players[i].name} проиграл партию!\nДилер получает вашу ставку: {players[i].bet}$")
            elif players[i].point == players[d].point:
                print(f"{players[i].name} получил свою ставку - {players[i].bet}$")
            else:
                if len(players[i].cards) == 2 and calc_point(players[i].cards[0], players[i].cards[1]) == 21:
                    print(f"{players[i].name} выиграл ставку 3/2  -  {players[i].bet * 1.5}$")
                else:
                    print(f"{players[i].name} выиграл свою ставку - {players[i].bet}$")


# print(calculator['A'] + calculator['10'])
Game().play()


