# Week 2 Log Analysis - Command Reference

## Task 1: Basic Error Analysis
# Count total errors
grep "ERROR" server.log | wc -l

# Count warnings
grep "WARNING" server.log | wc -l

# Most common error types
grep "ERROR" server.log | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn

## Task 2: Security Analysis
# Failed login attempts
grep "Failed login attempt" server.log | wc -l

# Targeted usernames
grep "Failed login attempt" server.log | awk '{print $8}' | sort | uniq -c | sort -rn

# Attack source IPs
grep "Failed login attempt" server.log | awk '{print $4}' | sort | uniq -c | sort -rn

## Task 3: Database Issues
# Database failures count
grep "Database connection failed" server.log | wc -l

# IP with most problems
grep "Database connection failed" server.log | awk '{print $4}' | sort | uniq -c | sort -rn

# Error timestamps
grep "Database connection failed" server.log | awk '{print $1, $2}' | sort

## Task 4: System Health
# Warning types
grep "WARNING" server.log | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn

# Memory trend detection
grep "High memory usage" server.log | awk '{print substr($8,1,2)}' | awk '
NR>1 && $1<prev {down++}
NR>1 && $1>prev {up++}
{prev=$1}
END {
  if (up && !down) print "Increasing";
  else if (down && !up) print "Decreasing";
  else print "Mixed or stable";
}'

# Pattern correlation (memory warnings by IP)
grep "High memory usage" server.log | awk '{print $4}' | sort | uniq -c | sort -rn
