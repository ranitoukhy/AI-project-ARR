import heapq

class PriorityQueue:
    """
    A Priority Queue for managing the A* search.
    """
    def __init__(self, priority_function):
        self.heap = []
        self.priority_function = priority_function

    def push(self, item):
        heapq.heappush(self.heap, (self.priority_function(item), item))

    def pop(self):
        _, item = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

def state_cost(state):
    """
    Returns the cost of the given KnapsackState.
    A state's cost is negative the sum of values of the items taken in the state.
    :param state: The KnapsackState object to calculate the cost of.
    :return: The cost of the given state.
    """
    return -state.value

def heuristic(state):
    """
    Returns the heuristic value of the given KnapsackState.
    This value is negative the solution of a Knapsack problem, where:
        1. The capacity of the Knapsack is the given state's remaining capacity, and
        2. The items available are the state's items left.
    :param state: The KnapsackState object to calculate the heuristic value of.
    :return: The heuristic value of the given state.
    """
    total_value = 0.0
    remaining_capacity = state.capacity
    
    if state.current_item is not None:
        total_value += state.current_item.value
        remaining_capacity -= state.current_item.weight

    for item in state.items_left:
        if remaining_capacity == 0:
            break
        if item.weight <= remaining_capacity:
            total_value += item.value
            remaining_capacity -= item.weight
        else:
            total_value += item.value * (remaining_capacity / item.weight)
            break
    
    return -total_value

def priority_func(state):
    """
    The priority function of a state, for managing the state within a PriorityQueue during A* search.
    It is the addition of the state's cost and the heuristic value of the state.
    :param state: The state to calculate the priority of.
    :return: The priority value of the state (the sum of the state's cost and heuristic value).
    """
    return state_cost(state) + heuristic(state)
