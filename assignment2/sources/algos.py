from abc import ABC, abstractmethod
from bisect import bisect
from typing import List, Callable
from collections import deque
from copy import deepcopy

def compute_height(blocks: List[List[int]]) -> int:
    heights, *_ = zip(*blocks)
    return sum(heights)

def bisect(lst: List[List[int]], value: List[int], key: Callable[[List[int]], int]) -> int:
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

# Greedy algorithm -- TODO : Find a better greedy choice
class GreedyAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        blocks.sort(key = lambda x : x[1] * x[2], reverse = True)
        solution = [blocks[0]]
        last_idx = 0
        idx = 1
        while idx < len(blocks):
            if blocks[last_idx][1] > blocks[idx][1] and blocks[last_idx][2] > blocks[idx][2] :
                solution.append(blocks[idx])
                last_idx = idx
            idx += 1
        return solution

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
    def __init__(self, blocks: List[List[int]], height: int) -> None:
        self._blocks  = blocks
        self._height  = height
        self._tabu    = []

    @property
    def height(self) -> int :
        return self._height
    
    @property
    def blocks(self) -> List[List[int]] :
        return self._blocks
    
    @property
    def tabu(self) -> List[List[int]] :
        return self._tabu
    
    def push(self, block: List[int], update: bool) -> int:
        insert = min([bisect(self._blocks, block,
                              key = lambda x: x[idx+1]) for idx in range(2)])

        upper = deque(self._blocks[insert:])
        blocks = self._blocks[:insert]
        blocks.append(block)

        if update :
          self._tabu = []

        while upper :
            if upper[0][1] < block[1] and upper[0][2] < block[2] :
                break
            else :
                if update :
                    self._tabu.append(upper[0])
                upper.popleft()
        blocks.extend(upper)
        height = compute_height(blocks)

        if update:
            self._blocks = blocks
            self._height = height
  
        return height

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
        best_candidate = Candidate(greedy_blocks, compute_height(greedy_blocks))
        candidate = deepcopy(best_candidate)
        
        tabus = deque(maxlen = self._tabus_size)
        count = self._max_iter

        while count :
            neighbours = set(blocks) - set(candidate.blocks)
            for tabu in tabus :
                neighbours -= set(tabu)

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
        
            tabus.appendleft(candidate.tabu)
        
        return best_candidate.blocks