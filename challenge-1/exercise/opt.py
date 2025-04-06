import numpy as np
from itertools import product

def max_distance_for_sink(x_sink, y_sink, points):
    # computes the maximum distance from a possible sink node to any sensor
    return max(np.sqrt((x - x_sink) ** 2 + (y - y_sink) ** 2) for x, y in points)

def find_optimal_sink_position(points):
    # finds the optimal sink node position by minimizing the maximum distance
    x_min = min(x for x, _ in points)
    x_max = max(x for x, _ in points)
    y_min = min(y for _, y in points)
    y_max = max(y for _, y in points)
    
    best_x, best_y, min_max_distance = None, None, float('inf')
    
    for x_sink, y_sink in product(np.arange(x_min, x_max + 0.1, 0.1), 
                                  np.arange(y_min, y_max + 0.1, 0.1)):
        max_dist = max_distance_for_sink(x_sink, y_sink, points)
        if max_dist < min_max_distance:
            min_max_distance = max_dist
            best_x, best_y = x_sink, y_sink
    
    return best_x, best_y

if __name__ == "__main__":
    points = [
        (1, 2),
        (10, 3),
        (4, 8),
        (15, 7),
        (6, 1),
        (9, 12),
        (14, 4),
        (3, 10),
        (7, 7),
        (12, 14),
    ]
    
    best_x, best_y = find_optimal_sink_position(points)
    print(f"Optimal Sink Position: ({best_x:.2f}, {best_y:.2f})")
