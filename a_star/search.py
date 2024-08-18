import heapq
from math import inf

class PriorityQueue:
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
    return -state.value

def heuristic(state):
    total_value = 0.0
    remaining_capacity = state.capacity
    
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
    return state_cost(state) + heuristic(state)

def a_star_search(problem):
    fringe = PriorityQueue(priority_func)
    fringe.push(problem.get_start_state())
    visited_states = set()
    while not fringe.isEmpty():
        state = fringe.pop()
        if problem.is_goal_state(state):
            return state.value, state.items_taken
        if state in visited_states:
            continue
        visited_states.add(state)
        for successor in problem.get_successors(state):
            if successor not in visited_states:
                fringe.push(successor)
