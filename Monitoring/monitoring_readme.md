# Monitoring Raspberry Pi Swarm Clusteru

## Přehled

Monitoring stack sleduje výkon clusteru v reálném čase pomocí:
- **Prometheus** — shromažďuje metriky (CPU, RAM, disk, teplota)
- **Grafana** — vizualizuje metriky v dashboardu
- **node-exporter** — exportuje HW metriky každého nodu
- **cAdvisor** — exportuje metriky kontejnerů

Všechny komponenty běží v `docker-compose` (ne v Swarm) s `network_mode: host` — to zajišťuje stabilní síťové adresy a přístup k `/dev/thermal_zone0` (teplota RPi).

---

## Architektura

```
┌─────────────────────────────────────────────────────────────┐
│                    RP1 (Manager)                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Docker Compose (host network)                       │   │
│  │ ├─ Prometheus:9090 (scrapes 9100, 8080 on LAN)    │   │
│  │ ├─ Grafana:3000 (datasource → localhost:9090)     │   │
│  │ ├─ node-exporter:9100 (CPU, RAM, disk, temp)      │   │
│  │ └─ cAdvisor:8080 (kontejnery)                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↑
                    scrapes přes LAN
                              ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│     RP2 (Worker) │  │     RP3 (Worker) │  │     RP4 (Worker) │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ node-exporter    │  │ node-exporter    │  │ node-exporter    │
│ :9100            │  │ :9100            │  │ :9100            │
│                  │  │                  │  │                  │
│ cAdvisor :8080   │  │ cAdvisor :8080   │  │ cAdvisor :8080   │
└──────────────────┘  └──────────────────┘  └──────────────────┘
  192.168.1.103        192.168.1.105        192.168.1.107
```

---

## Instalace

### 1. Předpoklady

- Docker a Docker Compose na všech 4 nodech
- SSH přístup k RP1–RP4
- LAN IP adresy nakonfigurované (viz [02_KONFIGURACE.md](./02_KONFIGURACE.md))
  - RP1 = `<RP1_IP>` (Manager)
  - RP2 = `<RP2_IP>` (Worker)
  - RP3 = `<RP3_IP>` (Worker)
  - RP4 = `<RP4_IP>` (Worker)

### 2. Na RP1: Prometheus + Grafana

Vytvořit `docker-compose.yml` v adresáři `monitoring/` na RP1:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    network_mode: host
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    network_mode: host
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

Vytvořit `prometheus.yml` ve stejném adresáři (upravit IP adresy podle tvé sítě):

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # node-exporter na všech nodech
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['<RP1_IP>:9100']
        labels:
          node: 'RP1'
      - targets: ['<RP2_IP>:9100']
        labels:
          node: 'RP2'
      - targets: ['<RP3_IP>:9100']
        labels:
          node: 'RP3'
      - targets: ['<RP4_IP>:9100']
        labels:
          node: 'RP4'

  # cAdvisor na všech nodech
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['<RP1_IP>:8080']
        labels:
          node: 'RP1'
      - targets: ['<RP2_IP>:8080']
        labels:
          node: 'RP2'
      - targets: ['<RP3_IP>:8080']
        labels:
          node: 'RP3'
      - targets: ['<RP4_IP>:8080']
        labels:
          node: 'RP4'
```

Spustit:
```bash
cd cluster/monitoring
docker-compose up -d
docker-compose logs -f prometheus  # Ověřit, že startuje
```

**Přístup:**
- Grafana: `http://<RP1_IP>:3000` (admin/admin)
- Prometheus: `http://<RP1_IP>:9090`

> **⚠️ Bezpečnost:** Po prvním přihlášení do Grafany změň heslo admina!

### 3. Na RP2–RP4: node-exporter + cAdvisor

Vytvořit stejný soubor `docker-compose.yml` na RP2, RP3, RP4 (v `cluster/monitoring/`):

```yaml
version: '3.8'

services:
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    network_mode: host
    command:
      - '--path.rootfs=/'
      - '--path.procfs=/proc'
      - '--path.sysfs=/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
      - '--collector.hwmon'
    volumes:
      - /:/rootfs:ro
      - /proc:/proc:ro
      - /sys:/sys:ro
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    network_mode: host
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    restart: unless-stopped
```

Spustit na každém workeru:
```bash
cd cluster/monitoring
docker-compose up -d
docker-compose logs cadvisor  # Ověřit, že startuje bez errors
```

---

## Proč Docker Compose (ne Swarm)?

| Aspekt | Docker Swarm | Docker Compose (host) |
|--------|--------------|----------------------|
| **Overlay síť** | Mění IP adresy po restartu clusteru | Fixní LAN IP — stabilní |
| **Prometheus scrapes** | Hardcoded overlay IPs se přeruší | Vždycky funguje |
| **Teplota RPi (`/dev/thermal_zone0`)** | Není přístupná z Swarm kontejneru | Přístupná s `network_mode: host` |
| **Hostname (`node_uname_info`)** | `uts: host` není v Swarm | Pracuje přesně |

**Výsledek:** Monitoring je **na production-grade úrovni** bez workaroundů.

---

## Metriky v Dashboardu

### CPU
```promql
100 - (avg by (node) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```
Zobrazuje % využití CPU na každém nodu.

### RAM
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```
% využitá paměť.

### Teplota (RPi5)
```promql
node_hwmon_temp_celsius{chip="thermal_thermal_zone0"}
```
Fyzická teplota čipu v °C. **Klíč:** Filtr na `chip="thermal_thermal_zone0"` — bez toho jsou nesmysly.

### Disk
```promql
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100
```
% obsazený disk.

### Kontejnery (cAdvisor)
```promql
rate(container_cpu_usage_seconds_total[5m]) * 100
```
CPU čas v kontejnerech.

---

## Troubleshooting

### "Prometheus scrapes hlásí connection refused"
**Příčina:** node-exporter nebo cAdvisor neběží na workeru.
```bash
# Na workeru zkontroluj:
docker ps | grep -E 'node-exporter|cadvisor'
docker-compose logs node-exporter
```

### "Grafana se nedaří připojit k Prometheus"
**Příčina:** Grafana datasource ukazuje na `http://prometheus:9090` (DNS s `network_mode: host` neexistuje).
**Řešení:** V Grafana (Settings → Data Sources → Prometheus) změnit na `http://localhost:9090`.

### "Teplota ukazuje nesmysly nebo 0"
**Příčina:** Chybí `--collector.hwmon` nebo filtr na `chip=`.
```bash
# Na RP1 ověřit query:
curl http://localhost:9090/api/v1/query?query=node_hwmon_temp_celsius
```

### "node-exporter se crashuje se 'permission denied'"
**Příčina:** Kontejner potřebuje přístup ke `/proc`, `/sys`, `/dev`.
```bash
# Ověřit volumes v docker-compose.yml:
- /proc:/proc:ro
- /sys:/sys:ro
- /dev/disk/:/dev/disk:ro
```

---

## Příští kroky

1. **Importuj dashboard** (`rpi_cluster_dashboard_v3_labels.json`) do Grafany
2. **Nastav alerting** (Grafana Alerts) na teplotu > 80°C
3. **Archivuj data** — Prometheus drží metriky ~30 dní defaultně

---

## Screenshot

[Vlož screenshot dashboardu sem — měl by ukazovat CPU, RAM, disk a teplotu na všech 4 nodech přehledně]
