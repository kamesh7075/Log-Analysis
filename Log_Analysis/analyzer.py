import re
import time
from collections import Counter

def analyze_logs(log_file):
    with open(log_file, 'r') as file:
        logs = file.readlines()

    successful_logins = 0
    failed_logins = 0
    failed_users = []

    for line in logs:
        line = line.strip()

        # Track login attempt
        if "Login attempt: Username:" in line:
            match = re.search(r'Username:\s*(\w+)', line)
            if match:
                current_username = match.group(1)

        # Failed login
        if "Failed login attempt:" in line:
            match = re.search(r'Username:\s*(\w+)', line)
            if match:
                failed_logins += 1
                failed_users.append(match.group(1))

        # Successful login based on HTTP 200
        if '"POST /login HTTP/1.1" 200 -' in line:
            successful_logins += 1

    # Prepare the report lines
    output = []
    output.append("===== Login Analysis Report =====\n")
    output.append(f"Total Successful Logins: {successful_logins}")
    output.append(f"Total Failed Logins:     {failed_logins}\n")

    if failed_users:
        output.append("Suspicious Activity Detected:\n")
        output.append(f"{'Username':<20}{'Failed Attempts':<20}")
        output.append(f"{'-'*40}")
        user_counts = Counter(failed_users)
        for user, count in user_counts.items():
            if count > 1:
                output.append(f"{user:<20}{count:<20}")
    else:
        output.append("No suspicious activity detected.")

    # Print to terminal
    for line in output:
        print(line)

    # Ask user if they want to save the results
    choice = input("\nDo you want to save the results? (y/n): ").strip().lower()
    if choice == 'y':
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"log_analysis_{timestamp}.txt"
        with open(filename, 'w') as f:
            for line in output:
                f.write(line + '\n')
        print(f"\nResults saved to: {filename}")
    else:
        print("\nResults were not saved.")

if __name__ == "__main__":
    analyze_logs('app.log')
