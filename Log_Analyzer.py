import os
import re
from datetime import datetime

# Helper function to parse a log line
def parse_log_line(line):
    try:
        # Match the log format using a regular expression
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR|DEBUG) (.+)"
        match = re.match(pattern, line)
        if match:
            timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
            log_level = match.group(2)
            message = match.group(3)
            return timestamp, log_level, message
        else:
            raise ValueError("Invalid log format")
    except Exception as e:
        return None  # Skip invalid or malformed entries


# Function to read and parse the log file
def read_logs(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file '{file_path}' not found.")
    
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            parsed = parse_log_line(line.strip())
            if parsed:
                logs.append(parsed)
            else:
                print(f"Warning: Skipping invalid log entry: {line.strip()}")
    return logs


# Function to count log levels
def count_log_levels(logs):
    log_level_counts = {}
    for _, log_level, _ in logs:
        log_level_counts[log_level] = log_level_counts.get(log_level, 0) + 1
    return log_level_counts


# Function to find the most recent entry for a specific log level
def find_most_recent_entry(logs, level):
    filtered_logs = [log for log in logs if log[1] == level]
    if not filtered_logs:
        return None
    return max(filtered_logs, key=lambda x: x[0])


# Function to filter logs by date range
def filter_logs_by_date(logs, start_date, end_date):
    filtered = [
        log for log in logs
        if start_date <= log[0].date() <= end_date
    ]
    return filtered


# Main program
def main():
    log_file = "logs.txt"
    
    try:
        # Read logs
        logs = read_logs(log_file)
        if not logs:
            print("No valid logs found.")
            return
        
        # 1. Count log levels
        log_level_counts = count_log_levels(logs)
        print("\nLog Level Counts:")
        for level, count in log_level_counts.items():
            print(f"{level}: {count}")
        
        # 2. Most recent entry for a specific log level
        level = input("\nEnter a log level to find the most recent entry (INFO/WARNING/ERROR/DEBUG): ").strip()
        most_recent = find_most_recent_entry(logs, level)
        if most_recent:
            print(f"\nMost Recent {level} Entry:\n{most_recent[0]} {most_recent[1]} {most_recent[2]}")
        else:
            print(f"No entries found for log level: {level}")
        
        # 3. Filter logs by date range
        start_date = input("\nEnter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            filtered_logs = filter_logs_by_date(logs, start_date, end_date)
            if filtered_logs:
                with open("filtered_logs.txt", "w") as f:
                    for log in filtered_logs:
                        f.write(f"{log[0]} {log[1]} {log[2]}\n")
                print("\nFiltered logs saved to 'filtered_logs.txt'.")
            else:
                print("No logs found in the given date range.")
        except ValueError as e:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
