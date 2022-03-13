from abc import ABC, abstractmethod
from bisect import bisect
from typing import List, Callable
from collections import deque

def bisect(lst: List[List[int]], value: List[int], key: Callable[[List[int]], int]):
    lo = 0
    hi = len(lst)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(lst[mid]) > key(value):
            lo = mid + 1
        else:
            hi = mid
    return lo

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
    def blocks(self) -> List[List[int]] :
        return self._blocks
    
    @property
    def tabu(self) -> List[List[int]] :
        return self._tabu
    
    def update(self, block: List[int]) -> None:
        idxs  = [bisect(self._blocks, block, key = lambda x: x[1]),
                  bisect(self._blocks, block, key = lambda x: x[2])]
        idx   = min(idxs)
        upper = deque(self._blocks[idx:])
        self._blocks = self._blocks[:idx]
        self._blocks.append(block)
        self._tabu = []
        while upper :
            if upper[0][1] < block[1] and upper[0][2] < block[2] :
              break
            else :
                self._tabu.append(upper[0])
                upper.popleft()
        self._blocks.extend(upper)

# Tabu search algorithm
class TabuAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        return []


if __name__ == "__main__" :
    blocks = [[10, 5, 8],[5, 8, 10],[8, 5, 10],[7, 1, 15],
              [15, 1, 7],[1, 7, 15],[4, 9, 14],[9, 4, 14],
              [14, 4, 9],[13, 2, 3],[3, 2, 13],[2, 3, 13],
              [12, 6, 11],[11, 6, 12],[6, 11, 12]]
  
    candidate = Candidate(blocks)
    for block in candidate.blocks :
        print(*block)
    print("Height : ", candidate.height)
    candidate.update([21, 7, 11])
    for block in candidate.blocks :
        print(*block)
    print("Height : ", candidate.height)