from abc import ABC, abstractmethod
from bisect import bisect
from typing import List
from collections import deque
from bisect import bisect_left

# Interface for algorithm
class IAlgo(ABC) :
    @abstractmethod
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        pass

# Greedy algorithm
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

class Candidate:
    def __init__(self, blocks: List[List[int]]) -> None:
        self._blocks  = DynProgAlgo().solve(blocks)
        self._height  = 0
        self._tabu    = []

    @property
    def height(self) -> int :
        heights, *_ = zip(*self._blocks)
        return sum(heights)
    
    @property
    def tabu(self) -> List[List[int]] :
        return self._tabu
    
    def update(self, block: List[int]) -> None:
        idxs  = [bisect_left(self._blocks, block, key = lambda x : x[1]),
                  bisect_left(self._blocks, block, key = lambda x : x[2])]
        idx   = max(idxs)
        upper = deque(self._blocks[idx:])
        self._blocks = self._blocks[:idx]
        self._blocks.append(block)
        self._tabu = []
        while upper :
            if upper[0][1] >= block[1] or upper[0][2] >= block[2] :
                self._tabu.append(upper[0])
                upper.popleft()
        self._blocks.extend(upper)

# Tabu search algorithm
class TabuAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        return []
