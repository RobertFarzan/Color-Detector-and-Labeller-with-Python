import pandas as pd
import numpy as np

class Colorname():

    def __init__(self):
        self.dataset = pd.read_csv('colorhexa_com.csv', header=0)
        self.dataset = self.dataset.rename(columns={'Red (8 bit)': 'R', 'Blue (8 bit)': 'B', 'Green (8 bit)': 'G'})
        self.color_list = self.dataset[["R", "G", "B"]].to_numpy()

    def get_colorname(self, r, g, b):
        target_color = np.array([r, g, b])
        dist = np.linalg.norm(self.color_list - target_color, axis=1, ord=2) # euclidean distance

        idx = dist.argmin()

        return self.dataset.loc[idx, 'Name'] 