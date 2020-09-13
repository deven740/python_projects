from random import shuffle


class Deck:
    # list of all suits
    suits = 'H D C S'.split()

    # ranks of all cards
    ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

    # Create a deck of cards
    @staticmethod
    def create_deck():
        full_deck = []
        for suit in Deck.suits:
            for rank in Deck.ranks:
                full_deck.append((rank, suit))

        # Shuffle the deck
        shuffle(full_deck)

        return full_deck

    # Creating 4 hands for 4 players
    def create_hands(self):

        full_deck = self.create_deck()

        stack_1 = full_deck[:13]
        stack_2 = full_deck[13:26]
        stack_3 = full_deck[26:39]
        stack_4 = full_deck[39:]

        return stack_1, stack_2, stack_3, stack_4


class Game:
    # Creating class variables
    is_trump_set = False
    trump_card = None
    table_cards = []
    player_cards = {}

    def __init__(self, player_1, player_2, player_3, player_4):
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4

        # Creating team_1 of player 1 and 3
        self.team_1 = [self.player_1, self.player_3]

        # Creating dictionary of mendi & hand for team_1
        self.team_1_score = {'mendi': 0, 'hands': 0}

        # Creating team_1 of player 2 and 4
        self.team_2 = [self.player_2, self.player_4]

        # Creating dictionary of mendi & hand for team_2
        self.team_2_score = {'mendi': 0, 'hands': 0}

    # Deciding winner for each round
    def round_winner(self, player_card_info):

        # Dictionary to store player points
        player_points = {}

        # Deciding winner after Trump card is set
        if self.is_trump_set:

            # Creating a dictionary with weight for cards to calculate highest card per round
            weight_of_cards = dict.fromkeys(Deck.suits, 0)
            for card in weight_of_cards:

                # If cards is a trump card set its weight to 200
                if self.trump_card == card:
                    weight_of_cards[card] = 200

            # If card is played first set its weight to 100
            for position in player_card_info.values():
                if position[1] == 1:
                    weight_of_cards[position[0][1]] += 100

            # Calculating the points received for each player according to their card
            for player_, played_card in player_card_info.items():
                # Adding the weight of ranked card to the according to their position
                player_points[player_.name] = weight_of_cards[played_card[0][1]] + Deck.ranks.index(played_card[0][0])

        # Deciding winner if trump card is not set
        else:
            for player_, played_card in player_card_info.items():
                player_points[player_.name] = Deck.ranks.index(played_card[0][0])

        # Saving player name inside a variable
        winner = max(player_points, key=player_points.get)
        print('==============================')
        print(f'{winner} is the winner')
        print('==============================')
        print()

        print('=================  Next Round  =================')
        print()

        # Calculating the number of mendis and hand collected after every round
        mendi_count = 0
        for player_ in player_card_info:
            if player_.name == winner:
                if player_ in self.team_1:
                    # print(f'{player_.name} is in Team1')

                    for card in self.table_cards:
                        if card[0] == '10':
                            mendi_count += 1

                    self.team_1_score['mendi'] += mendi_count
                    self.team_1_score['hands'] += 1
                else:
                    # print(f'{player_.name} is in Team2')

                    for card in self.table_cards:
                        if card[0] == '10':
                            mendi_count += 1

                    self.team_2_score['mendi'] += mendi_count
                    self.team_2_score['hands'] += 1
                return player_

    # Function to set Trump card
    def set_trump(self, trump_card):
        self.trump_card = trump_card
        self.is_trump_set = True

    # Function to display Trump Card
    def show_trump_card(self):
        print(self.trump_card)

    def show_player_cards(self):
        pass

    # Declaring the final winner after completing the completing game
    def declare_winner(self):
        # If both teams have same number of mendis, team with more hands is the winner
        if self.team_1_score['mendi'] == self.team_2_score['mendi']:
            if self.team_1_score['hands'] > self.team_2_score['hands']:
                print('Team 1 Wins')
            else:
                print('Team 2 Wins')

        # If team_1 has more mendis than team_2 declare team_1 as winner
        elif self.team_1_score['mendi'] > self.team_1_score['mendi']:

            # If mendis = 4 declare as mendi coat
            if self.team_1_score['mendi'] == 4:
                print('Team 1 wins wth a Mendi Cot')
            else:
                print('Team 1 wins')

        # If team_2 has more mendis than team_1 declare team_2 as winner
        else:
            if self.team_2_score['mendi'] == 4:
                print('Team 2 wins wth a Mendi Cot')
            else:
                print('Team 2 wins')


class Player:

    def __init__(self, cards, name):
        self.cards = cards
        self.name = name

    # Creating a dictionary of cards and their index to display the cards in hand
    def show_cards(self):
        cards_dict = {index: card for card, index in zip(self.cards, range(1, len(self.cards) + 1))}
        return cards_dict

    # Allowing player to choose the card he wants to play & return the card he played
    def select_card(self, keys_list):
        while True:
            try:
                choice = int(input(f'{self.name} - Choose the card yor want to play: '))
                print()

                if choice in keys_list:
                    selected_card = self.cards.pop(choice - 1)
                    print(f'{self.name} has played the {selected_card} card')
                    print()
                    return selected_card
                else:
                    print('Please select the correct option')
            except ValueError:
                print('Please select the correct option')
                pass

    def return_played_card(self, keys_list, current_game):
        played_card = self.select_card(keys_list)
        current_game.player_cards[self.name] = played_card
        return played_card

    # Function to allow the player to play the card
    def play_card(self, current_game, start_round):

        # Checking if it is the start of round
        if start_round:
            print('=============================================================')
            print(f'Its {self.name}\'s turn  Displaying {self.name}\'s cards  Trump card is {current_game.trump_card}')
            print('=============================================================')
            print()
            cards_list = self.show_cards()

            keys_list = []

            # If it is the start of round show player all the cards in his hand
            for key, values in cards_list.items():
                keys_list.append(key)
                print(key, ':', values)
            print()

            # Remove the card  selected by the player from hand
            return self.return_played_card(keys_list, current_game)
        else:
            print('=============================================================')
            print(f'Its {self.name}\'s turn  Displaying {self.name}\'s cards  Trump card is {current_game.trump_card}')
            print('=============================================================')
            print()
            print('Cards on Table are: ', current_game.player_cards)
            print()
            cards_list = self.show_cards()

            keys_list = []

            # Checking if the player has card which was played  at the start of round
            count = 0
            for key, values in cards_list.items():
                if values[1] == current_game.table_cards[0][1]:
                    keys_list.append(key)
                    print(key, ':', values)
                    count += 1
            print()

            # If the player does not have the card played at the start of round
            if count == 0:
                # Scenario 1 - If trump card is set and the player does not have the card played at start of the round
                if current_game.is_trump_set:

                    keys_list = []

                    # Displaying all the cards in the players hands
                    for key, values in cards_list.items():
                        keys_list.append(key)
                        print(key, ':', values)
                    print()
                    print('==============================')
                    print()

                    # Remove the card selected by the player
                    return self.return_played_card(keys_list, current_game)

                else:
                    # Scenario 2 - If trump card is not set and the player does not have the card
                    #              played at start of the round
                    print('Set Trump Card')
                    print()

                    # Creating empty dictionary with suits as keys and cards in each suit as list
                    suit_cards = {}

                    # Creating a empty list of cards for each suit
                    for cards in cards_list.values():
                        suit_cards[cards[1]] = []

                    # Adding cards for each suit in the list
                    for cards in cards_list.values():
                        suit_cards[cards[1]].append(cards[0])

                    # Showing the player the cards in his hand
                    print(suit_cards)
                    print()

                    # Asking the player to set Trump card
                    while True:
                        try:
                            choice = input(f'{self.name} - Select the Trump card: ')

                            if choice.upper() in suit_cards.keys():
                                # Calling method to Set user choice as Trump card
                                current_game.set_trump(choice.upper())

                                # Displaying the selected Trump card
                                print(current_game.trump_card, ' is the Trump card')
                                print()
                                break
                            else:
                                print('Please select the correct option')
                        except ValueError:
                            print('Please select the correct option')
                            pass

                    keys_list = []

                    # Displaying all the trump cards to the player
                    for key, values in cards_list.items():
                        if values[1] == current_game.trump_card:
                            keys_list.append(key)
                            print(key, ':', values)
                    print()

                    # Remove the card  selected by the player from hand
                    return self.return_played_card(keys_list, current_game)

            else:
                # Remove the card  selected by the player from hand
                return self.return_played_card(keys_list, current_game)


# Creating instance to Deck class
deck = Deck()

# Calling method to create 4 hands for 4 players
hand_1, hand_2, hand_3, hand_4 = deck.create_hands()

# Sorting the player hand according to his cards
hand_1 = sorted(hand_1, key=lambda x: x[1])
hand_2 = sorted(hand_2, key=lambda x: x[1])
hand_3 = sorted(hand_3, key=lambda x: x[1])
hand_4 = sorted(hand_4, key=lambda x: x[1])

# Creating our players
A = Player(hand_1, 'Deven')
B = Player(hand_2, 'Ashwin')
C = Player(hand_3, 'Pawan')
D = Player(hand_4, 'Suraj')

# Starting our game
game = Game(A, B, C, D)

# Default Turn list for players
player_turn_list = [A, B, C, D]

# Loop to check if hand is not empty
while len(A.show_cards()) != 0:

    # Checking if it the start of round
    is_first_round = True

    # Playing cards according to player_list
    for player in player_turn_list:
        card_played_by_player = player.play_card(start_round=is_first_round, current_game=game)

        # Adding the cards to list to display the cards played by the players
        game.table_cards.append(card_played_by_player)

        # Setting first_round to False after the round has started
        is_first_round = False

    # Creating a dictionary of player information and card played by the player
    players_card_info_dict = {player: [card, position] for player, card, position in
                              zip(player_turn_list, game.table_cards, range(1, len(game.table_cards) + 1))}

    # Declaring the round winner according to the player cards
    round_winner = game.round_winner(players_card_info_dict)

    # Clearing the table_cards list before new round
    game.table_cards.clear()
    game.player_cards.clear()

    # Changing the player turn list according to who won the last round
    temp_player_turn_list1 = player_turn_list[player_turn_list.index(round_winner):]
    temp_player_turn_list2 = player_turn_list[:player_turn_list.index(round_winner)]
    temp_player_turn_list1.extend(temp_player_turn_list2)
    player_turn_list = temp_player_turn_list1.copy()

# Print scores for both teams
print(f'Team 1 has {game.team_1_score["mendi"]} mendi\'s and {game.team_1_score["hands"]} hands')
print(f'Team 2 has {game.team_2_score["mendi"]} mendi\'s and {game.team_2_score["hands"]} hands')
print()

# Declaring the winner
game.declare_winner()
