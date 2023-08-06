import random

from datastretch.exceptions import AccessException
from typing import List

MAX_TASKS = 1000


class Task:

    def __init__(self, name: str = None):
        self._hash: int = random.randint(0, MAX_TASKS)
        # dependency to other task
        self._dependencies: List[Task] = []
        self.run_arguments = {'args': (), 'kwargs': {}}
        self.data: dict = {}
        self._access_type = 'attr'
        if name is not None:
            self.name = name
        else:
            self.name = self.__class__.__name__

    def __hash__(self) -> int:
        """
        method making the object hashable

        :return: random int
        """
        return self._hash

    def __str__(self):
        return str(self.name)

    def dependency(self, *obj: 'Task') -> None:
        """
        Set dependency of this Task-instance on a given Task-instance (obj).

        :param obj: Arbitrary number of Task-objects the created task depends on
        :return: None
        """
        for o in obj:
            if isinstance(o, Task):
                self._dependencies.append(o)
            else:
                raise TypeError("given object must be of type Task")

    def run_args(self, *args, **kwargs):
        self.run_arguments['args'] = args
        self.run_arguments['kwargs'] = kwargs

    def run(self, *args, **kwargs) -> None:
        """
        This is the starting-point of any task added to a pipeline and has to be implemented by each child

        :return: None
        """
        raise NotImplementedError()

    def move_data(self, successors: List['Task'], result: any) -> None:
        """
        This method moves the data of the Task-instance to its dependencies. Automatically called when task has finished.
        The data is stored in a dictionary, keyed by the name of the task stored its data. The value is the data-object.

        :return: None
        """
        for s in successors:
            s.receive(result, self.name)

    def get_dependency(self) -> 'Task':
        """
        Generator yielding the dependencies of a task

        :return: Task-object
        """
        for dep in self._dependencies:
            yield dep

    def get_dependencies(self) -> List['Task']:
        """
        Method returning the list of all dependencies

        :return: List of Task-objects
        """
        return self._dependencies

    def attr_access_as(self, access: str) -> None:
        """

        :param access: Type of how data sent by the ancestor can be accessed (via dictionary or via variable name).
        :return: None
        """
        if access != 'attr' or access != 'dict':
            raise ValueError("'access' must have value 'attr' or 'dict'.")
        self._access_type = access

    def receive(self, data: any, sender: str) -> None:
        """
        This method is called by the ancestor-task when 'move_data()' is called. 'move_data' itself is final, but
        'receive' can be overwritten by the developer.

        :param data: Data which is sent from ancestor of this task
        :param sender: Name of the sender
        :return: None
        """
        sender = sender.lower() + '_data'
        if self._access_type == 'attr':
            self.__dict__[sender] = data
        elif self._access_type == 'dict':
            if isinstance(self.data, dict):
                self.data[sender] = data
            else:
                raise TypeError("Data forwarding failed. Maybe self.data is no longer of type dict.")
        else:
            raise AccessException("Unknown access-type. Set access type to 'dict' or 'attr' via 'attr_access_as()'")

