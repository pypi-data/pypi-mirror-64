import networkx as nx
import core.Task as task


class Stage:

    def __init__(self):
        self.task_list = []

    def add(self, tsk: task.Task, dependency: task.Task = None) -> 'Stage':
        """

        :param dependency: Task object the added object depends on. Must be in a different stage. If None it has no dependency or must already be set.
        :param tsk: Task object to be added to stage
        :return: Stage-object
        """
        if dependency is not None:
            tsk.dependency(dependency)
        self.task_list.append(tsk)
        return self

    def remove(self, tsk: task.Task) -> 'Stage':
        """

        :param tsk: Task-object to be removed from stage.
        :return: Stage-object
        """
        try:
            self.task_list.remove(tsk)
        except Exception:
            pass
        return self

    def tasks(self):
        """

        :return: Task-object
        """
        for task in self.task_list:
            yield task
