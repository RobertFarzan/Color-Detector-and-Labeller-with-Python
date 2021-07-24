import pandas as pd

class Colorname():

    def __init__(self):
        self.dataset = pd.read_csv('colorhexa_com.csv', header=0)
        self.dataset = self.dataset.rename(columns={'Red (8 bit)': 'R', 'Blue (8 bit)': 'B', 'Green (8 bit)': 'G'})

    def get_colorname(self, r, g, b):
        mini = (float('inf'), '')

        for elem in self.dataset.iterrows():
            elem = elem[1]
            dist = abs(r - elem.loc['R']) + abs(g - elem.loc['G']) + abs(b - elem.loc['B'])
            mini = min(mini, (dist, elem['Name']), key= lambda t: t[0])
            
            if mini[0] == 0:
                break
        return mini[1]