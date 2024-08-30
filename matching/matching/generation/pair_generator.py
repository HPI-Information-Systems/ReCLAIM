

from typing import Callable, List, Tuple
import pandas as pd

from matching.generation.neighbourhood import Neighbourhood

BlockingCallable = Callable[[pd.Series, pd.Series], bool]

class PairGenerator:
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self.blocking_criteria: List[Tuple[int, BlockingCallable]] = []

        self.data = data

        self.neighbourhood_generator: Neighbourhood = None

    def add_blocking_criterion(self, blocking_criterion: BlockingCallable, priority: int = 0):
        """
        Add a blocking criterion to the pair generator.
        :param blocking_criterion: The blocking criterion to add. It should be a function that takes two entities (as pd.Series) as input and returns a boolean value of if they can even be candidates or not.
        :param priority: The priority of the blocking criterion. Higher values have higher priority and will be executed first. Otherwise, the order of addition is preserved.
        :return: The pair generator.
        """
        
        self.blocking_criteria.append((priority, blocking_criterion))
        
        self.blocking_criteria.sort(key=lambda x: x[0], reverse=True)
        
        return self
    
    def generate_pairs(self) -> pd.DataFrame:
        """
        Generate the pairs.
        """
        
        pairs = pd.DataFrame()

        for index, row in self.data.iterrows():

            if self.neighbourhood_generator is not None:
                neighbourhood = self.neighbourhood_generator.find_neighbourhood(row)
            else:
                neighbourhood = self.data
            
            row.index = ["1_" + str(x) for x in row.index]

            for index2, row2 in neighbourhood.iterrows():
                row2.index = ["2_" + str(x) for x in row2.index]
                # we only want to generate each pair once this also ensures that trainset and testset are disjoint
                if index < index2: 
                    if not self._blocking(row, row2):
                        # yield row, row2 # a candidate pair
                        pair = pd.concat([row, row2], axis=0)
                        pairs = pd.concat([pairs, pair], ignore_index=True)
        
        return pd.DataFrame(pairs)

    def _blocking(self, entity1: pd.Series, entity2: pd.Series) -> bool:
        """
        Check if the entities should be blocked.
        """
        
        for _, blocking_criterion in self.blocking_criteria:
            if blocking_criterion(entity1, entity2):
                return True
        
        return False