
from typing import List, Callable

# This method computes height for stacked blocks
def compute_height(blocks: List[List[int]]) -> int:
    if blocks :
        heights, *_ = zip(*blocks)
        return sum(heights)
    return 0

# This method implements binary search algorithm
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

# Class for candidate solution for tabu search
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
    
    # This method pushes a specific block into the candidate's stacked blocks
    #   and returns the height of the resulting stacked blocks 
    # If update is True, the resulting stacked blocks become the candidate's
    #   stacked blocks
    def push(self, block: List[int], update: bool) -> int:
        n = len(self._blocks)

        # in the candidate's stacked blocks, start is the index where to insert
        #   the given block. This index corresponds to the minimum of indices
        #   if we considered pushing width and depth separately
        start = min([bisect(self._blocks, block,
                              key = lambda x: x[idx+1]) for idx in range(2)])

        # in the candidate's stacked blocks, end corresponds to the first index
        # whose block can stack on the given block
        end = start

        # while we compute end, the height of the resulting stacked blocks
        # can also be computed
        height = self._height + block[0]
        while end < n :
            if self._blocks[end][1] < block[1] and self._blocks[end][2] < block[2] :
                break
            height -= self._blocks[end][0]
            end += 1

        if update:
            self._tabu   = self._blocks[start:end]
            self._blocks = self._blocks[:start] + [block] + self._blocks[end:]
            self._height = height
  
        return height