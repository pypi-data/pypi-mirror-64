import networkx as nx
import pipeline.Stage as stg
import core.Task as task

from typing import List


class Scheduler:

    def __init__(self):
        """
        :var self.task_to_dependencies: A dictionary mapping each task to its list of dependencies. It is used to keep track of all dependencies existing for a task.
             If this list is empty, there are no more dependencies for this tasks and so it can be started
        :var self.execution_graph: DAG representing the scheduling of tasks in the pipeline
        :var self.task_graph: DAG representing the pipeline and task-dependencies
        :var self.nodes: All nodes the task_graph-DAG contains (i.e. all tasks)
        """
        self.execution_graph = nx.DiGraph()
        self.task_graph = None
        self.nodes = None
        self.task_to_dependencies = None

    def generate_execution_graph(self, task_graph: nx.DiGraph, stages: List['stg.Stage']) -> (nx.DiGraph, List[List[task.Task]]):
        """
        This method builds an execution-graph which determines the schedule of the tasks registered in the pipeline.
        To do this, the following is done:
            as long as min. one task remains in any of the stages do:
                move backwards through task-graph-stages:
                    for each task in a stage:
                        check if it is ready to run
                        if so, add to execution-graph
                        connect the new node with all nodes added in the previous run to the execution-graph
                        remove all dependencies referring to this task in order to guarantee that in next round no task waits for a task already 'done' (i.e. added to the graph)

        :param task_graph: A directed acyclic graph (DAG) describing the pipeline-structure
        :param stages: List of stages defined in pipeline
        :var to_run: List of tasks that are marked ready for this round and so get added to execution-graph
        :var last_run: List of tasks marked ready in last round. Used to connect them in execution-graph with the tasks in 'to_run'
        :var start_nodes: List of nodes to start with when executing the execution graph (so all root-nodes)
        :return: Execution Graph which is also a directed acyclic graph (DAG)
        """
        self.task_graph = task_graph
        self.nodes = list(task_graph.nodes)
        self.task_to_dependencies = {t: t.get_dependencies() for t in self.nodes}

        def reduce_stages(stage_list: List['stg.Stage']):
            """

            :param stage_list: List of stages to be flattened
            :return: Flattened List containing references to all tasks in the stages
            """
            l = []
            for s in stage_list:
                l += s.task_list
            return l

        node_hierarchy = []
        last_run = []
        # repeat as long as there are unprocessed tasks in any stage
        while reduce_stages(stages):
            to_run = []

            # go through task graph backwards to guarantee dependency-freedom if dependency-free node is found
            for st_ind in range(len(stages) - 1, -1, -1):
                stage = stages[st_ind]
                to_run += self._find_ready(stage, last_run)

            node_hierarchy.append(to_run)
            last_run = to_run

        return self.execution_graph, node_hierarchy

    def _remove_dependencies(self, tsk: task.Task) -> None:
        """
        This method removes all dependencies for a given task. The given task is one which has no dependencies itself.
        Therefore it can be run, so to guarantee that no task has a dependency to the given task in the next iteration,
        all dependencies referring to it are removed.

        :param tsk: Task-object whose dependencies should be removed.
        :return: None
        """
        for t in self.task_to_dependencies.keys():
            if tsk in self.task_to_dependencies[t]:
                self.task_to_dependencies[t].remove(tsk)

    def _find_ready(self, stage: stg.Stage, last_run: List[task.Task]) -> List[task.Task]:
        """
        Private helper-method to find an execution graph. This method implements the finding of a list of tasks
        ready to be scheduled for one iteration over the stages.

        :param stage: A stage-object.
        :param last_run: A list of tasks that where added to 'to_run' in last iteration
        :return: A list of tasks ready to be executed (i.e. they have no dependencies)
        """
        # create a list of tasks that can be removed.
        # Due to Python's iterating-mechanism a list must save which objects can be removed.
        # You cannot safely remove an object of a list you are iterating over, this is because the indices will
        # change as you delete an object. Result: Python will skip some indices.
        to_be_removed, to_run = [], []

        # is any task ready to be executed?
        for t in stage.task_list:
            if not self.task_to_dependencies[t]:
                to_run.append(t)
                to_be_removed.append(t)
                self.execution_graph.add_node(t)
                if last_run:
                    for lr in last_run:
                        self.execution_graph.add_edge(lr, t)
                self._remove_dependencies(t)

        # remove the tasks that got scheduled.
        for t in to_be_removed:
            stage.task_list.remove(t)

        return to_run

