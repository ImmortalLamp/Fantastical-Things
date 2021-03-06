import os
import logging.config
import string
import random
import datetime

from hashlib import sha1
from collections import deque

from scrumban_board_python.scrumban_board.cardlist import CardList
from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")


class Board:
    """
    Board contains Cardlists with cards

    Example:
    client = scrumban_board.Client()

    user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)

    for board in user.user_boards:
        for cardlist in board.cardlists:
            cardlist.add_card(card)
            break
    """

    @staticmethod
    def get_cardlists(cardlists):
        new_cardlists = deque()

        if cardlists is not None:
            if isinstance(cardlists, CardList):
                new_cardlists.append(cardlists)

            elif isinstance(cardlists, deque):
                for cardlist in cardlists:
                    if isinstance(cardlist, str):
                        new_cardlist = CardList(title=cardlist)
                        new_cardlists.append(new_cardlist)

                    if isinstance(cardlist, CardList):
                        new_cardlists.append(cardlist)

        else:
            to_do = CardList("To-Do")
            doing = CardList("Doing")
            done = CardList("Done")
            overdue = CardList("Overdue")

            new_cardlists.append(to_do)
            new_cardlists.append(doing)
            new_cardlists.append(done)
            new_cardlists.append(overdue)

        return new_cardlists

    @staticmethod
    def get_users_login(users_login):
        new_users_login = deque()

        if isinstance(users_login, str):
            new_users_login.append(users_login)

        elif isinstance(users_login, deque):
            for user_id in users_login:
                if isinstance(user_id, str):
                    new_users_login.append(user_id)

        return new_users_login

    def __init__(self, title: str, users_login,
                 description: str = None, cardlists=None):
        """
        Initialising of Board

        :param title: board title
        :param users_login: users login
        :param description: board description
        :param cardlists: board cardlists
        """
        self.title = title
        self.description = description

        self.cardlists = Board.get_cardlists(cardlists)
        self.users_login = Board.get_users_login(users_login)

        self.id = self._get_id()

        logger.info("Board ({}) was created".format(self.id))

    def _get_id(self):
        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.title)))

        return sha1(("Board: " +
                     key + " " +
                     self.title + " " +
                     str(datetime.datetime.now())).encode('utf-8')).hexdigest()

    def __str__(self):
        users_id = [user_id for user_id in self.users_login]
        cardlists = [cardlist for cardlist in self.cardlists]

        output = Colors.cardlist_green + """
--- Board ---
Title: {}
Description: {}
ID: {}

Users logins:
{}

Cardlists:
{}

--End Board--
""".format(self.title,
           self.description,
           self.id,
           users_id,
           cardlists) + Colors.end_color

        return output

    def __repr__(self):
        users_id = [user_id for user_id in self.users_login]
        cardlists = [cardlist for cardlist in self.cardlists]

        output = Colors.cardlist_green + """
--- Board ---
Title: {}
Description: {}
ID: {}

Users logins:
{}

Cardlists:
{}

--End Board--
""".format(self.title,
           self.description,
           self.id,
           users_id,
           cardlists) + Colors.end_color

        return output

    def update_board(self, title: str = None, users_login: deque = None, description: str = None,
                     cardlists: deque = None):
        """
        Updating board params

        :param title: board title
        :param users_login: users login
        :param description: board description
        :param cardlists: board cardlists
        :return:
        """
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if cardlists is not None:
            self.cardlists = Board.get_cardlists(cardlists)

        if users_login is not None:
            self.users_login = Board.get_users_login(users_login)

        logger.info("Board ({}) was updated".format(self.id))

    def find_cardlist(self, cardlist_id=None, cardlist_title=None):
        """
        Searching cardlist on the board

        :param cardlist_id:
        :param cardlist_title:
        :return:
        """
        if cardlist_id is not None:
            try:
                cardlist = next(cardlist for cardlist in self.cardlists if cardlist.id == cardlist_id)
                logger.info("Cardlist ({}) was found by cardlist_id on the Board ({})".format(cardlist.id,
                                                                                              self.id))
                return cardlist

            except StopIteration:
                logger.info("Cardlist ({}) wasn't found by cardlist_id on the Board ({})".format(cardlist_id,
                                                                                                 self.id))

        elif cardlist_title is not None:
            try:
                cardlist = next(cardlist for cardlist in self.cardlists if cardlist.title == cardlist_title)
                logger.info("Cardlist ({}) was found by cardlist_title on the Board ({})".format(cardlist.id,
                                                                                                 self.id))
                return cardlist

            except StopIteration:
                logger.info("Cardlist ({}) wasn't found by cardlist_title on the Board ({})".format(cardlist_title,
                                                                                                    self.id))

        return None

    def add_cardlist(self, new_cardlist: CardList):
        """
        Adding new cardlist

        :param new_cardlist: new cardlist
        :return:
        """
        duplicate_cardlist = self.find_cardlist(new_cardlist)

        if duplicate_cardlist is None:
            self.cardlists.append(new_cardlist)
            logger.info("Cardlist ({}) was added on the Board ({})".format(new_cardlist.id,
                                                                           self.id))

    def remove_cardlist(self, cardlist: CardList = None, cardlist_id: str = None):
        """
        Removing cardlist from the board

        :param cardlist: Cardlist
        :param cardlist_id: cardlist id as str
        :return:
        """
        if cardlist is not None:
            duplicate_cardlist = self.find_cardlist(cardlist.id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)
                logger.info("Cardlist ({}) was removed from the Board ({})".format(duplicate_cardlist.id,
                                                                                   self.id))

        elif cardlist_id is not None:
            duplicate_cardlist = self.find_cardlist(cardlist_id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)
                logger.info("Cardlist ({}) was removed from the Board ({})".format(duplicate_cardlist.id,
                                                                                   self.id))

    def change_cardlist_position(self, position: int, cardlist: CardList = None, cardlist_id: str = None):
        """
        Changing cardlist position on the board

        :param position: 1, 2, 3 ... n
        :param cardlist: Cardlist
        :param cardlist_id: cardlist id
        :return:
        """
        if cardlist is not None:
            duplicate_cardlist = self.find_cardlist(cardlist.id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)

                real_position = position - 1
                self.cardlists.insert(real_position, duplicate_cardlist)

                logger.info(
                    "Cardlist ({}) was moved in the Board ({}) to position {}".format(duplicate_cardlist.id,
                                                                                      self.id,
                                                                                      real_position))

        elif cardlist_id is not None:
            duplicate_cardlist = self.find_cardlist(cardlist_id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)

                real_position = position - 1
                self.cardlists.insert(real_position, duplicate_cardlist)
                logger.info(
                    "Cardlist ({}) was moved in the Board ({}) to position {}".format(duplicate_cardlist.id,
                                                                                      self.id,
                                                                                      real_position))

    def move_card(self, card_id: str, old_cardlist_id: str, new_cardlist_id: str):
        """
        Moving cards between cardlists

        :param card_id: card id
        :param old_cardlist_id: old cardlist id
        :param new_cardlist_id: new cardlist id
        :return:
        """

        old_cardlist = self.find_cardlist(old_cardlist_id)
        new_cardlist = self.find_cardlist(new_cardlist_id)

        card = old_cardlist.find_card(card_id=card_id)
        old_cardlist.remove_card(card=card)
        new_cardlist.add_card(card)

        logger.info(
            "Card ({}) was moved from CardList ({}) to Cardlist ({})".format(card.id,
                                                                             old_cardlist.id,
                                                                             new_cardlist.id))
