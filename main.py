from tkinter import *
from PIL import ImageTk, Image

from poker.card import Card
from poker.card_deck import CardDeck
from poker.hand import Hand
from poker.player import Player
from poker.game_round import GameRound
from poker.ai import AI
from poker.human_player import Human, is_number
from time import sleep
from poker.images import get_file_names_from_directory
from poker.names import Names

import os


class PokerGUI:
    def __init__(self):
        self._root = Tk()
        dir_name = os.path.dirname(__file__)
        print(dir_name)
        self._root.iconbitmap(str(os.path.join(dir_name, 'card.ico')))
        self._root.title("Texas Holdem")
        self._frame = LabelFrame(self._root, padx=50, pady=50)
        self._frame.grid(row=0, column=0, padx=10, pady=10)
        self._answer = ""
        self._wait_for_responce = False
        self._players = []
        self._img_folder = os.path.join(dir_name, 'PNG')
        self.create_image_dictionary()
        self._card_back_Image = Image.open(str(os.path.join(self._img_folder, 'gray_back.png')))
        self._my_img = self.resize_image(self._card_back_Image)
        self._main()

    def create_image_dictionary(self):
        self._image_dic = {}
        for file in get_file_names_from_directory(self._img_folder):
            # print(file)
            self._image_dic.setdefault(file, self.resize_image(Image.open(os.path.join(self._img_folder, file))))

    def _main(self):
        self._quit_button()
        self._create_text_labels()
        self.show_text_labels_money()
        self.show_text_labels_hand()
        self._create_player_buttons()
        self.show_player_buttons()
        self._create_community_card_labels()
        self.show_community_cards_labels()
        self._create_player_card_labels()
        self.show_player_card_labels()
        self._create_bet_buttons()
        self.show_text_labels_info()
        self.show_text_labels_round()
        self.show_text_labels_game()
        self._root.mainloop()

    def stop(self):
        self._answer = "stop"
        self._wait_for_responce = False
        self._root.quit()
        exit()

    def _create_text_labels(self):
        self._game_label = Label(self._frame, text="Game: ")
        self._info_label = Label(self._frame, text=" ")
        self._winner_label = Label(self._frame, text="Winner: ")
        self._pot_label = Label(self._frame, text="Pot: 0")
        self._chips_label = Label(self._frame, text="Chips: 0")
        self._hand_label = Label(self._frame, text="Hand: ")
        self._bet_label = Label(self._frame, text="Active Bet: ")
        self._players_label = Label(self._frame, text="Active players: ")
        self._round_label = Label(self._frame, text="Round: ")

    def _create_money_slider(self, max_value):
        self.slider = Scale(self._frame, from_=1, to=max_value, orient=HORIZONTAL)
        self._button_bet_money = Button(self._frame, text="Bet", command=lambda: self._bet_money())

    def _create_player_buttons(self):
        self._button_2_player = Button(self._frame, text="2 Players", command=lambda: self._create_players(1))
        self._button_3_player = Button(self._frame, text="3 Players", command=lambda: self._create_players(2))
        self._button_4_player = Button(self._frame, text="4 Players", command=lambda: self._create_players(3))
        self._button_5_player = Button(self._frame, text="5 Players", command=lambda: self._create_players(4))

    def _create_bet_buttons(self):
        # call / raise / fold  # bet / check / fold # all in / fold
        self._button_bet = Button(self._frame, text="Bet", command=lambda: self._bet(1))
        self._button_check = Button(self._frame, text="Check", command=lambda: self._bet(2))
        self._button_raise = Button(self._frame, text="Raise", command=lambda: self._bet(3))
        self._button_fold = Button(self._frame, text="Fold", command=lambda: self._bet(4))
        self._button_call = Button(self._frame, text="Call", command=lambda: self._bet(5))
        self._button_all_in = Button(self._frame, text="All In", command=lambda: self._bet(6))

    def _create_community_card_labels(self):
        self._community_card_1 = Label(self._frame, image=self._my_img)
        self._community_card_2 = Label(self._frame, image=self._my_img)
        self._community_card_3 = Label(self._frame, image=self._my_img)
        self._community_card_4 = Label(self._frame, image=self._my_img)
        self._community_card_5 = Label(self._frame, image=self._my_img)

    def _create_player_card_labels(self):
        self._player_card_1 = Label(self._frame, image=self._my_img)
        self._player_card_2 = Label(self._frame, image=self._my_img)

    def _quit_button(self):
        self._button_quit = Button(self._frame, text="Exit", command=lambda: self.stop())
        self._button_quit.grid(row=0, column=5)

    def show_text_labels_money(self):
        self._chips_label.grid(row=0, column=1)
        self._pot_label.grid(row=1, column=3)

    def show_text_labels_players(self):
        self._players_label.grid(row=2, column=0, columnspan=6)

    def show_text_labels_game(self):
        self._game_label.grid(row=3, column=3)

    def show_text_labels_round(self):
        self._round_label.grid(row=4, column=3)

    def show_text_labels_winner(self):
        self._winner_label.grid(row=5, column=0, columnspan=6)

    def show_text_labels_info(self):
        self._info_label.grid(row=7, column=0, columnspan=6)

    def show_player_buttons(self):
        self._button_2_player.grid(row=10, column=1)
        self._button_3_player.grid(row=10, column=2)
        self._button_4_player.grid(row=10, column=3)
        self._button_5_player.grid(row=10, column=4)

    def show_community_cards_labels(self):
        self._community_card_1.grid(row=15, column=1)
        self._community_card_2.grid(row=15, column=2)
        self._community_card_3.grid(row=15, column=3)
        self._community_card_4.grid(row=15, column=4)
        self._community_card_5.grid(row=15, column=5)
        self._root.update()

    def show_text_labels_bet(self):
        self._bet_label.grid(row=20, column=4)

    def show_player_card_labels(self):
        self._player_card_1.grid(row=20, column=1, rowspan=5)
        self._player_card_2.grid(row=20, column=2, rowspan=5)
        self._root.update()

    def show_text_labels_hand(self):
        self._hand_label.grid(row=21, column=4)

    def _show_money_slider(self):
        self.slider.grid(row=22, column=3, columnspan=3)
        self._button_bet_money.grid(row=22, column=5)

    # call / raise / fold
    def show_call_raise_fold_buttons(self):
        self._button_call.grid(row=22, column=3)
        self._button_raise.grid(row=22, column=4)
        self._button_fold.grid(row=22, column=5)
        self._root.update()

    # all in / fold
    def show_all_in_fold_buttons(self):
        self._button_all_in.grid(row=22, column=3)
        self._button_fold.grid(row=22, column=5)
        self._root.update()

    # check / bet /  fold
    def show_check_bet_fold_buttons(self):
        self._button_check.grid(row=22, column=3)
        self._button_bet.grid(row=22, column=4)
        self._button_fold.grid(row=22, column=5)
        self._root.update()

    def update_text_labels_players(self, label_text):
        # self.show_text_labels_game()
        names = ",".join([player.name for player in label_text])
        players = f"Active Players: {names}"
        self._players_label.config(text=players)
        self._root.update()
        # self.hide_text_labels_game()

    def update_text_labels_game(self, label_text):
        # self.show_text_labels_game()
        game = f"Game: {label_text}"
        self._game_label.config(text=game)
        self._root.update()
        # self.hide_text_labels_game()

    def update_text_labels_round(self, label_text):
        # self.show_text_labels_round()
        game_round = f"Round: {label_text}"
        self._round_label.config(text=game_round)
        self._root.update()
        # self.hide_text_labels_round()

    def update_text_labels_winner(self, label_text):
        self.show_text_labels_winner()
        winner = f"Winner: {label_text}"
        self._winner_label.config(text=winner)
        self._root.update()
        sleep(5)  # update with button
        self.hide_text_label_winner()

    def update_text_labels_pot(self, label_text):
        pot = f"Pot: {label_text}"
        self._pot_label.config(text=pot)
        self._root.update()

    def update_text_labels_chips(self, label_text):
        chips = f"Chips: {label_text}"
        self._chips_label.config(text=chips)
        self._root.update()

    def update_text_labels_hand(self, label_text):
        hand = f"Hand: {label_text}"
        self._hand_label.config(text=hand)
        self._root.update()

    def update_text_labels_bet(self, label_text):
        self.show_text_labels_bet()
        bet = f"Active Bet: {label_text}"
        self._bet_label.config(text=bet)
        self._root.update()

    def update_text_labels_info(self, label_text):
        self._info_label.config(text=label_text)
        self._root.update()

    def destroy_money_slider(self):
        self.slider.destroy()
        self._button_bet_money.destroy()
        self._root.update()

    def hide_text_labels_info(self):
        self._info_label.grid_forget()

    def hide_text_labels_game(self):
        self._game_label.grid_forget()

    def hide_text_labels_round(self):
        self._round_label.grid_forget()

    def hide_player_buttons(self):
        self._button_2_player.grid_forget()
        self._button_3_player.grid_forget()
        self._button_4_player.grid_forget()
        self._button_5_player.grid_forget()
        self._root.update()

    # call / raise / fold
    def hide_call_raise_fold_buttons(self):
        self._button_call.grid_forget()
        self._button_raise.grid_forget()
        self._button_fold.grid_forget()
        self._root.update()

    # all in / fold
    def hide_all_in_fold_buttons(self):
        self._button_all_in.grid_forget()
        self._button_fold.grid_forget()
        self._root.update()

    # check / bet /  fold
    def hide_check_bet_fold_buttons(self):
        self._button_check.grid_forget()
        self._button_bet.grid_forget()
        self._button_fold.grid_forget()
        self._root.update()

    def hide_call_all_in_fold_buttons(self):
        self._button_fold.grid_forget()
        self._button_all_in.grid_forget()
        self._root.update()

    def hide_community_cards(self):
        self._community_card_1.grid_forget()
        self._community_card_2.grid_forget()
        self._community_card_3.grid_forget()
        self._community_card_4.grid_forget()
        self._community_card_5.grid_forget()
        self._root.update()

    def hide_player_card_labels(self):
        self._player_card_1.grid_forget()
        self._player_card_2.grid_forget()
        self._root.update()

    def hide_text_label_winner(self):
        self._winner_label.grid_forget()
        self._root.update()

    def hide_text_label_bet(self):
        self._bet_label.grid_forget()
        self._root.update()

    def _bet(self, answer):
        self._answer = str(answer)
        self._wait_for_responce = False
        return

    def check(self):
        self._wait_for_responce = True
        self.show_check_bet_fold_buttons()
        self._root.update()
        while self._wait_for_responce:
            self._root.update()
            # sleep(.1)
        self.hide_check_bet_fold_buttons()
        return self._answer

    def bet(self):
        self._wait_for_responce = True
        self.show_call_raise_fold_buttons()
        self._root.update()
        while self._wait_for_responce:
            self._root.update()
            # sleep(.1)
        self.hide_call_raise_fold_buttons()
        return self._answer

    def make_a_bet(self, chips):
        self._wait_for_responce = True
        self._create_money_slider(chips)
        self._show_money_slider()
        while self._wait_for_responce:
            self._root.update()
            # sleep(.1)
        return self._answer

    def all_in(self, chips):
        self._wait_for_responce = True
        self.show_all_in_fold_buttons()
        while self._wait_for_responce:
            self._root.update()
            # sleep(.1)
        self.hide_call_all_in_fold_buttons()
        return self._answer

    def _bet_money(self):
        self._answer = str(self.slider.get())
        self.destroy_money_slider()
        self._wait_for_responce = False
        return

    def _create_players(self, number):
        names = Names()
        self.hide_player_buttons()
        self._root.update()
        deck = CardDeck()
        cards = Card.create_cards()
        deck.add_cards(cards)
        hand = Hand()
        player = Player(f"Player", hand)
        self._players.append(player)
        human = Human(player=player, gui=self)
        for i in range(number):
            hand = Hand()
            # player = Player(f"Opponent {i + 1}", hand)
            player = Player(names.get_random_name(), hand)
            self._players.append(player)
            ai = AI(player=player)
        self.hide_player_buttons()
        for player in self._players:
            player.add_chips(60)
        game = GameRound(players=self._players, deck=deck, gui=self)
        # game.set_game_qty(game_qty=10)
        game.set_game_qty(infinite=True)
        game.play()
        self.stop()

    def change_card_image(self, card, image_name):
        img = self._image_dic[image_name]
        print(image_name)
        if card == "C1":
            self._community_card_1.config(image=img)
        elif card == "C2":
            self._community_card_2.config(image=img)
        elif card == "C3":
            self._community_card_3.config(image=img)
        elif card == "C4":
            self._community_card_4.config(image=img)
        elif card == "C5":
            self._community_card_5.config(image=img)
        elif card == "P1":
            self._player_card_1.config(image=img)
        elif card == "P2":
            self._player_card_2.config(image=img)
        self._root.update()

    def resize_image(self, img):
        # (691, 1056)
        resized = img.resize((86, 132), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(resized, master=self._frame)
        return pic


main = PokerGUI()
