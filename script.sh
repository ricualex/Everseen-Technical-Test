#!/bin/bash

LOG_FILE="/home/ricu/Desktop/everseen/ereceiver-service.log"
TMP_FILE="/home/ricu/Desktop/everseen/ereceiver_log_monitor.tmp"
validate_log_entry() {
    local log_entry="$1"
    if [[ "$log_entry" == *"ERROR"* ]]; then
        echo "Error detected: $log_entry"
    fi
}
if [[ ! -f "$TMP_FILE" ]]; then
    echo "0" > "$TMP_FILE"
fi
while true; do
    last_pos=$(cat "$TMP_FILE")
    new_entries=$(tail -c +$((last_pos + 1)) "$LOG_FILE")
    current_pos=$(wc -c < "$LOG_FILE")
    echo "$current_pos" > "$TMP_FILE"
    while IFS= read -r line; do
        validate_log_entry "$line"
    done <<< "$new_entries"
    sleep 30
done

