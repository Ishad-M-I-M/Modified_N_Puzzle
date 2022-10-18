import _thread
import math
import re
import argparse
import sys
import threading


class Node:
    def __init__(self, state, path_cost, heuristic_cost, parent, move_taken):
        self.state = state
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.parent = parent
        self.move_taken = move_taken

    def __eq__(self, other):
        return self.state == other.state

    def misplaced(self, goal_state):
        heuristic_cost = 0
        for i in range(len(self.state)):
            # count the number of tiles in curr_state different from goal_state
            if self.state[i] != '-' and self.state[i] != goal_state[i]:
                heuristic_cost += 1

        return heuristic_cost

    def manhattan(self, goal_state):
        size = int(len(self.state) ** 0.5)
        heuristic_cost = 0

        # calculate manhattan distance for both empty tiles
        for pos1 in range(len(self.state)):
            if self.state[pos1] != '-':
                pos2 = goal_state.index(self.state[pos1])

                row1 = pos1 // size
                row2 = pos2 // size
                col1 = pos1 - size * row1
                col2 = pos2 - size * row2

                heuristic_cost += abs(row1 - row2) + abs(col1 - col2)

        return heuristic_cost

    def backtrack(self):
        moves = []
        parent_node = self
        while parent_node.parent is not None:
            moves.append(parent_node.move_taken)
            parent_node = parent_node.parent
        return list(reversed(moves))


class Queue:
    def __init__(self):
        self.lst = []

    def add(self, node):
        self.lst += [node]

    def pop_min(self):
        f = float('INF')
        node_index = -1

        for i in range(len(self.lst)):
            if self.lst[i].path_cost + self.lst[i].heuristic_cost < f:
                node_index = i
                f = self.lst[i].path_cost + self.lst[i].heuristic_cost
        node = self.lst[node_index]
        self.lst = self.lst[:node_index] + self.lst[node_index + 1:]
        return node

    def exist(self, state):
        for i in range(len(self.lst)):
            if self.lst[i].state == state:
                return i
        return False

    def get(self, index):
        return self.lst[index]

    def __len__(self):
        return len(self.lst)


class ModifiedNPuzzle:
    time = 60.0

    def __init__(self, start, goal, h, w=False, time=time):

        if isinstance(start, list):
            self.start = start
            self.goal = goal
        else:
            self.start = self.__readfile(start)
            self.goal = self.__readfile(goal)

        self.size = math.ceil(math.sqrt(len(self.start)))

        self.open_queue = Queue()
        self.closed_queue = Queue()

        if h == "manhattan":
            self.h = lambda s, g: s.manhattan(g)
        else:
            self.h = lambda s, g: s.misplaced(g)

        self.w = w
        ModifiedNPuzzle.time = time

    @staticmethod
    def __readfile(path):
        file = open(path, 'r')
        text = file.read()
        file.close()
        return re.split('\t|\n', text.strip())

    @staticmethod
    def __writefile(path, moves):
        text = ', '.join(['({}, {})'.format(tile, move) for tile, move in moves]) + '\n'
        file = open(path, 'w')
        file.write(text)
        file.close()

    # methods to limit run time
    @staticmethod
    def quit_function(fn_name):
        # print to stderr, unbuffered in Python 2.
        print(f'\033[91mTakes too long to solve. Interrupting the execution.\n '
              f'Failed to solve within : {ModifiedNPuzzle.time} s \n'
              'try by specifying larger --time value\033[0m')
        sys.stderr.flush()  # Python 3 stderr is likely buffered.
        _thread.interrupt_main()  # raises KeyboardInterrupt

    @staticmethod
    def exit_after(s):
        '''
        use as decorator to exit process if
        function takes longer than s seconds
        '''

        def outer(fn):
            def inner(*args, **kwargs):
                timer = threading.Timer(s, ModifiedNPuzzle.quit_function, args=[fn.__name__])
                timer.start()
                try:
                    result = fn(*args, **kwargs)
                finally:
                    timer.cancel()
                return result

            return inner

        return outer

    @exit_after(time)
    def solve(self):

        start_node = Node(self.start,
                          0,
                          0,
                          None,
                          (-1, ''))
        start_node.heuristic_cost = self.h(start_node, self.goal)
        self.open_queue.add(start_node)

        self.closed_queue = Queue()

        # iterates till open_queue is not empty
        while True:

            # remove from open queue, the node with lowest f = g+h
            node = self.open_queue.pop_min()

            # mark node as closed
            self.closed_queue.add(node)

            # if the goal configuration is reached with min f score, stop
            if node.state == self.goal:
                break

            # expand the node
            for child in self.expand(node):

                # if child is in closed queue, ignore it
                if self.closed_queue.exist(child.state):
                    continue

                # if child is not in open queue, add it
                index = self.open_queue.exist(child.state)

                if not index:
                    self.open_queue.add(Node(
                        child.state,
                        node.path_cost + 1,
                        self.h(child, self.goal),
                        node,
                        child.move_taken))

                else:
                    # update data of the node
                    if self.open_queue.get(index).path_cost > node.path_cost + 1:
                        self.open_queue.get(index).path_cost = node.path_cost + 1
                        self.open_queue.get(index).parent = node
                        self.open_queue.get(index).move_taken = child.move_taken

        moves = node.backtrack()

        print("Number of nodes checked :", len(self.closed_queue))
        print("Solution :", moves)

        if self.w:
            self.__writefile('output.txt', moves)

        return len(self.closed_queue)

    def expand(self, node):
        children = []

        moving_tiles = [i for i, e in enumerate(node.state) if e == "-"]

        new_state = node.state.copy()

        for n in moving_tiles:

            row = n // self.size  # row number

            if not (n == self.size * row):
                num = node.state[n - 1]
                new_state[n] = num
                new_state[n - 1] = '-'

                move = (num, 'right')

                if num != '-': children.append(Node(new_state, float('INF'), float('INF'), node, move))
                new_state = node.state[:]

            if not (n == self.size * (row + 1) - 1):
                num = node.state[n + 1]
                new_state[n] = num
                new_state[n + 1] = '-'

                move = (num, 'left')

                if num != '-': children.append(Node(new_state, float('INF'), float('INF'), node, move))
                new_state = node.state[:]

            if not row == 0:
                num = node.state[n - self.size]
                new_state[n] = num
                new_state[n - self.size] = '-'

                move = (num, 'down')

                if num != '-': children.append(Node(new_state, float('INF'), float('INF'), node, move))
                new_state = node.state[:]

            if not row == self.size - 1:
                num = node.state[n + self.size]
                new_state[n] = num
                new_state[n + self.size] = '-'

                move = (num, 'up')

                if num != '-': children.append(Node(new_state, float('INF'), float('INF'), node, move))
                new_state = node.state[:]

        return children

    def print_start(self):
        print("Start state:")
        for row in [self.start[i:i + self.size] for i in range(0, self.size ** 2, self.size)]:
            print(*row, sep="\t")
        print()

    def print_goal(self):
        print("Goal state:")
        for row in [self.goal[i:i + self.size] for i in range(0, self.size ** 2, self.size)]:
            print(*row, sep="\t")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modified N Puzzle Problem")
    parser.add_argument('start',
                        metavar="Start Configuration",
                        type=str,
                        help="Text file containing start configuration of puzzle")

    parser.add_argument('goal',
                        metavar="Goal Configuration",
                        type=str,
                        help="Text file containing start configuration of puzzle")

    parser.add_argument('--heuristic',
                        dest='h',
                        metavar="misplaced/manhattan",
                        default="misplaced",
                        choices=["misplaced", "manhattan"])

    parser.add_argument('--time',
                        dest='time',
                        default=10.0,
                        )

    args = parser.parse_args()

    puzzle = ModifiedNPuzzle(args.start, args.goal, args.h, True, args.time)
    puzzle.print_start()
    puzzle.print_goal()
    try:
        puzzle.solve()
    except KeyboardInterrupt:
        sys.exit()
