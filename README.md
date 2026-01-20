# Raspberry-pi-cluster

## Introduction
This repository documents my bachelor's project, which involved creating and configuring a cluster using Raspberry Pi 5.
Raspberry Pi is a popular platform for development and experimentation thanks to its low price, low power consumption, and broad community support. Creating a Raspberry Pi-based cluster allows you to simulate distributed systems, test parallel computations, or run applications in a multi-node environment. The goal of this work is to design, implement, and test a Raspberry Pi-based cluster capable of running distributed computing tasks and to evaluate its performance and potential uses.

## Architecture and hardware

### Hardware specification
* **4x Raspberry Pi 5:**  8 GB RAM.
* **4x Pimoroni NVMe Base:** 250 GB NVMe SSD disk
* **Network topologi:** Master-worker

### Topologie sítě a IP adresy
Our cluster has a simple topology with one master node and three workers.
* **Master (RP1):** `192.168.1.111`
* **Worker (RP2):** `192.168.1.103`
* **Worker (RP3):** `192.168.1.105`
* **Worker (RP4):** `192.168.1.107`

<img width="750" height="455" alt="image" src="https://github.com/user-attachments/assets/7d3e3345-ee39-45c5-8654-16f36c1b6602" />

<img width="1910" height="782" alt="image" src="https://github.com/user-attachments/assets/be933ad1-dc41-4259-9882-cd7fd34b504b" />

### Grafana and Prometheus
* Open a browser and go to your_ip:grana_port for me: 192.168.1.111:3000
* connections -> Data Sources -> click on Prometheus -> into connection URL paste your Prometheus URL, for me: http://192.168.1.111:9090 -> Save and test
* Dashboards -> + Create dashboards -> import dashboards -> paste 1860 -> load -> select Prometheus -> Import

<img width="1910" height="931" alt="image" src="https://github.com/user-attachments/assets/b482e91e-8b64-4a02-ab6d-554bb343eb94" />



2. The "Ultimate Guide"
3. 
Markdown
# Raspberry Pi 5 Supercomputer Cluster

Build your own high-performance computing (HPC) cluster using Raspberry Pi 5 and Docker Swarm. This project provides a ready-to-use environment for parallel computing and image processing.

## Prerequisites
1. **Hardware:** 2 or more Raspberry Pi 5 boards (recommended 8GB RAM).
2. **OS:** Raspberry Pi OS Lite (64-bit) installed on all nodes.
3. **Network:** All nodes must be on the same local network with static IPs.

## Quick Start Guide (5 Minutes)

### Step 1: Install Docker (All Nodes)
Log in to each Pi and run the installation script provided in this repo:
```bash
curl -sSL [https://raw.githubusercontent.com/YOUR_USERNAME/pi-cluster-optimization/main/infra/setup/install_docker.sh](https://raw.githubusercontent.com/YOUR_USERNAME/pi-cluster-optimization/main/infra/setup/install_docker.sh) | sh
Step 2: Initialize the Cluster (Master Only)
On your primary node (RP1), run:

Bash
docker swarm init --advertise-addr <YOUR_MASTER_IP>
Copy the command that appears (starting with docker swarm join) and run it on all other nodes (RP2, RP3, etc.).

Step 3: Deploy Your First App (Master Only)
Download the project and launch the Pi estimation task:

Bash
git clone [https://github.com/YOUR_USERNAME/pi-cluster-optimization.git](https://github.com/YOUR_USERNAME/pi-cluster-optimization.git)
cd pi-cluster-optimization/apps/pi-estimation

# Build the image on ALL nodes (or use a registry)
docker build -t pi-cluster-image .

# Deploy to the cluster
docker stack deploy -c docker-compose.yml pi_calc
Monitoring & Results
Check the status of your tasks:

Bash
docker service ps pi_calc_pi-worker
View the parallel output:

Bash
docker service logs -f pi_calc_pi-worker
