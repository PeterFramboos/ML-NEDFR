import re
import pandas as pd
from typing import List, Tuple, Generator

class Dataset:
    
    def __init__(self):
        
        data = self.get_rawdata()
        data = self.clean_data(data)
        self.lines = self.split_pairs(data)
        return
    
    # ====================================================
    def get_rawdata(self, filename="texts.txt") -> str:
        
        # Read the data from file
        with open('texts.txt', 'r') as f:
            data = f.read()
        return data
    
    def clean_data(self, data:str) -> str:
        
        # Filter on alphabet characters (no more commas, dots, etc)
        data = re.sub(r'[^a-zA-Z0-9\[\]\: \n]+', '', data)
        
        return data.lower()
    
    def split_pairs(self, data:str) -> List[str]:
        return data.split('\n\n')

    # ====================================================
    
    def _select_options(self, line:str) -> str:
        
        if line.find('[') == -1:
            yield line
        
        y = 0
        while range(4):
            # Try to find the symbols
            x = line.find('[', y)
            y = line.find(']', x)+1

            # Brake if not found
            if x < 0 or y < 0:
                break

            # Grab the options
            subline = line[x+1:y-1]
            for word in subline.split(' '):
                
                # Compose new line based on choice
                result = line[:x] + word + line[y:]

                # Recursive search through remainder of sentense
                for item in self._select_options(result):
                    yield item
                
            y = x+1
        return
            
            
    
    def get_trainingslines(self) -> Generator[Tuple[str, str], None, None]:
        
        for line in self.lines:
            
            linepair = line.split('\ntr:')
            
            if len(linepair) >= 2:
                
                # All options in the input sentence
                for linein in  self._select_options(linepair[0]):

                    # Select an output sentence
                    for lineouts in linepair[1:]:

                        # All options inside the output sentence
                        for lineout in  self._select_options(lineouts):
                            if len(lineout.strip()) > 0 and len(linein.strip())>0:
                                yield (linein.strip(), lineout.strip())    
                                
    def get_dataframe(self) -> pd.DataFrame:
        

        nederlands, fries = [], []
        for item in self.get_trainingslines():
            nederlands.append(item[0])
            fries.append(item[1])
            
        df = pd.DataFrame({'nederlands': nederlands,
                           'fries': fries})
        
        return df.drop_duplicates().reset_index(drop=True)
        
