#!/usr/bin/env python3
import psutil
import boto3
import logging
from datetime import datetime
import socket
# --------------------------
# Configuration
# --------------------------
LOG_FILE = "/var/log/system_health.log"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:SystemAlerts"  # Replace with your SNS topic ARN
INSTANCE_NAME = socket.gethostname()
# Thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80
PROCESS_THRESHOLD = 200
# --------------------------
# Setup logging
# --------------------------
logging.basicConfig(filename=LOG_FILE,
                   level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
sns_client = boto3.client('sns', region_name='us-east-1')
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
# --------------------------
# Function to publish SNS alert
# --------------------------
def send_sns_alert(subject, message):
   try:
       sns_client.publish(
           TopicArn=SNS_TOPIC_ARN,
           Subject=subject,
           Message=message
       )
       print(f"SNS Alert sent: {subject}")
   except Exception as e:
       print(f"Failed to send SNS alert: {e}")
       logging.error(f"Failed to send SNS alert: {e}")
# --------------------------
# Function to push metrics to CloudWatch
# --------------------------
def push_to_cloudwatch(metric_name, value):
   try:
       cloudwatch.put_metric_data(
           Namespace='Custom/SystemHealth',
           MetricData=[
               {
                   'MetricName': metric_name,
                   'Dimensions': [
                       {
                           'Name': 'InstanceName',
                           'Value': INSTANCE_NAME
                       },
                   ],
                   'Value': value,
                   'Unit': 'Percent'
               },
           ]
       )
   except Exception as e:
       logging.error(f"Failed to push metric {metric_name} to CloudWatch: {e}")
# --------------------------
# Monitoring Functions
# --------------------------
def check_cpu():
   cpu_usage = psutil.cpu_percent(interval=1)
   push_to_cloudwatch("CPUUsage", cpu_usage)
   if cpu_usage > CPU_THRESHOLD:
       alert = f"High CPU Usage detected: {cpu_usage}% on {INSTANCE_NAME}"
       logging.warning(alert)
       send_sns_alert("High CPU Usage Alert", alert)
   return cpu_usage
def check_memory():
   memory = psutil.virtual_memory()
   memory_usage = memory.percent
   push_to_cloudwatch("MemoryUsage", memory_usage)
   if memory_usage > MEMORY_THRESHOLD:
       alert = f"High Memory Usage detected: {memory_usage}% on {INSTANCE_NAME}"
       logging.warning(alert)
       send_sns_alert("High Memory Usage Alert", alert)
   return memory_usage
def check_disk():
   disk = psutil.disk_usage('/')
   disk_usage = disk.percent
   push_to_cloudwatch("DiskUsage", disk_usage)
   if disk_usage > DISK_THRESHOLD:
       alert = f"High Disk Usage detected: {disk_usage}% on {INSTANCE_NAME}"
       logging.warning(alert)
       send_sns_alert("High Disk Usage Alert", alert)
   return disk_usage
def check_processes():
   processes = len(psutil.pids())
   push_to_cloudwatch("ProcessCount", processes)
   if processes > PROCESS_THRESHOLD:
       alert = f"High number of running processes detected: {processes} on {INSTANCE_NAME}"
       logging.warning(alert)
       send_sns_alert("High Process Count Alert", alert)
   return processes
# --------------------------
# Main Function
# --------------------------
def main():
   print("Starting System Health Monitoring...")
   logging.info("System Health Monitoring started")
   cpu = check_cpu()
   memory = check_memory()
   disk = check_disk()
   processes = check_processes()
   # Log current system stats
   logging.info(f"CPU Usage: {cpu}% | Memory Usage: {memory}% | Disk Usage: {disk}% | Processes: {processes}")
   print(f"CPU: {cpu}% | Memory: {memory}% | Disk: {disk}% | Processes: {processes}")
   logging.info("System Health Monitoring completed")
if __name__ == "__main__":
   main()
