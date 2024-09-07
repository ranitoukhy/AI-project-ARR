class KnapsackItem:
    """
    An item of the KnapsackProblem.
    """
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight
    
    def __str__(self):
        return f"\n    {self.index}. Value: {self.value}, Weight: {self.weight}"

    def __repr__(self):
        return self.__str__()

class State:
    """
    A state within the search space of A* search of the KnapsackProblem.
    """
    def __init__(self, value, capacity, current_item, items_taken, items_left):
        self.value = value
        self.capacity = capacity
        self.current_item = current_item
        self.items_taken = items_taken
        self.items_left = items_left
    
    def __lt__(self, _):
        return True

    def __str__(self):
        return f"\n<STATE> Total value: {self.value}, Capacity: {self.capacity}," + \
             f"\nIndices taken: {sorted(self.items_taken, key=lambda item: item.index)}, " + \
             f"\nIndices left: {sorted(self.items_left, key=lambda item: item.index)}"

    def __repr__(self):
        return self.__str__()

def parse_input(filepath):
    """
    Parses a file with a Knapsack problem encoding into data.
    An encoding is in the form of:
        n wmax
        v1 w1
        v2 w2
        : :
        vi wi
        : :
        vn wn
    Where:
        1. n is the total number of items
        2. wmax is the capacity of the Knapsack
        3. vi, wi are the value and weight of each item
    :param filepath: A path to a Knapsack problem encoding
    :return: number of items, capacity of the Knapsack, and a list of KnapsackItems.
    """
    items = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    num_items, capacity = lines[0].split()
    num_items = int(num_items)
    capacity = float(capacity)
    for index, line in enumerate(lines[1:]):
        if index == num_items:
            break
        value, weight = map(float, line.split())
        if weight > capacity:
            continue
        items.append(KnapsackItem(index + 1, value, weight))
    items = sorted(items, key=lambda item: item.value / item.weight, reverse=True)
    return num_items, capacity, items


class KnapsackProblem:
    """
    A representation of a Knapsack problem.
    """
    def __init__(self, filepath):
        self.num_items, self.capacity, self.items = parse_input(filepath)
    
    def get_start_state(self):
        """
        :return: A KnapsackState representing the starting state of a search space for the A* search of a goal state.
        """
        start_state = State(0, self.capacity, self.items[0], frozenset(), self.items[1:])
        return start_state

    def is_goal_state(self, state):
        """
        :param state: a KnapsackState to check if it is a goal state of a KnapsackProblem, meaning, if there are
            no more items to add to the Knapsack within the given problem.
        :return: True if the given state is a goal state, false otherwise.
        """
        return state.current_item is None

    def get_successors(self, state):
        """
        :param state: a KnapsackState to find all possible successor states within the search space.
        :return: a set of two KnapsackStates:
            1. A state where the state.current_item is taken into the Knapsack.
            2. A state where the state.current_item is not taken into the Knapsack.
        """
        taken_successor_capacity = state.capacity - state.current_item.weight
        taken_successor_items_left = [item for item in state.items_left if item.weight <= taken_successor_capacity]
        taken = State(
            value = state.value + state.current_item.value,
            capacity = taken_successor_capacity,
            current_item = taken_successor_items_left[0] if len(taken_successor_items_left) > 0 else None,
            items_taken = state.items_taken.union({state.current_item}),
            items_left = taken_successor_items_left[1:]
        )
        not_taken = State(
            value = state.value,
            capacity = state.capacity,
            current_item = state.items_left[0] if len(state.items_left) > 0 else None,
            items_taken = state.items_taken,
            items_left = state.items_left[1:]
        )
        return set([taken, not_taken])

    def __str__(self):
        string = ""
        string += f"\nNumber of items: {self.num_items}, Capacity: {self.capacity}."
        string += "\nItems: "
        for item in sorted(self.items, key=lambda item: item.index):
            string += str(item)
        return string

class KnapsackSolution:
    """
    A solution (an individual) within the population of the Genetic algorithm.
    """
    def __init__(self, solution_str, score):
        self.solution_str = solution_str
        self.score = score

    def __str__(self):
        return f"Solution = {self.solution_str}, Score = {self.score}"

    def __lt__(self, other):
        return self.score < other.score
