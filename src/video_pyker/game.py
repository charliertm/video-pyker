import itertools
import random

class Card:
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['C', 'D', 'S', 'H']
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __repr__(self):
        return f'{self.value}{self.suit}'

    def __gt__(self, other):
        return Card.VALUES.index(self.value) > Card.VALUES.index(other.value)
    
    def __lt__(self, other):
        return Card.VALUES.index(self.value) < Card.VALUES.index(other.value)

class Hand:
    @classmethod
    @property
    def RANKS(cls):
        return {
            'high_card': cls.get_high_card,
            'pair': cls.get_pair,
            'two_pair': cls.get_two_pair,
            'toak': cls.get_toak,
            'straight': cls.get_straight,
            'flush': cls.get_flush,
            'full_house': cls.get_full_house,
            'foak': cls.get_foak,
            'straight_flush': cls.get_straight_flush,
            'royal_flush': cls.get_royal_flush,
        }
    
    @property
    def name(self):
        best_hand_name, best_hand = self.get_best_hand()
        match best_hand_name:
            case 'high_card':
                return f'High card {best_hand[0][0].value}'
            case 'pair':
                return f'Pair of {best_hand[0][0].value}s'
            case 'two_pair':
                return f'Two Pair, {best_hand[0][0].value}s and {best_hand[1][0].value}s'
            case 'toak':
                return f'Three {best_hand[0][0].value}s'
            case 'straight':
                return f'Straight {best_hand[0][0]} to {best_hand[0][-1]}'
            case 'flush':
                return f'{best_hand[0][0].suit} flush'
            case 'full_house':
                toak_val = self.get_toak()[0][0].value
                pair_val = self.get_pair()[0][0].value
                return f'Full House {toak_val}s full of {pair_val}s'
            case 'foak':
                return f'Four {best_hand[0][0].value}s'
            case 'straight_flush':
                return f'Straight Flush {best_hand[0][0]} to {best_hand[0][-1]}'
            case 'royal_flush':
                return f'Royal Flush'
    
    @property
    def jacks_or_better(self):
        best_hand_name, best_hand = self.get_best_hand()
        if best_hand_name == 'pair':
            # suit is aribitrary here
            return best_hand[0][0] > Card('10', 'C')
        return False

    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return ' '.join([c for c in self.cards])

    def get_equal_combos(self, n):
        '''internal function for finding p, 2p, toak, foak'''
        combintaions = itertools.combinations(self.cards, n)
        equal_combos = []
        for combo in combintaions:
            # check that all values are equal
            if not len(set([c.value for c in combo])) == 1:
                continue
            # check we havent already added this combo
            if sorted(combo, key=lambda c: c.suit) in equal_combos:
                continue
            equal_combos.append(combo)
        return equal_combos

    def get_pairs(self):
        if self.get_equal_combos(4):
            return []
        toak = self.get_equal_combos(3)
        if toak:
            remaining_pair = [c for c in self.cards if c not in toak[0]]
            if remaining_pair[0].value == remaining_pair[1].value:
                return [(remaining_pair[0], remaining_pair[1])]
        pairs = self.get_equal_combos(2)
        if pairs:
            return pairs
        return []

    def get_high_card(self):
        return [(sorted(self.cards)[-1], )]

    def get_pair(self):
        pairs = self.get_pairs()
        if len(pairs) == 1:
            return pairs
        return []
    
    def get_two_pair(self):
        pairs = self.get_pairs()
        if len(pairs) == 2:
            return pairs
        return []
    
    def get_toak(self):
        if self.get_equal_combos(4):
            return []
        return self.get_equal_combos(3)
    
    def get_foak(self):
        return self.get_equal_combos(4)

    def get_full_house(self):
        if self.get_pair() and self.get_toak():
            return [tuple(self.cards)]
        return []

    def get_flush(self):
        if len(set([c.suit for c in self.cards])) == 1:
            return [tuple(self.cards)]
        return []

    def get_straight(self):
        sorted_values = [c.value for c in sorted(self.cards)]
        for i in range(len(Card.VALUES) - 4):
            if sorted_values == Card.VALUES[i:i+5]:
                return [tuple(sorted(self.cards))]
        if sorted_values == [ '2', '3', '4', '5', 'A']:
            return [tuple(sorted(self.cards)[-1:] + sorted(self.cards)[:-1])]
        return []
    
    def get_straight_flush(self):
        if not self.get_flush():
            return []
        straight = self.get_straight()
        if straight:
            return straight
        return []

    def get_royal_flush(self):
        straight_flush = self.get_straight_flush()
        if not straight_flush:
            return []
        sorted_values = [c.value for c in sorted(self.cards)]
        if sorted_values == ['10', 'J', 'Q', 'K', 'A']:
            return [tuple(sorted(self.cards))]
        return []

    def get_best_hand(self):
        for name, rank_fn in reversed(Hand.RANKS.items()):
            hand = rank_fn(self)
            if hand:
                return name, hand

class Game:
    STARTING_BALANCE = 100
    PAYOUTS = {
        'high_card': 0,
        'pair': 1,
        'two_pair': 2,
        'toak': 3,
        'straight': 4,
        'flush': 5,
        'full_house': 7,
        'foak': 25,
        'straight_flush': 50,
        'royal_flush': 250
        
    }

    def __init__(self):
        self.balance = Game.STARTING_BALANCE
        self.current_bet = None
        self.deck = [Card(v, s) for v in Card.VALUES for s in Card.SUITS]
    
    def deal(self, new_deck=False):
        if new_deck:
            self.deck = [Card(v, s) for v in Card.VALUES for s in Card.SUITS]
        random.shuffle(self.deck)
        self.hand = Hand([self.deck.pop() for _ in range(5)])

    def redeal(self, held_indicies):
        self.hand.cards = [c for i, c in enumerate(self.hand.cards) if i in held_indicies]
        for _ in range(5 - len(held_indicies)):
            self.hand.cards.append(self.deck.pop())

    def place_bet(self, bet):
        self.balance -= bet
        self.current_bet = bet

    def payout_player(self):
        best_hand_name = self.hand.get_best_hand()[0]
        multiplier = Game.PAYOUTS[best_hand_name]
        # only payout jacks or better
        if best_hand_name == 'pair':
            multiplier = 1 if self.hand.jacks_or_better else 0
        payout = self.current_bet * multiplier
        self.balance += payout
        return payout