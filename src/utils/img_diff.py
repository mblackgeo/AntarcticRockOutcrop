import numpy as np
import matplotlib.pyplot as plt

"""
This class can be used to calculate the differences between two binary rasters with identical spatial extent. 
We use this to validate the outputs of our model by comparing them to the published burton-johnson rock labels.
"""
class OutputAnalysis:
    COLOR_MAP = 'Set1'

    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        self.diff_raster = self.img_diff()
        # get histogram results and filter out empty values. Should return len(4) array
        self.diff_hist = [i for i in np.histogram(self.diff_raster)[0] if i]

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

    def __str__(self):
        total_pixels = self.diff_hist[0] + self.diff_hist[1] + self.diff_hist[2] + self.diff_hist[3]
        agreement = self.diff_hist[0] + self.diff_hist[3]
        disagreement = self.diff_hist[1] + self.diff_hist[2]
        summary_stats = "Total: {}\nAgreement: {}\nDisagreement:{}\nNegative: {}\nFalse Negative: {}\n" \
                        "False Positive: {}\nPositive:{}\n\n".format(total_pixels,
                                                                  agreement,
                                                                  disagreement,
                                                                  self.diff_hist[0], 
                                                                  self.diff_hist[1], 
                                                                  self.diff_hist[2],
                                                                  self.diff_hist[3])
        accuracy = agreement / total_pixels * 100
        error = disagreement / total_pixels * 100
        rock_omission = self.diff_hist[1] / (self.diff_hist[1] + self.diff_hist[3]) * 100
        rock_commission = self.diff_hist[2] / (self.diff_hist[2] + self.diff_hist[3]) * 100
        notrock_omission = self.diff_hist[2] / (self.diff_hist[0] + self.diff_hist[2]) * 100
        notrock_commission = self.diff_hist[1] / (self.diff_hist[0] + self.diff_hist[1]) * 100
        
        error_stats = "Accuracy: {:2.2f}%\nError: {:2.2f}%\n"\
                "Omission Error\n\tRock: {:2.2f}%\n\tNotRock: {:2.2f}%\n"\
                "Commission Error\n\tRock: {:2.2f}%\n\tNotrock: {:2.2f}%\n\n".format(
                                                                accuracy, error,
                                                                rock_omission, notrock_omission,
                                                                rock_commission, notrock_omission)

        rock_producers = self.diff_hist[3] / (self.diff_hist[1] + self.diff_hist[3]) * 100
        notrock_producers = self.diff_hist[0] / (self.diff_hist[0] + self.diff_hist[2]) * 100
        rock_users = self.diff_hist[3] / (self.diff_hist[2] + self.diff_hist[3]) * 100
        notrock_users = self.diff_hist[0] / (self.diff_hist[0] + self.diff_hist[1]) * 100

        accuracy_stats = "Producer's Accuracy\n\tRock: {:2.2f}%\n\tNot Rock: {:2.2f}%\n"\
                "User's Accuracy\n\tRock:{:2.2f}%\n\tNot Rock: {:2.2f}%\n\n".format(rock_producers, notrock_producers,
                                                                  rock_users, notrock_users)
        return summary_stats + error_stats + accuracy_stats


