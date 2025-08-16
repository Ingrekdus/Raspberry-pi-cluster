# Raspberry-pi-cluster

## Úvod
Tento repozitář dokumentuje můj bakalářský projekt - vytvoření a konfiguraci clusteru z Raspberry Pi 5. Hlavním cílem je demonstrovat využití distribuovaných systémů pro běh aplikací, v mém případě jednoduché point-and-click hry "Šmucik".

## Architektura a hardware

### Hardwarová specifikace
* **4x Raspberry Pi 5:** Každé s 8 GB RAM.
* **4x Pimoroni NVMe Base:** Pro připojení 250 GB NVMe SSD disků.
* **Síťová topologie:** Master-worker (jednotlivé uzly jsou propojeny pomocí sítě, která je popsána níže).

### Topologie sítě a IP adresy
Náš cluster má jednoduchou topologii s jedním master uzlem a třemi workery.
* **Master (RP1):** `192.168.1.111`
* **Worker (RP2):** `192.168.1.103`
* **Worker (RP3):** `192.168.1.105`
* **Worker (RP4):** `192.168.1.107`

Hardware:
4x Raspberry Pi 5 with active cooling and 250gb ssd disk
Router
swtich

<img width="750" height="455" alt="image" src="https://github.com/user-attachments/assets/7d3e3345-ee39-45c5-8654-16f36c1b6602" />
<img width="1910" height="782" alt="image" src="https://github.com/user-attachments/assets/be933ad1-dc41-4259-9882-cd7fd34b504b" />

