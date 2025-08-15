import time
import sys

def heavy_computation(payload):
    # Simulace těžké výpočetní úlohy
    print(f"Processing payload: {payload}")
    time.sleep(5)  # simulace zátěže 5 sekund
    print(f"Finished processing: {payload}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        heavy_computation(sys.argv[1])
    else:
        print("No payload provided")
