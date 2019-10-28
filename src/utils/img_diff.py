import numpy as np
import matplotlib.pyplot as plt


class OutputAnalysis:
    COLOR_MAP = 'Set1'

    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual

    """
    @param np array (M * N * [0, 1]) actual: A binary raster generated as a model output.
    @param np array (M * N * [0, 1]) expected: A binary raster representing the desired output or ground truth.

    @return np array (M * N * [0 - 3] diff: 0 - Negative, 1 - False Negative, 2 - False Positive, 3 - Positive.
    """

    def img_diff(self):
        actual = self.actual * 2
        return self.expected + actual

    """
    @param np array (M * N * 1) or (1 * M * N) arr: a raster to be plotted.

    @returns pyplot figure object: fig with color map assigned. Ready to be shown or saved to file.
    """

    def create_fig(self, arr):
        plt.imshow(arr.squeeze(), cmap=self.COLOR_MAP)
        plt.colorbar()

    """
    @param np array (M * N * 1) or (1 * M * N) arr: a raster to be histogrammed.

    @returns pyplot figure object: histogram with color map assigned. 
    Ready to be shown or saved to file.
    """

    def create_diff_hist(self, arr):

        hist, bin_edges = np.histogram(arr, bins=[0,1,2,3])
        fig, axes = plt.subplots(1,1)
        axes.bar(bin_edges[:-1], hist, width=1)

        return fig
