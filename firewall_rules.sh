#!/bin/bash
#
# firewall_rules.sh
# ------------------
# Traffic filtering for the student records server, laboratory environment.
# Run ONLY on the authorised lab machine/VM acting as the records server
# (or its gateway). Requires root (sudo).
#
# >>> Edit the variables below to match the values your assessor gave you <<<

IFACE="lo"                 # network interface facing the LAN
SERVICE_PORT="8080"           # the service specified by the assessor (e.g. 443 for HTTPS)
STAFF_NET="192.168.10.0/24"  # authorised staff subnet  -- EDIT ME
GUEST_NET="192.168.20.0/24"  # guest subnet             -- EDIT ME

set -e

echo "[*] Flushing existing rules for a clean state..."
iptables -F
iptables -X

echo "[*] Default policy: drop all inbound, allow outbound/established..."
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#iptables -A INPUT -i lo -j ACCEPT

echo "[*] (a) Block guest network access to the records server explicitly..."
iptables -A INPUT -i "$IFACE" -s "$GUEST_NET" -p tcp --dport "$SERVICE_PORT" -j DROP

echo "[*] (b) Permit staff network access to the specified service..."
iptables -A INPUT -i "$IFACE" -s "$STAFF_NET" -p tcp --dport "$SERVICE_PORT" -j ACCEPT

echo "[*] (c) Block all other inbound access to that service..."
iptables -A INPUT -i "$IFACE" -p tcp --dport "$SERVICE_PORT" -j DROP

echo "[*] Rules applied. Current INPUT chain:"
iptables -L INPUT -v -n --line-numbers
