# Title
Runbook to remediate RDS EBS volume size alert

## Issue
PostgreSQL database instance is running out of storage space.

## Description
This run book provides the step by step instructions to increase the RDS EBS volume size if it runs out of space
Follow the instrctions in this run book to remediate the issues related to the low storage.

## Steps

1. Check if the RDS instance is in available state. If the status is available, continue otherwise abort the process.

2. Get the current storage space. 

3. Get the allocated storage space.

4. Check if the current storage space is more than 90% of the allocated storage space, then increase the volume by 30%. If not increase the volume by 20%



