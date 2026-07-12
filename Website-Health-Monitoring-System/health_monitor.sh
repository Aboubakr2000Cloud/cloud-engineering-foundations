#!/bin/bash

# ============================================
# Website Health Monitor
# Checks website availability and generates reports
# ============================================

# Configuration

GREEN="\e[32m"
RED="\e[31m"
RESET="\e[0m"


CONFIG_FILE="/home/abou/cloud-learning-project/configs/websites.conf"
LOG_FILE="/home/abou/cloud-learning-project/logs/health.log"
ERROR_LOG="/home/abou/cloud-learning-project/logs/errors.log"

# ============================================
# FUNCTIONS
# ============================================

run_health_checks() {

echo "=== Websites Checks ===="

while IFS=',' read -r url name max_time; do
    RESPONSE=$(curl -I -s -o /dev/null -w "%{http_code},%{time_total}" --max-time 10 "$url")
    STATUS_CODE=$(echo "$RESPONSE" | cut -d',' -f1)
    RESPONSE_TIME=$(echo "$RESPONSE" | cut -d',' -f2 | awk '{printf "%.0f", $1*1000}')
    if [ "$RESPONSE_TIME" -lt "$max_time" ]; then
    SPEED="${GREEN}FAST${RESET}"
    else
    SPEED="${RED}SLOW${RESET}"
    fi
    if [ "$STATUS_CODE" -eq 000 ]; then
    LOG_MSG1="[$(date '+%F %H:%M:%S')] $name - ---- (status: ${RED}Unreachable (FAILED)${RESET}, TIME: ----)" 
    echo -e "$LOG_MSG1" >> "$LOG_FILE"
    echo -e "$LOG_MSG1" >> "$ERROR_LOG"
    elif [ "$STATUS_CODE" -ge 200 ] && [ "$STATUS_CODE" -lt 400 ]; then
    echo -e "[$(date '+%F %H:%M:%S')] $name - $SPEED (status: ${GREEN}$STATUS_CODE (SUCCESS)${RESET}, TIME: ${RESPONSE_TIME}ms)" >> "$LOG_FILE"
    else
    LOG_MSG2="[$(date '+%F %H:%M:%S')] $name -$SPEED (status: ${RED}$STATUS_CODE (FAILED)${RESET}, TIME: ${RESPONSE_TIME}ms)"       
    echo -e "$LOG_MSG2" >> "$LOG_FILE"
    echo -e "$LOG_MSG2" >> "$ERROR_LOG"

    fi
done < "$CONFIG_FILE"
echo ""
    echo "✓ Health checks completed!"
    echo "Results saved to: $LOG_FILE"
    echo ""
    echo "To view results: cat $LOG_FILE"
    echo "To view errors only: cat $ERROR_LOG"
}

generate_report() {

echo "=== Daily Report ==="

{
total_checks=$(grep -c "$(date +%F)" "$LOG_FILE")
echo "Total checks performed: $total_checks"
SUCCESS_TOTAL=$(grep "$(date +%F)" "$LOG_FILE" | grep -c "SUCCESS")
SUCCESS_RATE=$(("$SUCCESS_TOTAL" * 100 / "$total_checks"))
echo "Success rate: $SUCCESS_RATE%"
AVG_TIME=$(grep "$(date +%F)" "$LOG_FILE" | grep "SUCCESS" | grep -o '[0-9]\+ms' | sed 's/ms//' | awk '{sum += $1; count++} END {if(count>0) print int(sum/count); else print 0}')
echo "Average response time: ${AVG_TIME}ms"
echo "Sites with issues:"
echo "- Unreachable Sites"
grep "$(date +%F)" "$LOG_FILE" | grep 'Unreachable' | awk '{print $3}' | sort -u
echo "- Failed Sites (HTTP Errors)"
grep "$(date +%F)" "$LOG_FILE" | grep 'FAILED' | grep -v 'Unreachable' | awk '{print $3}' | sort -u
echo "- Slow Sites"
grep "$(date +%F)" "$LOG_FILE" | grep 'SLOW' | awk '{print $3}' | sort -u
echo "Slowest sites:"
grep "$(date +%F)" "$LOG_FILE" | grep -v 'Unreachable' | awk '{
    for(i=1; i<=NF; i++) {
        if($i ~ /[0-9]+ms/) {
            time = $i
            gsub(/ms.*/, "", time)
            print time, $3

        }
    }
}' | sort -k1 -rn | head -3 | awk '{print $2 " - " $1 "ms"}'
} > /home/abou/cloud-learning-project/logs/daily_reports/report_$(date +%F).txt

REPORT_FILE="home/abou/cloud-learning-project/logs/daily_reports/report_$(date +%F).txt"
    echo ""
    echo "✓ Daily report generated!"
    echo "Report saved to: $REPORT_FILE"
    echo ""
    echo "To view report: cat $REPORT_FILE"
}

show_status() {

    echo "=== Current Website Status ==="
    echo ""
   
    while IFS=',' read -r url name max_time; do
        grep "$name" "$LOG_FILE" | tail -1
    done < "$CONFIG_FILE"
}

show_help() {
    echo "Usage: $0 {check|report|status|--help}"
    echo ""
    echo "Commands:"
    echo "  check      Run health checks on all configured websites"
    echo "  report     Generate daily summary report"
    echo "  status     Show current status of all websites"
    echo "  --help     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 check"
    echo "  $0 report"
    echo "  $0 status"
}

# ============================================
# MAIN LOGIC
# ============================================

case "$1" in
    check)
        run_health_checks
        ;;
    report)
        generate_report
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Error: Invalid command"
        echo ""
        show_help
        exit 1
        ;;
esac

exit 0
