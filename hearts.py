"""
Tommy Aitchison & Oswin Shin
Hearts Game
11-17-23 - skeleton classes with generic methods
11-20-23 - basic gui
11-21-23 - pass cards feature, human-play_card feature
11-22-23 - computer-controlled play_card feature
11-23-23 - next hand, end game functionalitycd
11-24-23 - implemented (buggy) single game save functionality
11-25-23 - fixed save/load bugs, implemented trick images
11-27-23 - fixed duplicate card in trick and hand bug
11-29-23 - fixed double click bug, show points this hand
11-30-23 - fixed showing wrong cards on game load bug
11-31-23 - added scoreboard
12-1-23 - implemented stack_cards method
12-2-23 - implemented EndGame window
12-4-23 - bug fixes

Funcions without a painfully obvious purpose have a comment noting purpose

Note about tests: We have extensively tested logic functions through playing the game (rigging it so edge cases occur)
Testing every UI possibility is much harder and there are very likely more bugs that cause UI and backend to not
match up (which would still break the game) You would probably have to play the game for a long time to find them though.

Things we could add if we have more time:
    better error messages if you are breaking the rules (playing a card you can't play)
    better cpu logic (endless rabit hole)
    make it look better
    bug test better
"""
import pickle
from enum import Enum
from random import shuffle
import sys
import os
from PySide6 import QtTest
from PySide6.QtCore import QSize, Qt, QItemSelectionModel, QAbstractTableModel
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QListWidget,
    QListView,
    QListWidgetItem,
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QTableView,
    QHeaderView,
    QWidget,
)
from PySide6.QtGui import (
    QFont,
    QPixmap,
    QTransform,
    QIcon,
    QImage,
    QColor,
    QPainter,
)
basedir = os.path.dirname(__file__)

class Suit(Enum):
    HEARTS = 0
    SPADES = 1
    DIAMONDS = 2
    CLUBS = 3


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class PlayerType(Enum):
    HUMAN = 0
    AI = 1


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hearts")
        self.setFixedSize(750, 720)
        self.setStyleSheet("QMainWindow { background-color: green;}")

        # making New game and rules buttons
        self.title = QLabel("Hearts")
        font = QFont()
        font.setPointSize(50)
        self.title.setFont(font)
        self.title.setStyleSheet("font-family: 'Times New Roman';")

        self.play_game = QPushButton()
        self.play_game.setText("Play Game")
        self.play_game.setFixedSize(300, 100)
        self.play_game.clicked.connect(self.play_game_listener)
        self.play_game.setStyleSheet("font-family: 'Times New Roman';")

        self.rules = QPushButton()
        self.rules.setText("Hearts Rules")
        self.rules.setFixedSize(300, 100)
        self.rules.setStyleSheet("font-family: 'Times New Roman';")
        self.rules.clicked.connect(self.rules_listener)

        self.menuButtonsLayout = QVBoxLayout()
        self.menuButtonsLayout.addWidget(self.title)
        self.menuButtonsLayout.addWidget(self.play_game)
        self.menuButtonsLayout.addWidget(self.rules)
        self.menuButtonsLayout.setAlignment(Qt.AlignCenter)
        self.title.setAlignment(Qt.AlignCenter)

        centralWidget = QWidget()
        centralWidget.setLayout(self.menuButtonsLayout)
        self.setCentralWidget(centralWidget)

    def play_game_listener(self):
        self.hide()
        self.game_window = MainWindow()
        self.game_window.show()

    def rules_listener(self):
        self.hide()
        self.rules = RulesWindow()
        self.rules.show()


class RulesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hearts Rules")
        self.setFixedSize(750, 720)
        self.setStyleSheet("QMainWindow { background-color: green;}")

        self.main_menu = QPushButton()
        self.main_menu.setText("Main Menu")
        self.main_menu.clicked.connect(self.main_menu_listener)
        self.main_menu.setStyleSheet("font-family: 'Times New Roman';")
        self.rules_title = QLabel("Rules")
        self.description = QLabel(
            "Here are the simplified rules of hearts. More details can be found online."
        )
        rule_title_font = QFont()
        rule_title_font.setPointSize(72)
        self.rules_title.setFont(rule_title_font)
        rules_description_font = QFont()
        rules_description_font.setPointSize(15)
        self.description.setFont(rules_description_font)
        self.rules_text = QLabel(
            "<b>Objective</b>: Avoid taking cards with hearts and the Queen of Spades.<br><br>"
            "<b>Deal</b>: Each player is dealt 13 cards.<br><br>"
            "<b>Passing</b>: Before each round, pass three cards to an opponent.<br><br>"
            "<b>Trick-taking</b>: Play a card; the highest card of the lead suit wins the trick.<br><br>"
            "<b>Breaking Hearts</b>: Hearts cannot be played in the first round; after that, they can be played.<br><br>"
            "<b>Scoring</b>: Hearts are worth 1 point each, and the Queen of Spades is worth 13 points.<br><br>"
            "<b>Winning</b>: The player with the fewest points at the end wins."
        )
        self.rules_text.setTextFormat(Qt.RichText)

        text_font = QFont()
        text_font.setPointSize(15)
        self.rules_text.setFont(text_font)
        self.rules_title.setStyleSheet(
            "font-family: 'Times New Roman'; font-weight: bold;"
        )
        self.description.setStyleSheet(
            "font-family: 'Times New Roman'; font-weight: bold;"
        )
        self.description.setMargin(50)
        self.rules_text.setStyleSheet("font-family: 'Times New Roman';")
        rules_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        title_layout.addStretch()
        title_layout.addWidget(self.main_menu)
        rules_layout.addLayout(title_layout)
        rules_layout.addWidget(self.rules_title)
        rules_layout.addWidget(self.description)
        rules_layout.addWidget(self.rules_text)
        self.rules_title.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        rules_layout.setAlignment(Qt.AlignCenter)
        rules_layout.addStretch()

        # Using empty QLabels to create a space between selected widgets.
        # self.rules_title.setAlignment(Qt.AlignCenter)

        centralWidget = QWidget()
        centralWidget.setLayout(rules_layout)
        self.setCentralWidget(centralWidget)

    def main_menu_listener(self):
        self.hide()
        menu.show()


class TableModel(QAbstractTableModel):
    # for EndWindow scoreboard
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data[1:]
        self.HHeaders = data[0]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # sets custom headers
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HHeaders[section]
        elif (
            orientation == Qt.Vertical
            and role == Qt.DisplayRole
            and section + 1 == len(self._data)
        ):
            return "Total"
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class EndWindow(QMainWindow):
    # appears on game end or you click scoreboard
    def __init__(self, scores, winner=None, winner_i=None):
        super().__init__()
        self.winner = winner
        self.setWindowTitle("Game Review")
        self.setFixedSize(750, 720)
        self.setStyleSheet("QMainWindow { background-color: green;}")

        self.title = (
            QLabel(f"{winner} Win!") if winner == "You" else QLabel(f"{winner} Wins!")
        )
        font = QFont()
        font.setPointSize(50)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black")
        self.main_menu = QPushButton()
        self.main_menu.setText("Main Menu")
        self.main_menu.clicked.connect(self.main_menu_listener)
        self.new_game = QPushButton()
        self.new_game.setText("New Game")
        self.new_game.clicked.connect(self.new_game_listener)
        self.scoreboard = QTableView()
        self.scoreboard.setModel(TableModel(scores))
        if winner_i:
            self.scoreboard.selectColumn(winner_i)
        self.scoreboard.setSelectionMode(QAbstractItemView.NoSelection)
        self.scoreboard.setFixedWidth(435)
        self.back_to_game = QPushButton()
        self.back_to_game.setText("Back To Game")
        self.back_to_game.clicked.connect(self.back)

        VTRLayout = QVBoxLayout()
        HTLayout = QHBoxLayout()
        HMLayout = QHBoxLayout()
        BigLayout = QVBoxLayout()

        VTRLayout.addWidget(self.main_menu)
        VTRLayout.addWidget(self.new_game)
        HTLayout.addStretch()
        HTLayout.addLayout(VTRLayout)
        HMLayout.addStretch()
        HMLayout.addWidget(self.scoreboard)
        HMLayout.addStretch()
        BigLayout.addLayout(HTLayout)
        if winner:
            BigLayout.addWidget(self.title)
        else:
            VTRLayout.addWidget(self.back_to_game)
        BigLayout.addLayout(HMLayout)
        BigLayout.addStretch()

        centralWidget = QWidget()
        centralWidget.setLayout(BigLayout)
        self.setCentralWidget(centralWidget)

    def back(self):
        # back to current game (if it's not over)
        menu.game_window.cur_game.scores.pop()
        menu.game_window.show()
        self.hide()

    def main_menu_listener(self):
        if not self.winner:
            self.save_confirm()
        self.hide()
        menu.show()

    def new_game_listener(self):
        if not self.winner:
            self.save_confirm()
        self.game_window = MainWindow()
        self.game_window.show()
        self.hide()

    def save_confirm(self):
        if not menu.game_window.thinking:
            confirm = QMessageBox.question(
                self,
                "Save Game?",
                "Would you like to save this game? (last save game will be overwriten)",
            )
            if confirm == QMessageBox.Yes:
                menu.game_window.cur_game.save()
                return True
        else:
            confirm = QMessageBox.information(
                self,
                "Error!",
                "Please wait for opponents to complete their turn.",
            )
            return False


class MyHand(QListWidget):
    # for your hand of cards
    def __init__(self, parent=None, max_selected=3):
        super().__init__(parent)
        self.max_selected = max_selected

    def selectionCommand(self, index, event):
        # only allows selection of 3 cards to pass
        if len(self.selectedItems()) >= self.max_selected:
            return QItemSelectionModel.Deselect
        else:
            return super().selectionCommand(index, event)


# so objects in MyHand listwidget can be customized
CustomObjectRole = Qt.UserRole + 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QMainWindow { background-color: green;}")
        self.setWindowTitle("Hearts")
        self.setFixedSize(QSize(1100, 850))

        self.initGame()
        self.inst = QLabel()
        self.inst.setAlignment(Qt.AlignCenter)
        self.inst.setStyleSheet("font-family: 'Times New Roman';")
        self.card_back = QImage(os.path.join(basedir, "card_pngs", "back08.svg"))
        self.card_back = self.card_back.scaledToWidth(100)

        self.rotate90 = QTransform()
        self.rotate90.rotate(90)
        self.rotate180 = QTransform()
        self.rotate180.rotate(180)
        self.rotate270 = QTransform()
        self.rotate270.rotate(270)

        self.scoreboard = QTableWidget(2, 4, self)
        self.scoreboard.verticalHeader().setVisible(False)
        self.scoreboard.horizontalHeader().setVisible(False)
        self.scoreboard.setHorizontalHeaderLabels("ScoreBoard")
        self.scoreboard.setFixedHeight(60)
        self.scoreboard.setFixedWidth(65 * 4)
        self.scoreboard.setSelectionMode(QAbstractItemView.NoSelection)
        self.scoreboard.cellClicked.connect(self.inspect_scoreboard)
        self.scoreboard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scoreboard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scoreboard.setStyleSheet("font-family: 'Times New Roman';")
        self.thinking = False
        self.update_scoreboard()
        self.scoreboard.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clear = QPixmap(100, 145)
        self.clear.fill(Qt.transparent)
        self.P0card = QLabel()
        self.P1card = QLabel()
        self.P2card = QLabel()
        self.P3card = QLabel()
        self.hand_0 = MyHand()
        self.hand_0.setFixedHeight(100)
        self.hand_0.setViewMode(QListView.IconMode)
        self.hand_0.setIconSize(QSize(90, 90))
        self.hand_0_points = QLabel()
        self.hand_0_points.setStyleSheet("font-family: 'Times New Roman';")
        self.hand_0_points.setText(f"Points this hand: 0")
        self.hand_0_points.setAlignment(Qt.AlignCenter)
        self.hand_1 = QLabel()
        self.hand_1_name = QLabel()
        self.hand_1_name.setText(f"{self.cur_game.players[1].name}")
        self.hand_2 = QLabel()
        self.hand_2_name = QLabel()
        self.hand_2_name.setText(f"{self.cur_game.players[2].name}")
        self.hand_2.setAlignment(Qt.AlignCenter)
        self.hand_2_name.setAlignment(Qt.AlignCenter)
        self.hand_3 = QLabel()
        self.hand_3_name = QLabel()
        self.hand_3_name.setText(f"{self.cur_game.players[3].name}")
        self.load_button = QPushButton()
        self.load_button.setText("Load")
        self.load_button.clicked.connect(self.load_listener)
        self.load_button.setStyleSheet("font-family: 'Times New Roman';")
        self.save_button = QPushButton()
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save_confirm)
        self.save_button.setStyleSheet("font-family: 'Times New Roman';")
        self.pass_button = QPushButton()
        self.pass_button.setVisible(False)
        self.pass_button.setText("Pass Cards")
        self.pass_button.setStyleSheet("font-family: 'Times New Roman';")
        self.pass_button.clicked.connect(self.pass_cards)
        self.hand_0.itemClicked.connect(self.get_selection)
        self.main_menu = QPushButton()
        self.main_menu.setText("Main Menu")
        self.main_menu.clicked.connect(self.main_menu_listener)
        self.main_menu.setStyleSheet("font-family: 'Times New Roman';")
        self.new_game()
        self.trick_labels = [self.P0card, self.P1card, self.P2card, self.P3card]
        for label in self.trick_labels:
            label.setPixmap(self.clear)
        for player in range(1, 4):
            self.stack_cards(player)

        bigLayout = QVBoxLayout()
        HLayout = QHBoxLayout()
        HTLayout = QHBoxLayout()
        VTRLayout = QVBoxLayout()
        MLayout = QVBoxLayout()
        TrickLayout = QHBoxLayout()
        MVLayout = QVBoxLayout()
        PLayout = QHBoxLayout()

        #         end = QPushButton()
        #         end.clicked.connect(self.end_game)
        #         VTRLayout.addWidget(end)
        VTRLayout.addWidget(self.main_menu)
        VTRLayout.addWidget(self.load_button)
        VTRLayout.addWidget(self.save_button)
        HTLayout.addWidget(self.scoreboard)
        HTLayout.addStretch()
        HTLayout.addLayout(VTRLayout)
        HLayout.setAlignment(Qt.AlignCenter)
        HLayout.addWidget(self.hand_1)
        HLayout.addWidget(self.hand_1_name)
        HLayout.addStretch()
        TrickLayout.addWidget(self.P1card)
        TrickLayout.addLayout(MLayout)
        MLayout.addWidget(self.P2card)
        MLayout.addWidget(self.P0card)
        TrickLayout.addWidget(self.P3card)
        PLayout.addStretch()
        PLayout.addWidget(self.pass_button)
        PLayout.addStretch()
        MVLayout.addLayout(TrickLayout)
        MVLayout.addWidget(self.inst)
        MVLayout.addWidget(self.hand_0_points)
        MVLayout.addLayout(PLayout)
        HLayout.addLayout(MVLayout)
        HLayout.addStretch()
        HLayout.addWidget(self.hand_3_name)
        HLayout.addWidget(self.hand_3)
        bigLayout.addLayout(HTLayout)
        bigLayout.setAlignment(Qt.AlignCenter)
        bigLayout.addWidget(self.hand_2_name)
        bigLayout.addWidget(self.hand_2)
        bigLayout.addLayout(HLayout)

        bigLayout.addWidget(self.hand_0)
        bigLayout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(bigLayout)

        self.setCentralWidget(central_widget)
        self.show_hand(self.cur_game.players[0])

    def closeEvent(self, event):
        if self.save_confirm():
            event.accept()
        else:
            event.ignore()

    def main_menu_listener(self):
        self.save_confirm()
        self.hide()
        menu.show()

    def save_confirm(self):
        if self.thinking:
            error = QMessageBox.information(
                self,
                "Error!",
                "Please wait for opponents to complete their turn.",
            )
            return False
        else:
            confirm = QMessageBox.question(
                self,
                "Save Game?",
                "Would you like to save this game? (last save game will be overwriten)",
            )
            if confirm == QMessageBox.Yes:
                self.cur_game.save()
            return True
        
    def inspect_scoreboard(self):
        # opens EndWindow for better scoreboard
        self.cur_game.scores.append(self.get_totals())
        self.score_window = EndWindow(self.cur_game.scores)
        self.score_window.show()
        self.hide()

    def update_scoreboard(self):
        for i in range(0, 4):
            self.scoreboard.setItem(
                0, i, QTableWidgetItem(f"{self.cur_game.players[i]}")
            )
            #             print(self.get_totals())
            self.scoreboard.setItem(1, i, QTableWidgetItem(f"{self.get_totals()[i]}"))

    def stack_cards(self, player):
        # renders and displays image of the number of cards in a cpu's hand using base image
        label = getattr(self, f"hand_{player}")
        count = len(self.cur_game.players[player].hand)
        # below code resizes image based on number of cards
        #         stackImageSize = QSize(
        #             self.card_back.width() + self.card_back.width() * (count - 1) * 0.25,
        #             self.card_back.height(),
        #         )
        stackImageSize = QSize(
            self.card_back.width() + self.card_back.width() * (12) * 0.25,
            self.card_back.height(),
        )
        stack = QImage(stackImageSize, QImage.Format.Format_ARGB32)
        stack.fill(QColor(0, 0, 0, 0))

        painter = QPainter()
        painter.begin(stack)
        for i in range(count):
            painter.drawImage(i * 25, 0, self.card_back)
        painter.end()
        if player == 1:
            stack = stack.transformed(self.rotate90)
        elif player == 2:
            stack = stack.transformed(self.rotate180)
        elif player == 3:
            stack = stack.transformed(self.rotate270)
        label.setPixmap(QPixmap.fromImage(stack))

    def initGame(self, load=False):
        # creates new game instance or loads existing one
        if load == True:
            self.clear_cards()
            self.cur_game = HeartsGame.load()
            self.show_hand(self.cur_game.players[0])
            self.update_scoreboard()
            for i in range(1, 4):
                self.stack_cards(i)
            if self.cur_game.trick:
                for i, card in enumerate(self.cur_game.trick):
                    self.display_pixmap(card, (i + self.cur_game.took_last_hand) % 4)
        else:
            self.cur_game = HeartsGame()

    def show_hand(self, player):
        # updates MyHand listwidget with current cards in hand
        self.hand_0.clear()
        for card in player.hand:
            it = QListWidgetItem()
            it.setIcon(QIcon(os.path.join(basedir, "card_pngs", card.get_image())))
            self.hand_0.addItem(it)
            it.setData(CustomObjectRole, card)

    def load_listener(self):
        confirm = QMessageBox.question(
            self,
            "Load Game?",
            "Would you like to load your saved game? (Current game will be lost)",
        )

        if confirm == QMessageBox.Yes:
            self.initGame(True)
            if self.cur_game.passed:
                self.pass_button.setVisible(False)
                self.hand_0.setSelectionMode(QAbstractItemView.SingleSelection)
                self.inst.setText("Select a card to play")
            else:
                self.pass_button.setVisible(True)
                self.hand_0.setSelectionMode(QAbstractItemView.MultiSelection)
                self.inst.setText(
                    f"Select 3 cards to pass to {str(self.cur_game.players[self.cur_game.calc_swap(0)])}"
                )

    def new_game(self):
        # starts new hand (basically soft reset of cur_game)
        self.cur_game.make_deck()
        self.cur_game.deal_hands()
        self.cur_game.players[0].sort_hand()
        self.cur_game.shot_the_moon = False
        self.cur_game.hearts_broken = False
        self.cur_game.queen_played = False
        self.cur_game.turn = False
        self.cur_game.round_counter = 1
        self.cur_game.took_last_hand = None
        self.cur_game.trick = []
        self.cur_game.passed = False
        for player in range(1, 4):
            self.stack_cards(player)
        self.show_hand(self.cur_game.players[0])

        if self.cur_game.hand_counter % 4 != 0:
            self.hand_0.setSelectionMode(QAbstractItemView.MultiSelection)
            self.pass_button.setVisible(True)
            self.inst.setText(
                f"Select 3 cards to pass to {str(self.cur_game.players[self.cur_game.calc_swap(0)])}"
            )
        else:
            self.cur_game.passed = True
            self.cur_game.took_last_hand = [
                i
                for i in range(4)
                if HeartsCard(Suit.CLUBS, Rank.TWO).in_(self.cur_game.players[i].hand)
            ][0]
            self.round_loop(self.cur_game.took_last_hand)

    def pass_cards(self):
        # passes cards from and to each player
        picked_cards = self.hand_0.selectedItems()
        if len(picked_cards) == 3:
            swap_list = [[card.data(CustomObjectRole) for card in picked_cards]] + [
                player.choose_pass_cards() for player in self.cur_game.players[1:]
            ]
            for i in range(4):
                self.cur_game.swap(
                    swap_list[i],
                    self.cur_game.players[i],
                    self.cur_game.players[self.cur_game.calc_swap(i)],
                )
            self.hand_0.setSelectionMode(QAbstractItemView.SingleSelection)
            self.cur_game.players[0].sort_hand()
            self.show_hand(self.cur_game.players[0])
            self.pass_button.setVisible(False)
            self.cur_game.took_last_hand = [
                i
                for i in range(4)
                if HeartsCard(Suit.CLUBS, Rank.TWO).in_(self.cur_game.players[i].hand)
            ][0]
            self.cur_game.passed = True
            self.round_loop(self.cur_game.took_last_hand)
        else:
            self.inst.setText(f"Select {3 - len(picked_cards)} more card(s)")

    def display_pixmap(self, card, player):
        # shows card image in trick once it is played
        label = getattr(self, f"P{player}card")
        p = QPixmap(os.path.join(basedir, "card_pngs", card.get_image()))
        p = p.scaledToWidth(100)
        label.setPixmap(p)
        QtTest.QTest.qWait(500)

    def round_loop(self, offset_i, start=0, end=4):
        # each of four players take their turn.
        # stops to wait for your card selection on your turn before being called again so remaining players can play
        self.thinking = True
        for i in range(start, end):
            player = self.cur_game.players[(i + offset_i) % 4]
            if (i + offset_i) % 4 == 0:
                self.cur_game.turn = True
                self.inst.setText("Select a card to play")
                self.cur_game.resume_info = [(i + offset_i + 1) % 4, 4 - i]
                self.thinking = False
                return
            else:
                card = player.choose_play_card()
                player.play_card(card)
                self.stack_cards((i + offset_i) % 4)
                self.display_pixmap(card, (i + offset_i) % 4)
                if card.suit == Suit.HEARTS:
                    self.cur_game.hearts_broken = True
                elif card.in_(["queen of spades"]):
                    self.cur_game.queen_played = True
        #             print(self.cur_game.trick)
        self.end_round()
        self.thinking = False

    def end_round(self):
        # updates ui
        # sets variables
        # starts next round if all cards are not played
        winner = self.cur_game.score_round()
        if winner != self.cur_game.players[0]:
            label = getattr(self, f'hand_{self.cur_game.players.index(winner)}_name')
            style = label.styleSheet()
            label.setStyleSheet("color: 'red';")
            QtTest.QTest.qWait(500)
            label.setStyleSheet(style)
        else:
            QtTest.QTest.qWait(500)
        for label in self.trick_labels:
            label.setPixmap(self.clear)
        self.cur_game.round_counter += 1
        self.hand_0_points.setText(
            f"Points this hand: {self.cur_game.players[0].points_this_hand(False)}"
        )
        self.cur_game.trick = []
        self.cur_game.resume_info = None
        if self.cur_game.round_counter == 14:
            self.end_hand()
        else:
            self.cur_game.took_last_hand = self.cur_game.players.index(winner)
            self.round_loop(self.cur_game.took_last_hand)

    def clear_cards(self):
        # sets clear placeholder cards in the trick so nothing in the ui moves
        for label in self.trick_labels:
            label.setPixmap(self.clear)

    def end_hand(self):
        # scores this hand and checks if game is over. Otherwise, starts a new hand.
        self.clear_cards()
        shot_the_moon_player = [
            player
            for player in self.cur_game.players
            if player.points_this_hand(False) == 26
        ]
        if shot_the_moon_player:
            self.cur_game.shot_the_moon = True
            for player in self.cur_game.players:
                if player is shot_the_moon_player[0]:
                    player.points -= 26
                else:
                    player.points += 26
        self.hand_0_points.setText(f"Points this hand: 0")
        # print([player.points_this_hand(False) for player in self.cur_game.players])

        self.cur_game.scores.append(
            [
                player.points_this_hand(self.cur_game.shot_the_moon)
                for player in self.cur_game.players
            ]
        )
        self.update_scoreboard()
        point_list = [player.points for player in self.cur_game.players]
        if (
            max(point_list) >= 100
            and len([small for small in point_list if small == min(point_list)]) == 1
        ):
            self.end_game(point_list.index(min(point_list)))
        else:
            self.cur_game.hand_counter += 1

            for player in self.cur_game.players:
                player.taken = []
            self.new_game()

    def end_game(self, winner):
        # opens EndWindow on game end
        self.cur_game.finishes += 1
        self.cur_game.scores.append(self.get_totals())
        self.end_window = EndWindow(
            self.cur_game.scores, self.cur_game.players[winner].name, winner
        )
        self.end_window.show()
        self.hide()
        self.inst.setText(
            f"{min(self.cur_game.players, key=lambda player: player.points)} Wins!"
        )

    # we got rid of these hand len labels since you can see it visually with stack_cards
    #     def update_labels(self):
    #         self.hand_1_label.setText(f"{len(self.cur_game.players[1].hand)}")
    #         self.hand_2_label.setText(f"{len(self.cur_game.players[2].hand)}")
    #         self.hand_3_label.setText(f"{len(self.cur_game.players[3].hand)}")
    def get_totals(self):
        # returns list of each player's total points
        return [
            sum(
                (
                    score
                    for score in [
                        [round_score[i] for round_score in self.cur_game.scores[1:]]
                        for i in range(4)
                    ][j]
                )
            )
            for j in range(4)
        ]

    def get_selection(self):
        # validates and plays your selected card, updates ui, re-enters round_loop
        if self.cur_game.turn:
            card = self.hand_0.currentItem().data(CustomObjectRole)
            if self.cur_game.players[0].can_play_card(card):
                self.cur_game.turn = False
                self.cur_game.players[0].play_card(card)
                self.show_hand(self.cur_game.players[0])
                self.display_pixmap(card, 0)
                self.round_loop(
                    0, self.cur_game.resume_info[0], self.cur_game.resume_info[1]
                )

            else:
                self.inst.setText("That card cannot be played!")


class HeartsCard:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank.name.lower()} of {self.suit.name.lower()}"

    def __repr__(self) -> str:
        return f"HeartsCard({self.suit}, {self.rank})"

    def score_value(self):
        if self.suit == Suit.HEARTS:
            return 1
        elif self.suit == Suit.SPADES and self.rank == Rank.QUEEN:
            return 13
        else:
            return 0

    def get_image(self):
        # return filename for self
        return f"{self.rank.value if self.rank.value < 11 else self.rank.name.lower()}_of_{self.suit.name.lower()}.png"

    def in_(self, group):
        # basically overrides __contains__ but for object being contained since cards can be in more than one other object type

        return str(self) in [str(card) for card in group]

    def __gt__(self, other):
        return self.rank.value > other.rank.value

    def __lt__(self, other):
        return self.rank.value < other.rank.value
    def __eq__(self, other):
        return repr(self) == repr(other)

    def high_card(cards, suit=None):
        return max(
            cards if not suit else HeartsCard.cards_of_suit(cards, suit),
            key=lambda card: card.rank.value,
            default=None,
        )

    def low_card(cards, suit=None):
        return min(
            cards if not suit else HeartsCard.cards_of_suit(cards, suit),
            key=lambda card: card.rank.value,
            default=None,
        )

    def winning(self, trick):
        #         print(self > max(
        #             HeartsCard.cards_of_suit(trick, trick[0].suit) + [self]
        #         ))
        #         print(self)
        cards = HeartsCard.cards_of_suit(trick, trick[0].suit) if HeartsCard.in_(self, trick) else HeartsCard.cards_of_suit(trick + [self], trick[0].suit)
        return self == max(
            cards,
            key=lambda card: card.rank.value,
            default=None,)
        

    def cards_of_suit(cards, suit):
        return [card for card in cards if card.suit == suit]


class HeartsPlayer:
    def index_(li, other):
        return [str(card) for card in li].index(str(other))

    def __init__(self, game, name=None) -> None:
        self.game = game
        self.hand = []
        self.taken = []
        self.points = 0
        self.game.player_counter += 1
        self.name = name if name else f"Player {self.game.player_counter}"

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"HeartsPlayer({self.game}, {self.name})"

    def points_this_hand(self, shot_the_moon):
        #         print(self.taken)
        if shot_the_moon:
            if self.points_this_hand(False) == 26:
                return 0
            else:
                return 26
        else:
            return sum((card.score_value() for card in self.taken))

    def play_card(self, card):
        self.hand.pop(HeartsPlayer.index_(self.hand, card))
        self.game.trick.append(card)

    def sort_hand(self):
        self.hand = sum(
            (
                sorted(x, key=lambda card: card.rank.value)
                for x in [
                    [card for card in self.hand if card.suit == suit] for suit in Suit
                ]
            ),
            [],
        )

    def choose_pass_cards(self):
        # cpu logic
        pass_cards = []
        for _ in range(3):
            cur_hand = [card for card in self.hand if card not in pass_cards]
            high_spades = HeartsCard.high_card(cur_hand, Suit.SPADES)
            if high_spades is not None and high_spades.suit.value >= 12:
                pass_cards.append(high_spades)
            elif HeartsCard.cards_of_suit(cur_hand, Suit.HEARTS):
                pass_cards.append(HeartsCard.high_card(cur_hand, Suit.HEARTS))
            else:
                pass_cards.append(HeartsCard.high_card(cur_hand))
        return pass_cards

    def choose_play_card(self):
        # more cpu logic
        leader = self.game.trick == []
        card = None
        if self.game.round_counter == 1:
            if leader:
                card = HeartsCard(Suit.CLUBS, Rank.TWO)
            else:
                card = HeartsCard.high_card(
                    self.hand,
                    Suit.CLUBS
                    if HeartsCard.cards_of_suit(self.hand, Suit.CLUBS)
                    else None,
                )

        elif self.game.round_counter == 13:
            card = self.hand[0]
        elif not self.game.queen_played:
            if leader:
                if HeartsCard.cards_of_suit(self.hand, Suit.SPADES):
                    if HeartsCard(Suit.SPADES, Rank.QUEEN).in_(self.hand):
                        card = HeartsCard.low_card(
                            [
                                card
                                for card in self.hand
                                if self.can_play_card(card) and card.suit != Suit.SPADES
                            ]
                        )
                        if card is None:
                            card = HeartsCard.high_card(self.hand)
                    else:
                        card = self.highest_losing(HeartsCard(Suit.SPADES, Rank.QUEEN))
            elif (
                not HeartsCard(Suit.SPADES, Rank.QUEEN).winning(self.game.trick)
            ) and HeartsCard(Suit.SPADES, Rank.QUEEN).in_(self.hand):
                card = HeartsCard(Suit.SPADES, Rank.QUEEN)
            elif not HeartsCard.cards_of_suit(self.hand, self.game.trick[0].suit):
                if HeartsCard.cards_of_suit(self.hand, Suit.HEARTS):
                    if HeartsCard.high_card(self.hand, Suit.HEARTS).rank.value >= 11:
                        card = HeartsCard.high_card(self.hand, Suit.HEARTS)
                if card is None:
                    card = HeartsCard.high_card(self.hand)
        else:
            if not leader:
                if HeartsCard.cards_of_suit(self.hand, self.game.trick[0].suit):
                    card = self.highest_losing(
                        HeartsCard.high_card(self.game.trick, self.game.trick[0].suit)
                    )
                else:
                    card = HeartsCard.high_card(self.hand)

        if card is None:
            card = HeartsCard.low_card(
                [card for card in self.hand if self.can_play_card(card)]
            )
        return card

    def highest_losing(self, max):
        return HeartsCard.high_card(
            [card for card in self.hand if card < max],
            suit=max.suit,
        )

    def can_play_card(self, card):
        # validation function
        if self.game.trick:
            if self.game.round_counter == 1:
                return (
                    (card.suit == Suit.CLUBS)
                    if HeartsCard.cards_of_suit(self.hand, Suit.CLUBS)
                    else card.suit != Suit.HEARTS and not card.in_(["queen of spades"])
                )
            return (
                (card.suit == self.game.trick[0].suit)
                if HeartsCard.cards_of_suit(self.hand, self.game.trick[0].suit)
                else True
            )
        else:
            if self.game.round_counter == 1:
                return card.in_(["two of clubs"])
            return (
                True
                if self.game.hearts_broken
                or len(self.hand)
                == len(HeartsCard.cards_of_suit(self.hand, Suit.HEARTS))
                else (card.suit != Suit.HEARTS)
            )


class HeartsGame:
    def __init__(self) -> None:
        self.passed = False
        self.players = []
        self.deck = None
        self.trick = []
        self.hand_counter = 1
        self.round_counter = 1
        self.took_last_hand = 0
        self.cur_trick = []
        self.hearts_broken = False
        self.queen_played = False
        self.player_counter = 0
        self.finishes = 0
        self.turn = False
        self.resume_info = None
        self.shot_the_moon = False
        self.players.append(HeartsPlayer(self, "You"))
        while len(self.players) < 4:
            self.players.append(HeartsPlayer(self))
        self.scores = [[player.name for player in self.players]]

    def __repr__(self):
        return f"HeartsGame()"

    def __str__(self):
        return f"HeartsGame"

    def save(self):
        with open(os.path.join(basedir, "saves", "savedata"), "wb") as file:
            pickle.dump(self, file)

    def score_round(self):
        # updates points of and returns round winner
        winner = self.round_winner()
        print(winner)
        print(self.trick)
        [winner.taken.append(card) for card in self.trick]
        winner.points += sum((card.score_value() for card in self.trick))
        return winner

    def load():
        loaded_game = None
        with open(os.path.join(basedir, "saves", "savedata"), "rb") as file:
            loaded_game = pickle.load(file)
        return loaded_game

    def make_deck(self):
        deck = [HeartsCard(suit, rank) for suit in Suit for rank in Rank]
        shuffle(deck)
        self.deck = deck

    def deal_hands(self):
        for _ in range(13):
            for i in range(4):
                self.players[i].hand.append(self.deck.pop())

    def round_winner(self):
        # returns winner of round
        print([card for card in self.trick if card.winning(self.trick)][0])
        return self.players[
            (
                self.took_last_hand
                + HeartsPlayer.index_(
                    self.trick,
                    [card for card in self.trick if card.winning(self.trick)][0],
                )
            )
            % 4
        ]

    def calc_swap(self, swap):
        # determines player a specified player should pass cards to in current hand
        if self.hand_counter % 4 == 1:
            return (swap + 1) % 4
        elif self.hand_counter % 4 == 2:
            return swap - 1 if swap - 1 >= 0 else 3
        else:
            return (swap + 2) % 4

    def swap(self, swap_cards, player, swap_player):
        # passes cards from player to swap_player
        for card in swap_cards:
            swap_player.hand.append(player.hand.pop(player.hand.index(card)))


# if __name__ == "__main__":
#     import doctest
#
#     doctest.testmod()
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     app.exec()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    app.exec()
