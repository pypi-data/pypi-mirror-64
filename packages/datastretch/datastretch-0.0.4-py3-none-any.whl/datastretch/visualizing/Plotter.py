import matplotlib.pyplot as plt


class Plotter:

    """
    Plotter-class is recommended to be used as parent-class. If inheriting from Plotter you have to implement the plot-method, so an instance of your class
    provides a plot-method directly.

    It's also possible to instantiate the Plotter-class and give the data per argument to the .plot-method
    """

    def __init__(self):
        return

    def plot(self, data=None):
        """

        :param data: Data to be plotted. If you inherit from Plotter this should always be None
        :return: None or figure
        """
        raise NotImplementedError()
