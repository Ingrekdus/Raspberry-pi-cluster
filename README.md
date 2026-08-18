# Raspberry-pi-cluster
## WORK IN PROGRESS
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
* **Master (RP1):** `192.168.1.xxx`
* **Worker (RP2):** `192.168.1.xxx`
* **Worker (RP3):** `192.168.1.xxx`
* **Worker (RP4):** `192.168.1.xxx`

<img width="1910" height="782" alt="image" src="https://github.com/user-attachments/assets/be933ad1-dc41-4259-9882-cd7fd34b504b" />
