import subprocess
import json
import concurrent.futures
import time

WORKERS = {
    "192.168.1.103": "RP2",
    "192.168.1.105": "RP3",
    "192.168.1.107": "RP4"
}
TOTAL_SAMPLES = 40000000

def run_ssh_command(ip, user, command):
    """
    Spustí SSH příkaz na dané IP adrese s daným uživatelem a vrátí výstup.
    """
    try:
        ssh_command = ["ssh", f"{user}@{ip}", command]
        result = subprocess.run(ssh_command, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            if "timed out" not in result.stderr:
                print(f"Chyba na {ip} pod uživatelem {user}: {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"Chyba připojení k {ip}: {e}")
        return None

def get_available_workers():
    """
    Zkontroluje dostupnost všech workerů a vrátí slovník dostupných.
    """
    print("Kontrola dostupnosti workerů...")
    available_workers = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_ssh_command, ip, user, 'uptime'): (ip, user) for ip, user in WORKERS.items()}
        for future in concurrent.futures.as_completed(futures):
            ip, user = futures[future]
            if future.result():
                print(f"  - Worker na {ip} (uživatel {user}) je online.")
                available_workers[ip] = user
            else:
                print(f"  - Worker na {ip} (uživatel {user}) je OFFLINE.")
    return available_workers

def main():
    start_time = time.time()
    
    available_workers = get_available_workers()
    if not available_workers:
        print("Žádný worker není dostupný. Ukončuji.")
        return

    num_workers = len(available_workers)
    samples_per_worker = TOTAL_SAMPLES // num_workers

    print(f"\nDistribuuji {TOTAL_SAMPLES:,} simulací mezi {num_workers} workerů ({samples_per_worker:,} na každého).")

    total_hits = 0
    total_samples_processed = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_ssh_command, ip, user, f'docker run --rm pi_worker:latest {samples_per_worker}'): ip for ip, user in available_workers.items()}
        
        for future in concurrent.futures.as_completed(futures):
            ip = futures[future]
            result_json = future.result()
            
            if result_json:
                try:
                    data = json.loads(result_json)
                    hits = data['hits']
                    samples = data['samples']
                    total_hits += hits
                    total_samples_processed += samples # Sečteme úspěšně dokončené simulace
                    print(f"  - Získán výsledek od {ip}: {hits:,} zásahů z {samples:,} pokusů.")
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Chyba při zpracování JSON výsledku od {ip}: {e}")
            else:
                print(f"  - Worker {ip} selhal nebo se nepodařilo získat výsledek.")
                
    if total_samples_processed > 0:
        estimated_pi = 4 * (total_hits / total_samples_processed)
    else:
        estimated_pi = 0.0
    
    end_time = time.time()
    
    print("\n" + "="*40)
    print("VÝSLEDEK")
    print("="*40)
    print(f"Celkový počet pokusů: {total_samples_processed:,}")
    print(f"Celkový počet zásahů: {total_hits:,}")
    print(f"Odhadovaná hodnota Pi: {estimated_pi}")
    print(f"Výpočet trval: {end_time - start_time:.2f} sekund")
    print("="*40)

if __name__ == "__main__":
    main()