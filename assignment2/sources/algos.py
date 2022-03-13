from abc import ABC, abstractmethod
from typing import List
from collections import deque
from copy import deepcopy
import utils

# Interface for algorithm
class IAlgo(ABC) :
    @abstractmethod
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        pass

# Greedy algorithm -- TODO : Find a better greedy choice
class GreedyAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        return []

# Dynamic programming algorithm
class DynProgAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        blocks.sort(key = lambda x : x[1] * x[2], reverse = True)
        heights, widths, depths = zip(*blocks)

        n = len(blocks)
        dependency = [-1]*n
        table = [0]*n
        j = 0
        while j < n:
            i = 0
            running_max = 0
            while i < j :
                if widths[i] > widths[j] and depths[i] > depths[j] :
                    if table[i] > running_max :
                        running_max = table[i]
                        dependency[j] = i
                i += 1
            table[j] = running_max + heights[j]
            j += 1

        track = deque([max(range(n), key = table.__getitem__)])
        while dependency[track[0]] != -1:
            track.appendleft(dependency[track[0]])

        return [blocks[idx] for idx in track]


# Tabu search algorithm
class TabuAlgo(IAlgo):
    def __init__(self, max_iter: int, tabus_size: int) -> None: 
        self._max_iter = max_iter
        self._tabus_size = tabus_size
    
    @property
    def max_iter(self) -> int :
        return self._max_iter
        
    @property
    def tabus_size(self) -> int :
        return self._tabus_size
        
    @max_iter.setter
    def max_iter(self, max_iter: int) -> None :
        self._max_iter = max_iter

    @tabus_size.setter
    def tabus_size(self, tabus_size: int) -> None :
        self._tabus_size = tabus_size

    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        greedy_blocks = GreedyAlgo().solve(blocks)
        best_candidate = utils.Candidate(greedy_blocks, utils.compute_height(greedy_blocks))
        candidate = deepcopy(best_candidate)
        
        tabus = deque(maxlen = self._tabus_size)
        count = self._max_iter

        while count :
            neighbours = {*blocks} - {*candidate.blocks} - \
                         {block for tabu in tabus for block in tabu}

            best_height = 0
            best_neighbour = ()
            for neighbour in neighbours :
                height = candidate.push(neighbour, update = False)
                if height > best_height :
                    best_height = height
                    best_neighbour = neighbour
            
            if best_height == 0 :
                break

            candidate.push(best_neighbour, update = True)
            if candidate.height > best_candidate.height :
                best_candidate = deepcopy(candidate)
                count = self._max_iter
            else :
                count -= 1
        
            tabus.append(candidate.tabu)
        
        return best_candidate.blocks