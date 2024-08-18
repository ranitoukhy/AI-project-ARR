class KnapsackItem:
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight
    
    def __str__(self):
        return f"\n    {self.index}. Value: {self.value}, Weight: {self.weight}"

    def __repr__(self):
        return self.__str__()

class State:
    def __init__(self, value, capacity, current_item, items_taken, items_left):
        self.value = value
        self.capacity = capacity
        self.current_item = current_item
        self.items_taken = items_taken
        self.items_left = items_left

    def __key(self):
        return (self.current_item, self.items_taken)
    
    def __lt__(self, _):
        return True
    
    def __hash__(self):
        return hash(self.__key())
    
    def __eq__(self, other):
        return self.__key() == other.__key()

    def __str__(self):
        return f"\n<STATE> Total value: {self.value}, Capacity: {self.capacity}," + \
             f"\nIndices taken: {sorted(self.items_taken, key=lambda item: item.index)}, " + \
             f"\nIndices left: {sorted(self.items_left, key=lambda item: item.index)}"

    def __repr__(self):
        return self.__str__()

class KnapsackProblem:
    def __init__(self, filepath):
        self.items = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        num_items, capacity = lines[0].split()
        self.num_items = int(num_items)
        self.capacity = float(capacity)
        for index, line in enumerate(lines[1:]):
            if index == self.num_items:
                break
            value, weight = map(float, line.split())
            if weight > self.capacity:
                continue
            self.items.append(KnapsackItem(index+1, value, weight))
        self.items = sorted(self.items, key=lambda item: item.value / item.weight, reverse=True)
    
    def get_start_state(self):
        start_state = State(0, self.capacity, self.items[0], frozenset(), self.items[1:])
        return start_state

    def is_goal_state(self, state):
        return state.current_item is None

    def get_successors(self, state):
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
