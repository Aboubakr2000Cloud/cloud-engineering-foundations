#!/bin/bash
LOG_FILE=$1
REPORT="report.txt"
{
echo "LOG ANALYSIS REPORT"
echo "Date: $(date)"
echo "=== SUMMARY: ==="
echo "- Total lines: $(wc -l < "$LOG_FILE")"
echo "- ERROR count: $(grep "ERROR" $LOG_FILE | wc -l)"
echo "- WARNING count: $(grep "WARNING" $LOG_FILE | wc -l)"
echo "- INFO count: $(grep "INFO" $LOG_FILE | wc -l)"
echo "=== TOP ERRORS: ==="
grep "ERROR" $LOG_FILE | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn | head -5
echo "=== SECURITY ALERTS: ==="
grep "Failed login attempt" $LOG_FILE | awk '{print $5, $6, $7, $8}' | sort | uniq -c 
echo "=== DATABASE ISSUES: ==="
grep "Database connection failed" $LOG_FILE | awk '{print $5, $6, $7}' | sort | uniq -c 
echo "=== SYSTEM WARNINGS: ==="
grep "WARNING" $LOG_FILE | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn
echo "=== END OF THE REPPORT ==="
} > "$REPORT"
echo "report saved to $REPORT"
