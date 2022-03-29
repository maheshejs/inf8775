import time
import argparse
from algos import IAlgo, GreedyAlgo, DynProgAlgo, TabuAlgo
from typing import List, Dict
import utils

class BoxStacking:
    def __init__(self, algo: IAlgo) -> None:
        self._algo = algo

    @property
    def algo(self) -> int :
        return self._algo

    @algo.setter
    def algo(self, algo: int) -> None :
        self._algo = algo
    
    def execute_algo(self, blocks: List[List[int]], options: Dict[str, bool]) -> None :
        start_time = time.perf_counter()
        solution = self._algo.solve(blocks)
        end_time = time.perf_counter()

        if options['height'] :
            print(utils.compute_height(solution))
        if options['print'] :
            for block in solution :
                print(*block)
        # This is optional
        if options['time'] :
            elapsed_time_ms = (end_time - start_time) * 1000
            print(elapsed_time_ms)

if __name__ == "__main__" :
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", \
                        help="algorithm to use", \
                        dest="algo", \
                        action='store', required=True)
    parser.add_argument("-e", \
                        help="example file with blocks", \
                        dest="example_file", \
                        action='store', required=True, metavar = 'FILE_EXAMPLE')
    parser.add_argument("-t", \
                        help="prints elapsed time", \
                        dest="time", \
                        action='store_true')
    parser.add_argument("-p", \
                        help="print solution", \
                        dest="print", \
                        action='store_true')
    parser.add_argument("-x", \
                        help="prints maximum height", \
                        dest="height", \
                        action='store_true')
    args = parser.parse_args()

    # read blocks in file
    blocks = []
    with open(args.example_file, 'r') as f :
        for line in f :
            blocks.append(tuple(int(x) for x in line.rstrip().split()))

    options = {'print': args.print, 'time': args.time, 'height': args.height}

    algo = {'glouton': GreedyAlgo(),
            'progdyn': DynProgAlgo(),
            'tabou'  : TabuAlgo(100)}[args.algo]

    # solve box stacking problem
    box_stacking = BoxStacking(algo)
    box_stacking.execute_algo(blocks, options)