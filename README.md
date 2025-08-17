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
