# Problem Statement 2 - System Health Monitoring

## Objective
This Python script monitors a Linux system's health by checking:
- CPU usage
- Memory usage
- Disk usage
- Number of running processes

If any of these metrics exceed predefined thresholds, an alert is sent to AWS SNS and metrics are pushed to CloudWatch.

---

## Architecture

+----------------------+
|   EC2 Instance       |
|----------------------|
| Python Script        |
| - CPU, Memory, Disk  |
| - Running Processes  |
|                      |
| Thresholds -> SNS    |
+-----------+----------+
           |
           v
  +----------------+
  | SNS Topic      |
  | - Email Alerts |
  | - SMS Alerts   |
  +----------------+
           |
           v
  +----------------+
  | CloudWatch     |
  | - Metrics      |
  | - Dashboards   |
  +----------------+



1. Update the `SNS_TOPIC_ARN` with your SNS topic.
2. Run the script:

```bash
python3 system_health_monitor.py
Check logs at /var/log/system_health.log

Features

Monitors CPU, Memory, Disk, and Processes

Sends alerts via AWS SNS

Pushes metrics to AWS CloudWatch

Logs all activities locally




### 2. Application Health Checker
- Bash script: `scripts/application_health_checker.sh`
- Checks if an application is running on port 4499
- Prints "UP" if application responds with HTTP 200, else prints "DOWN"

## Architecture

![System Health Monitoring Architecture](images/Image.png)

## Usage

### System Health Monitoring
```bash
python3 scripts/system_health_monitor.py