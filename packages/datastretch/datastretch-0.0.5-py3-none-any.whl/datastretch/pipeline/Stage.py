from datastretch.core import Task


class Stage:

    def __init__(self):
        self.task_list = []

    def add(self, *tsk: Task, dependency: Task = None) -> 'Stage':
        """

        :param dependency: Task object the added object depends on. Must be in a different stage. If None it has no dependency or must already be set.
        :param tsk: Tuple of Task objects to be added to stage
        :return: Stage-object
        """
        for t in tsk:
            if dependency is not None:
                t.dependency(dependency)
            self.task_list.append(t)
        return self

    def remove(self, tsk: Task) -> 'Stage':
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
