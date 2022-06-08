from simple_term_menu import TerminalMenu
import os
import time

class Screen:
    SUIT_SYMBOLS = {'C': '♣', 'D': '♦', 'S': '♠', 'H': '♥'}
    SUIT_COLORS = {'C': '\u001b[32m', 'D': '\u001b[34m', 'S': '\u001b[35m', 'H': '\u001b[31m'}

    def __init__(self, game = None):
        self.game = game

    @staticmethod
    def clear(splash=False):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')
        if splash:
            Screen.show_splash()

    @staticmethod
    def play_intro():
        splash_lines = [
            "        _     _                              _             ",
            " __   _(_) __| | ___  ___        _ __  _   _| | _____ _ __ ",
            " \ \ / / |/ _` |/ _ \/ _ \ _____| '_ \| | | | |/ / _ \ '__|",
            "  \ V /| | (_| |  __/ (_) |_____| |_) | |_| |   <  __/ |   ",
            "   \_/ |_|\__,_|\___|\___/      | .__/ \__, |_|\_\___|_|   ",
            "                                |_|    |___/                         "
        ]
        print("")
        for line in splash_lines:
            print(line)
            time.sleep(0.4)
        time.sleep(0.6)

    @staticmethod
    def show_splash():
        print('''
        _     _                              _             
 __   _(_) __| | ___  ___        _ __  _   _| | _____ _ __ 
 \ \ / / |/ _` |/ _ \/ _ \ _____| '_ \| | | | |/ / _ \ '__|
  \ V /| | (_| |  __/ (_) |_____| |_) | |_| |   <  __/ |   
   \_/ |_|\__,_|\___|\___/      | .__/ \__, |_|\_\___|_|   
                                |_|    |___/                         
        ''')

    @staticmethod
    def pretty_card(card):
        return f'{Screen.SUIT_COLORS[card.suit]}{card.value}{Screen.SUIT_SYMBOLS[card.suit]}\u001b[0m'
        
    def show_balance(self):
        print(f'\n\u001b[33mBalance: {self.game.balance}\u001b[0m')

    def show_cards(self):
        for card in self.game.hand.cards:
            print(Screen.pretty_card(card), end='  ')

    def show_predeal(self):
        print('\nYour cards are:')
        self.show_cards()
        print(f'\n\u001b[36m{self.game.hand.name}\u001b[0m')
    
    def show_final_cards(self):
        print('\nYour final cards are...\n')
        self.show_cards()
        print(f'\n\u001b[36m{self.game.hand.name}\u001b[0m')

    def show_wager(self):
        print(f'\n\u001b[33mWager: {self.game.current_bet}\u001b[0m')

    def get_cards_held_indices(self):
        options = [str(c) for c in self.game.hand.cards]
        terminal_menu = TerminalMenu(options, multi_select=True, multi_select_select_on_accept=False, multi_select_empty_ok=True)
        print('\nChoose which cards to hold:')
        menu_entry_indices = terminal_menu.show()
        if menu_entry_indices is None:
            return []
        return list(menu_entry_indices)
    
    def get_main_menu_option(self):
        options = ['[n]New Game', '[p]Payouts', '[x]Exit']
        terminal_menu = TerminalMenu(options)
        print('\nWelcome to the casino!')
        choice_index = terminal_menu.show()
        return choice_index
    
    def get_gameover_option(self):
        print("\n\u001b[31mOh no! You're broke...\n \u001b[0m")
        options = ['[m]Main Menu', '[x]Exit']
        terminal_menu = TerminalMenu(options)
        choice_index = terminal_menu.show()
        return choice_index

    def get_player_bet(self):
        print('\nHow much would you like to wager:')
        return input('>> ')
    
    def show_payout(self, payout):
        if not payout:
            print(f'\n\u001b[31mUnlucky... no payout\u001b[0m')
            return
        print(f'\n\u001b[33mYou won {payout}\u001b[0m')

    def show_payouts(self):
        print("{:<15} {:<15}".format('HAND', 'MULTIPLIER'))

        for k, v in self.game.PAYOUTS.items():
            name = k.replace('_', ' ').title().strip()
            multiplier = f'{v}x'
            if name == 'Pair':
                name += ' (JJ+)'
            print("{:<15} {:<15}".format(name, multiplier))


