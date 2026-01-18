import sys
import random
import json

def estimate_pi_part(num_samples):
    """
    Simuluje "házení šipek" a vrací počet zásahů do kruhu.
    """
    inside_circle = 0
    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2
        if distance <= 1:
            inside_circle += 1
    
    return inside_circle

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Použití: python pi_worker.py <pocet_simulaci>")
        sys.exit(1)
        
    try:
        num_samples = int(sys.argv[1])
    except ValueError:
        print("Počet simulací musí být celé číslo.")
        sys.exit(1)
        
    hits = estimate_pi_part(num_samples)
    
    result = {
        "hits": hits,
        "samples": num_samples
    }
    print(json.dumps(result))