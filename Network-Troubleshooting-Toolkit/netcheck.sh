#!/bin/bash
# ==========================================
# Advanced Network Diagnostics Script
# ==========================================

# ===== Colors =====
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
BLUE="\e[34m"
RESET="\e[0m"

# ===== Usage Check =====
if [ $# -eq 0 ]; then
  echo -e "${YELLOW}Usage: $0 host1 [host2 host3 ...]${RESET}"
  exit 1
fi

# ===== Logging =====
REPORT="network_report_$(date +%F_%H-%M-%S).txt"
exec > >(tee -a "$REPORT") 2>&1

# ===== Functions =====
{
ping_test() {
  echo "[1] PING TEST"
  if timeout 5 ping -c 4 -q $HOST >/dev/null 2>&1; then
    avg_time=$(ping -c 4 -q $HOST | grep -oP '(?<=/)[0-9.]+(?=/)' | awk 'NR==2 {print $1}')
    echo -e "${GREEN}Result: Host is UP${RESET}"
    echo "Average response time: ${avg_time} ms"
    PING_OK=true
  else
    echo -e "${RED}Result: Host is DOWN or unreachable${RESET}"
    PING_OK=false
  fi
  echo "..."
}

dns_test() {
  echo "[2] DNS RESOLUTION CHECK"
  IP_ADDRESS=$(timeout 5 dig +short $HOST | head -n 1)
  if [ -z "$IP_ADDRESS" ]; then
    echo -e "${RED}DNS Resolution: Failed${RESET}"
    DNS_OK=false
  else
    echo -e "IP Address: ${GREEN}$IP_ADDRESS${RESET}"
    echo "DNS Server: Working"
    DNS_OK=true
  fi
  echo "..."
}

route_test() {
  echo "[3] ROUTE TRACING"
  if command -v traceroute >/dev/null 2>&1; then
    ROUTE_OUTPUT=$(timeout 15 traceroute -m 15 $HOST 2>/dev/null)
    if [ $? -eq 0 ]; then
      echo "$ROUTE_OUTPUT"
      HOP_COUNT=$(echo "$ROUTE_OUTPUT" | grep -E '^[ 0-9]' | wc -l)
      echo "Total Hops: $HOP_COUNT"
    else
      echo -e "${RED}Traceroute failed${RESET}"
    fi
  else
    echo -e "${YELLOW}Traceroute not installed${RESET}"
  fi
  echo "..."
}

web_test() {
  echo "[4] WEB CONNECTIVITY"
  WEB_OK=false
  for PROTOCOL in http https; do
    URL="${PROTOCOL}://$HOST"
    STATUS_CODE=$(curl -I -s -o /dev/null -w "%{http_code}" --max-time 5 $URL)
    if [ "$STATUS_CODE" -eq 000 ]; then
      echo -e "${RED}$PROTOCOL: Unreachable${RESET}"
    else
      echo -e "${GREEN}$PROTOCOL: HTTP Status $STATUS_CODE${RESET}"
      WEB_OK=true
    fi
  done
  echo "..."
}

local_ports() {
  echo "[5] LOCAL PORT CHECK"
  if command -v ss >/dev/null 2>&1; then
    PORTS=$(ss -tuln)
  else
    PORTS=$(netstat -tuln)
  fi
  echo "$PORTS"
  echo ""
  echo "Common Services:"
  echo "$PORTS" | grep ":22 " >/dev/null && echo " - SSH (22)"
  echo "$PORTS" | grep ":80 " >/dev/null && echo " - HTTP (80)"
  echo "$PORTS" | grep ":443 " >/dev/null && echo " - HTTPS (443)"
  echo "$PORTS" | grep ":3306 " >/dev/null && echo " - MySQL (3306)"
  echo "..."
}

port_scan() {
  echo "[6] SPECIFIC PORT CHECK (22, 80, 443, 3306)"
  for PORT in 22 80 443 3306; do
    if nc -z -w2 $HOST $PORT 2>/dev/null; then
      echo -e "${GREEN}Port $PORT is OPEN${RESET}"
    else
      echo -e "${RED}Port $PORT is CLOSED${RESET}"
    fi
  done
  echo "..."
}

summary() {
  echo "=== SUMMARY ==="
  if [ "$PING_OK" = true ] && [ "$DNS_OK" = true ] && [ "$WEB_OK" = true ]; then
    echo -e "${GREEN}Target is REACHABLE${RESET}"
    echo -e "${GREEN}All checks PASSED ✅${RESET}"
  else
    echo -e "${RED}Some checks FAILED ❌${RESET}"
    [ "$PING_OK" != true ] && echo "- Ping test failed"
    [ "$DNS_OK" != true ] && echo "- DNS resolution failed"
    [ "$WEB_OK" != true ] && echo "- Web connectivity failed"
  fi
  echo ""
}

# ===== MAIN LOOP =====
for HOST in "$@"; do
  echo "===================================================="
  echo -e "${BLUE}=== NETWORK DIAGNOSTICS REPORT FOR $HOST ===${RESET}"
  echo "DATE: $(date)"
  echo "TARGET: $HOST"
  echo "----------------------------------------------------"

  ping_test
  dns_test
  route_test
  web_test
  local_ports
  port_scan
  summary
done
} > "$REPORT"
echo -e "${YELLOW}Results saved to $REPORT${RESET}"
