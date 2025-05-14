import random

def generate_lottery_grid():
    grid = []
    for i in range(100):  # from 00 to 99
        prefix = f"{i:02d}"  # 2-digit prefix
        suffix = f"{random.randint(0, 99):02d}"  # random 2-digit suffix
        full_number = prefix + suffix  # combine to get 4-digit number
        grid.append(full_number)
    return [grid[i:i+10] for i in range(0, 100, 10)]