import random

from typing import List

MAX_TASKS = 1000


class Task:

    def __init__(self, name: str = None):
        self._hash: int = random.randint(0, MAX_TASKS)
        # dependency to other task
        self._depencies: List[Task] = []
        self.run_arguments = {'args': (), 'kwargs': {}}
        self.data = None
        self._flow_data: dict = {}
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
                self._depencies.append(o)
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

    def move_data(self, successors: List['Task']):
        """
        This method moves the data of the Task-instance to its dependencies. Automatically called when task has finished.
        The data is stored in a dictionary, keyed by the name of the task stored its data. The value is the data-object.

        :return: None
        """
        for s in successors:
            if s._flow_data is None:
                raise ValueError("Value of successors data is None. Maybe you have assigned self._flow_data to None in a child-class?")
            self._flow_data[self.name] = self.data
            s._flow_data = self._flow_data

    def get_dependency(self):
        """
        Generator yielding the dependencies of a task

        :return: Task-object
        """
        for dep in self._depencies:
            yield dep

    def get_dependencies(self):
        """
        Method returning the list of all dependencies

        :return: List of Task-objects
        """
        return self._depencies
