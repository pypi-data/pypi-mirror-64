import random
import networkx as nx
import multiprocessing as mp
import matplotlib.pyplot as plt

from core.Task import Task
from datastretch.pipeline.Scheduler import Scheduler
from datastretch.pipeline.Stage import Stage
from visualizing.Plotter import Plotter
from exceptions.CompilationError import CompilationError
from exceptions.PipelineRuntimeError import PipelineRuntimeError
from typing import List, Set, Iterable
from functools import partial

MAX_PIPELINES = 1000


class Pipeline(Plotter):

    def __init__(self):
        super().__init__()
        self._hash = random.randint(0, MAX_PIPELINES)
        self.task_graph = nx.DiGraph()
        self.stages: List[Stage] = []
        self.MAX_PROCESSES = mp.cpu_count() * 2
        self.scheduler = Scheduler()
        self.execution_graph = None
        self._start_nodes: Set[Task] = set()
        self._process_pool: mp.Pool = None
        self.tree = []

    def __hash__(self) -> int:
        """
        Method making pipeline-objects hashable

        :return: random int
        """
        return self._hash

    def run(self):
        """
        executes the whole pipeline registered

        :return: None
        """
        # avoid changes in task graph
        nx.freeze(self.task_graph)

        # calculate execution graph
        if self.execution_graph is None:
            self.compile()

        # create pool with MAX_PROCESSES processes.
        self._process_pool = mp.Pool(self.MAX_PROCESSES)

        # start execution
        self._exec_execution_graph()

        # close of all is done
        self._process_pool.close()
        self._process_pool.join()

    def add(self, tsk_or_stage: Task or Stage) -> 'Pipeline':
        """
        add a new Task-instance to the pipeline

        :param tsk_or_stage: an object inheriting from Task
        :return: Pipeline-object
        """
        if isinstance(tsk_or_stage, Stage):
            self._add_stage(tsk_or_stage)
        elif isinstance(tsk_or_stage, Task):
            self._add_task(tsk_or_stage)
        else:
            raise TypeError("Given type must be Task or Stage")
        return self

    def compile(self):
        """
        This method can be called before run() to create the execution graph. Especially for debugging-purposes
        this can be a good method to check whether the pipeline is correctly built without running it.
        This method has not to be called before calling run, run will call this implicitly.

        :return: None
        """
        if self._check_cycles_freedom():
            self.execution_graph, self.tree = self.scheduler.generate_execution_graph(self.task_graph, self.stages)
        else:
            raise CompilationError("Can't compile execution graph from task graph. Task graph contains cycles.")

    def plot(self, graph: str = 'task', node_size: int = 5000, font_size: int = 10, arrow_size=30):
        """

        :param arrow_size: size of arrows displayed
        :param font_size: size of font displayed
        :param node_size: size of nodes displayed
        :param graph: String specifying which graph is plotted. Can be 'task' or 'execution'
        :return: None
        """
        labels = {task: task.name for task in list(self.task_graph.nodes)}
        if graph == 'task':
            pos = nx.spring_layout(self.task_graph)
            nx.drawing.draw(self.task_graph, pos=pos, labels=labels, node_size=node_size,
                            font_size=font_size, label="Task Graph", arrow_size=arrow_size)
            plt.draw()
            plt.show()
        elif graph == 'execution':
            if self.execution_graph is not None:
                pos = nx.spring_layout(self.execution_graph)
                nx.drawing.draw(self.execution_graph, pos=pos, labels=labels, node_size=node_size,
                                font_size=font_size, label="Execution Graph", arrow_size=arrow_size)
                plt.draw()
                plt.show()
            else:
                raise RuntimeError("Call 'compile' before drawing execution graph.")
        else:
            raise ValueError("'graph'-argument must have value 'task' or 'execution'")

    def _add_stage(self, stage: Stage) -> None:
        """

        :param stage: Stage-object to be added in pipeline
        :return: None
        """
        for task in stage.tasks():
            self.task_graph.add_node(task)
            if task.get_dependency() is not None:
                for d in task.get_dependency():
                    self.task_graph.add_edge(d, task)
        self.stages.append(stage)

    def _add_task(self, task: Task) -> None:
        """

        :param task: Task-object to be added in pipeline
        :return: None
        """
        self.task_graph.add_node(task)
        for dep in task.get_dependency():
            if len(list(self.task_graph.successors(dep))) > 0:
                self.task_graph.remove_node(task)
                raise ReferenceError("Task " + str(task) + " already has successor task.")
            else:
                self.task_graph.add_edge(dep, task)

    def _exec_execution_graph(self) -> None:
        """
        This method applies the breadth-first-search-algorithm on the execution graph and executes each node it finds.
        The bfs guarantees that the nodes are executed in the correct order.
        Furthermore the algorithm in blocks the master-process as long there are worker-processes processing a
        tree-level.

        :return: None
        """
        for level in self.tree:
            batches = self._create_batches(level)
            for batch in batches:
                self._exec_nodes(batch)

    def _exec_nodes(self, tasks: Iterable) -> None:
        """
        This method is called as a subroutine of breadth-first-search and executes one level of the execution graph.

        :param tasks: An Iterable containing tasks to be executed.
        :return: None
        """
        if not tasks:
            raise ValueError("Given execution graph is empty. Maybe the pipeline is emtpy.")

        results = []
        for task in tasks:
            print("Starting node {}...".format(str(task)))
            callback = partial(self._move_data, task)
            res = self._process_pool.apply_async(task.run, args=task.run_arguments['args'],
                                                 kwds=task.run_arguments['kwargs'], callback=callback)
            results.append(res)
        [res.wait() for res in results]

    def _create_batches(self, tasks: List[Task]) -> List[List[Task]]:
        """
        This method creates batches with respect to the maximum of processes being launched. If there are more parallel
        tasks than available processes the processes have to process the tasks in batches.

        :param tasks: A list of tasks
        :return: a nested list of tasks
        """
        if len(tasks) <= self.MAX_PROCESSES:
            return [tasks]
        else:
            batches = []

            batch = [tasks[0]]
            for i in range(1, len(tasks)):
                if i % self.MAX_PROCESSES != 0:
                    batch.append(tasks[i])
                else:
                    batches.append(batch)
                    batch = [tasks[i]]
            # add rest of the batch
            batches.append(batch)
            return batches

    def _move_data(self, tsk: Task, _) -> None:
        """
        This method is called if a task is executed and the process returns. It moves the data of task.data to its
        successors.

        :param tsk: Task-object whose successors are calculated
        :return: None
        """
        try:
            successors = list(self.execution_graph.successors(tsk))
            tsk.move_data(successors)
        except nx.NetworkXError:
            raise PipelineRuntimeError("Could not evaluate successors, probably a non-task object was passed.")

    def _check_cycles_freedom(self) -> bool:
        start_nodes = self.stages[0].task_list
        try:
            nx.algorithms.find_cycle(self.task_graph, start_nodes)
            return False
        except nx.NetworkXNoCycle:
            return True

