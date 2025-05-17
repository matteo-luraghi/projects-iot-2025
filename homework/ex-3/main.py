import itertools
import matplotlib.pyplot as plt

# number of tags
N = 4

# pre-computed L0, L1, L2, L3
L = {
    0: 0,
    1: 1,
    2: 4,
    3: 51 / 8,
}

# returns a dict mapping number of successful slots s (0…N)
# to P{S=s} when N tags pick uniformly among r slots.
def compute_prob_dist(r):
    outcomes = itertools.product(range(r), repeat=N)
    total = r**N
    distribution = {}
    for outcome in outcomes:
        # count how many slots were chosen exactly once
        counts = [outcome.count(slot) for slot in range(r)]
        successes = sum(1 for c in counts if c == 1)
        distribution[successes] = distribution.get(successes, 0) + 1
    # convert counts to probabilities
    for s in distribution:
        distribution[s] /= total
    return distribution

# compute L4 by solving the recursion for r = 4:
dist4 = compute_prob_dist(4)
P0 = dist4.get(0, 0)
# numerator = r + sum_{s=1..3} P(S=s) * L_{4−s}
num = 4 + sum(dist4.get(s, 0) * L[4 - s] for s in range(1, 4))
# then L4 = num / (1 − P0)
L[4] = num / (1 - P0)

# for each initial frame size r1 compute E[T] and η
results = []
for r1 in range(1, 7):
    dist = compute_prob_dist(r1)
    # E[T]
    expected_resolution_time = r1 + sum(dist.get(s, 0) * L[N - s] for s in dist)
    # η = N / E[T]
    eta = N / expected_resolution_time
    results.append({"r1": r1, "E[T]": expected_resolution_time, "η": eta})

print(results)

# display results
r1_values = list(range(1, 7))
etas = [results[i]["η"] for i in range(0, 6)]
plt.figure()
plt.plot(r1_values, etas, marker="o")
plt.xlabel("Initial Frame Size r1")
plt.ylabel("Efficiency η")
plt.title("Efficiency over values of initial frame size")
plt.grid(True)
plt.xticks(r1_values)
plt.tight_layout()
plt.show()
