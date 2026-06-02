import time

# SQL detection
sql_patterns = ["OR 1=1",
                "UNION SELECT",
                "'--",
                "DROP TABLE"]

# XSS detection
xss_patterns = ["<script>",
                "alert(",
                "onerror="]

# Path Traversal attack
traversal_patterns =[
    "../",
    "..\\",
    "/etc/passwd",
    "windows/system32"
    
]

print("Monitoring logs in real time...")

# Store previous line count
old_lines = 0

while True:

    with open("logs/access.log", "r") as file:

        logs = file.readlines()

        # Count current lines
        new_lines = len(logs)

        # If new log added
        if new_lines > old_lines:
            #SQL Injection Detection
            for pattern in sql_patterns:

                # Get newest line
                last_line = logs[-1]

                ip = last_line.split(" ")[0]
                timestamp = last_line.split("[")[1].split("]")[0]

                if pattern.lower() in last_line.lower():

                    print("\n========== REALTIME ALERT ==========")
                    print("Attack Type : SQL Injection")
                    print("Attacker IP :", ip)
                    print("Time        :", timestamp)
                    print("Payload     :", pattern)
                    print("====================================")

                    with open("alerts.log", "a") as alert_file:
                        alert_file.write(f"[SQL Injection] IP: {ip} | Time: {timestamp} | Payload: {pattern}\n")
    

            #XSS Detection
            for pattern in xss_patterns:

                if pattern.lower() in last_line.lower():

                    print("\n========== REALTIME ALERT ==========")
                    print("Attack Type : XSS Attack")
                    print("Attacker IP :", ip)
                    print("Time        :", timestamp)
                    print("Payload     :", pattern)
                    print("====================================")

                    with open("alerts.log", "a") as alert_file:
                        alert_file.write(f"[XSS Attack] IP: {ip} | Time: {timestamp} | Payload: {pattern}\n")

            #Path Traversal Detection
            for pattern in traversal_patterns:

                if pattern.lower() in last_line.lower():

                    print("\n========== REALTIME ALERT ==========")
                    print("Attack Type : Path Traversal")
                    print("Attacker IP :", ip)
                    print("Time        :", timestamp)
                    print("Payload     :", pattern)
                    print("====================================")

                    with open("alerts.log", "a") as alert_file:
                        alert_file.write(f"[Path Traversal] IP: {ip} | Time: {timestamp} | Payload: {pattern}\n")

            print("\n[+] New Log Detected!")
            print(last_line)

            # Update line count
            old_lines = new_lines

    time.sleep(1)

