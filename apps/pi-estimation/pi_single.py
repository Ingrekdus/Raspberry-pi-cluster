import random, socket, time
def estimate_pi(n):
    hits = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1.0:
            hits += 1
    return hits

samples = 10000000
start = time.time()
hits = estimate_pi(samples)
end = time.time()
print(f"Node: {socket.gethostname()}, Hits: {hits}, Samples: {samples}, Time: {end-start:.4f}")