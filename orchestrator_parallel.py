import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import os
import time

# Nastavení logování
logging.basicConfig(filename='logs/orchestrator.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

def build_docker_image(image_name, dockerfile_path):
    logging.info(f"Building Docker image {image_name} from {dockerfile_path}")
    subprocess.run(["docker", "build", "-t", image_name, dockerfile_path], check=True)
    logging.info(f"Docker image {image_name} built successfully")

def run_task_in_docker(image_name, payload):
    logging.info(f"Running task in docker with payload: {payload}")
    result = subprocess.run(["docker", "run", "--rm", image_name, payload],
                            capture_output=True, text=True)
    if result.returncode == 0:
        logging.info(f"Task completed successfully: {result.stdout.strip()}")
    else:
        logging.error(f"Task failed: {result.stderr.strip()}")
    return result.returncode

def main():
    # Načti konfiguraci
    with open("task_config.json") as f:
        config = json.load(f)

    image_name = config["name"] + "_image"
    dockerfile_path = config["dockerfile_path"]
    num_workers = config["num_workers"]
    tasks = config["tasks"]

    # Build docker image
    build_docker_image(image_name, dockerfile_path)

    # Paralelní spuštění úloh pomocí ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for task in tasks:
            payload = task["payload"]
            futures.append(executor.submit(run_task_in_docker, image_name, payload))

        # Sledování dokončení úloh
        for future in as_completed(futures):
            try:
                result_code = future.result()
                logging.info(f"Task finished with exit code {result_code}")
            except Exception as e:
                logging.error(f"Exception during task execution: {e}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    total_time = time.time() - start_time
    print(f"All tasks completed in {total_time:.2f} seconds")
    logging.info(f"All tasks completed in {total_time:.2f} seconds")
