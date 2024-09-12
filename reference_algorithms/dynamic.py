class Solution:
    def __init__(self, items):
        self.items = items
        self.value = sum([item.value for item in items])

def dynamic_programming(problem):
    solutions = [[None for _ in range(int(problem.capacity)+1)] for _ in range(problem.num_items+1)]
    for i in range(problem.num_items+1):
        solutions[i][0] = Solution(list())
    for j in range(int(problem.capacity)+1):
        solutions[0][j] = Solution(list())
    
    for i in range(1, problem.num_items+1):
        for j in range(1, int(problem.capacity)+1):
            without_i = solutions[i-1][j]
            with_i = Solution(list())
            if j >= problem.items[i-1].weight:
                with_i = Solution(solutions[i-1][j - int(problem.items[i-1].weight)].items + [problem.items[i-1]])
            solutions[i][j] = with_i if with_i.value > without_i.value else without_i
    
    return solutions[-1][-1].value, set(solutions[-1][-1].items)
