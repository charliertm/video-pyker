import colorama
from .game import Game
from .screen import Screen

def new_game(screen):
    game = Game()
    screen.game = game
    while game.balance > 0:
        valid_wager = False
        while not valid_wager:
            screen.clear(splash=True)
            screen.show_balance()
            wager_input = screen.get_player_bet()
            try:
                wager = int(wager_input)
            except ValueError:
                continue
            if not (0 < wager <= game.balance):
                continue
            valid_wager = True
            game.place_bet(wager)
        screen.clear(splash=True)
        screen.show_wager()
        game.deal(new_deck=True)
        screen.show_predeal()
        held_cards_indices = screen.get_cards_held_indices()
        game.redeal(held_cards_indices)
        screen.clear(splash=True)
        screen.show_final_cards()
        payout = game.payout_player()
        screen.show_payout(payout)
        input()
    screen.clear(splash=True)
    option_index = screen.get_gameover_option()
    match option_index:
        case 0:
            main_menu(skip_intro=True)
        case 1:
            exit()

def show_payouts(screen):
    screen.clear(splash=True)
    screen.show_payouts()
    input()
    main_menu(skip_intro=True)

def main_menu(skip_intro=False):
    game = Game()
    screen = Screen(game)
    screen.clear()
    if skip_intro:
        screen.clear(splash=True)
    else:
        screen.play_intro()
    option_index = screen.get_main_menu_option()
    match option_index:
        case 0:
            new_game(screen)
        case 1:
            show_payouts(screen)
        case 2:
            exit()

def main():
    colorama.init()
    main_menu()
    
if __name__ == '__main__':
    main()