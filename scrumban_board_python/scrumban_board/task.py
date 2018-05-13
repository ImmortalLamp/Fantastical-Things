from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.subtask import Subtask


class Task:
    def __init__(self, title: str, description: str = None, subtasks_list: list = None):

        self.title = title
        self.description = title

        if description is not None:
            self.description = description

        self.subtasks_list = list()
        if subtasks_list is not None:
            for subtask in subtasks_list:
                if isinstance(subtask, Subtask):
                    self.subtasks_list.append(subtask)

        self.completed = False

        self.id = sha1(("Task: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def update_task(self, title: str = None, description: str = None,
                    subtasks_list: list = None, completed:bool = None):

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if subtasks_list is not None:
            self.subtasks_list.clear()

            for subtask in subtasks_list:
                if isinstance(subtask, Subtask):
                    self.subtasks_list.append(subtask)

        if completed is not None:
            self.completed = completed

    def find_subtask(self, title: str = None, subtask_id: str = None):
        if subtask_id is not None:
            return next(subtask for subtask in self.subtasks_list if subtask.id == subtask_id)

        elif title is not None:
            return next(subtask for subtask in self.subtasks_list if subtask.title == title)

        else:
            return None

    def add_subtask(self, subtask):
        if isinstance(subtask, Subtask):
            new_subtask = self.find_subtask(title=subtask.title)

            if new_subtask is None:
                self.subtasks_list.append(subtask)

        elif isinstance(subtask, str):
            new_subtask = self.find_subtask(subtask)
            if new_subtask is None:

                new_subtask = Subtask(title=subtask)
                self.subtasks_list.append(new_subtask)

    def remove_subtask(self, subtask: Subtask = None, subtask_id: str = None):
        if subtask is not None:
            subtask = self.find_subtask(title=subtask.title)

            if subtask is not None:
                self.subtasks_list.remove(subtask)

        elif subtask_id is not None:
            subtask = self.find_subtask(subtask_id=subtask_id)

            if subtask is not None:
                self.subtasks_list.remove(subtask)
