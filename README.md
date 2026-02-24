# Self-Healing Infrastructure with Prometheus, Grafana, Alertmanager & Ansible

## Overview

This project implements a self-healing infrastructure system that automatically detects when a web service goes down and restores it without manual intervention.

The system continuously monitors service availability, generates alerts during failure, triggers automated recovery, and verifies restoration in real time.

This workflow mirrors real-world reliability engineering practices used in production environments.

---

## System Architecture

```
                    ┌────────────────────┐
                    │      Grafana       │
                    │  Visualization UI  │
                    └─────────▲──────────┘
                              │
                              │ queries metrics
                              │
                    ┌─────────┴──────────┐
                    │     Prometheus     │
                    │  Metrics Engine    │
                    └─────────▲──────────┘
                              │
                probe metrics │
                              │
                    ┌─────────┴──────────┐
                    │ Blackbox Exporter  │
                    │ Availability Probe │
                    └─────────▲──────────┘
                              │ HTTP check
                              │
                    ┌─────────┴──────────┐
                    │       NGINX        │
                    │    Web Service     │
                    └─────────┬──────────┘
                              │
                failure detected
                              │
                    ┌─────────▼──────────┐
                    │    Alertmanager    │
                    │   Alert Routing    │
                    └─────────▲──────────┘
                              │ POST alert
                              │
                    ┌─────────▼──────────┐
                    │     Webhook API    │
                    │  Trigger Handler   │
                    └─────────▲──────────┘
                              │ executes automation
                              │
                    ┌─────────▼──────────┐
                    │      Ansible       │
                    │ Recovery Automation│
                    └─────────▲──────────┘
                              │
                              │ restart service
                              │
                    ┌─────────▼──────────┐
                    │       NGINX        │
                    │   Service Restored │
                    └────────────────────┘
```

---

## Workflow Explained

1. The availability probe checks if the web service responds.
2. Prometheus collects probe metrics.
3. Alert rules detect downtime.
4. Alertmanager sends the alert to a webhook.
5. The webhook triggers an automation task.
6. The automation task restarts the service.
7. Monitoring confirms recovery.
8. Dashboards reflect real-time status.

---

## Technologies Used

| Tool              | Role                     |
| ----------------- | ------------------------ |
| Docker            | Containerized deployment |
| NGINX             | Sample web service       |
| Prometheus        | Monitoring & metrics     |
| Blackbox Exporter | HTTP health probing      |
| Alertmanager      | Alert routing            |
| Python Webhooks   | Alert trigger handler    |
| Ansible           | Automated recovery       |
| Grafana           | Visualization            |

---

## Step-by-Step Setup

### 1. Create a Monitoring Network

```bash
docker network create monitoring
```

**Purpose:**
Allows containers to communicate using service names instead of IP addresses.

---

### 2. Run the Web Service (NGINX)

```bash
docker run -d \
  --name nginx \
  --network monitoring \
  -p 8080:80 \
  nginx
```

**Purpose:**

* NGINX runs as the target service.
* Port 8080 allows browser access.
* Other containers access it using `nginx`.

---

### 3. Start Node Exporter (Host Metrics)

```bash
docker run -d \
  --name node-exporter \
  --network monitoring \
  prom/node-exporter
```

**Purpose:**
Provides CPU, memory, and system metrics for monitoring.

---

### 4. Start Blackbox Exporter (HTTP Monitoring)

```bash
docker run -d \
  --name blackbox \
  --network monitoring \
  -p 9115:9115 \
  prom/blackbox-exporter
```

**Purpose:**
Probes HTTP endpoints and reports availability metrics.

---

### 5. Start Alertmanager

```bash
docker run -d \
  --name alertmanager \
  --network monitoring \
  -p 9093:9093 \
  prom/alertmanager
```

**Purpose:**
Receives alerts and forwards them to automation systems.

---

### 6. Start Webhook Service

```bash
docker run -d \
  --name webhook \
  --network monitoring \
  -p 5001:5001 \
  webhook-image
```

**Purpose:**

* Receives alert notifications.
* Executes automation tasks.
* Triggers service recovery.

---

### 7. Start Prometheus

```bash
docker run -d \
  --name prometheus \
  --network monitoring \
  -p 9090:9090 \
  prom/prometheus
```

**Purpose:**

* Collects metrics from exporters.
* Evaluates alert rules.
* Sends alerts to Alertmanager.

---

### 8. (Optional) Start Grafana

```bash
docker run -d \
  --name grafana \
  --network monitoring \
  -p 3000:3000 \
  grafana/grafana
```

**Access:**
Open `http://localhost:3000`
Default login: admin / admin

Add Prometheus as a data source and import dashboards.

---

## Verifying the System

### Check containers

```bash
docker ps
```

### Check monitoring targets

Open:

```
http://localhost:9090/targets
```

All targets should show **UP**.

---

## Testing Self-Healing

### Simulate failure

```bash
docker stop nginx
```

### Expected sequence

1. Probe fails.
2. Alert fires.
3. Alertmanager sends webhook.
4. Webhook triggers automation.
5. NGINX restarts automatically.
6. Target returns to UP state.

---

## Troubleshooting Tips

**Check container logs**

```bash
docker logs prometheus
docker logs alertmanager
docker logs webhook
```

**Test webhook manually**

```bash
curl -X POST http://localhost:5001/webhook
```

**Verify probe**

```bash
curl "http://localhost:9115/probe?target=http://nginx&module=http_2xx"
```

---

## Summary

This project demonstrates a complete self-healing infrastructure workflow using monitoring, alerting, and automation. It replicates real-world DevOps reliability patterns and showcases automated incident response and service recovery.

---

## Future Improvements

* Slack/email notifications
* Kubernetes deployment
* Multi-service monitoring
* TLS security hardening
* Cloud deployment
* Auto-scaling integration
