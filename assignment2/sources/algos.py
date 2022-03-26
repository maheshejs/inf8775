from abc import ABC, abstractmethod
from typing import List
from collections import deque
import utils
import random
import copy

# Interface for algorithm
class IAlgo(ABC) :
    @abstractmethod
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        pass

# Greedy algorithm
class GreedyAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        blocks.sort(key = lambda x : x[0] + x[1] * x[2], reverse = True)
        greedy_blocks = [blocks[0]]
        last_idx = 0
        idx = 1
        while idx < len(blocks):
            if blocks[last_idx][1] > blocks[idx][1] and blocks[last_idx][2] > blocks[idx][2] :
                greedy_blocks.append(blocks[idx])
                last_idx = idx
            idx += 1
        return greedy_blocks

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
    def __init__(self, max_iter: int) -> None: 
        self._max_iter = max_iter
    
    @property
    def max_iter(self) -> int :
        return self._max_iter
        
    @max_iter.setter
    def max_iter(self, max_iter: int) -> None :
        self._max_iter = max_iter


    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        greedy_blocks = GreedyAlgo().solve(blocks)
        best_candidate = utils.Candidate(greedy_blocks, utils.compute_height(greedy_blocks))
        candidate = copy.deepcopy(best_candidate)
        
        tabus = tuple(deque(maxlen = size) for size in range(7, 10+1))
        random.seed(0)
        count = self._max_iter

        while count :
            neighbours = {*blocks} - {*candidate.blocks} - \
                         {block for tabu in tabus for blocks in tabu for block in blocks}

            best_height = 0
            best_neighbour = ()
            for neighbour in neighbours :
                height = candidate.push(neighbour, update = False)
                if height > best_height :
                    best_height = height
                    best_neighbour = neighbour
            
            if not neighbours:
                for tabu in tabus :
                    tabu.popleft()
                pass

            candidate.push(best_neighbour, update = True)
            if candidate.height > best_candidate.height :
                best_candidate = copy.deepcopy(candidate)
                count = self._max_iter
            else :
                count -= 1
        
            random.choice(tabus).append(candidate.tabu)
        
        return best_candidate.blocks