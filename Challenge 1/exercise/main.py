import math

# Define the set of points
points = {
    1: (1, 2),
    2: (10, 3),
    3: (4, 8),
    4: (15, 7),
    5: (6, 1),
    6: (9, 12),
    7: (14, 4),
    8: (3, 10),
    9: (7, 7),
    10: (12, 14),
}

# Sink node
# sink_node = (20, 20)
sink_node = (6.9, 7.6)

# Compute energy for each point
def compute_energy(points, ref_point):
    results = {}
    for idx, (x, y) in points.items():
        d = math.sqrt((x - ref_point[0]) ** 2 + (y - ref_point[1]) ** 2)
        energy = 2000 * (50 + (d**2)) / 1000000
        results[idx] = (d, energy)
    return results

if __name__ == "__main__":
    energies = compute_energy(points, sink_node)
    for idx, (distance, energy) in energies.items():
        print(
            f"Point {points[idx]}: distance from the sink node: {distance:.2f}, energy consumption at each transmission = {energy:.2f} mJ"
        )
