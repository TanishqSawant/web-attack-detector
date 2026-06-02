# read log files
with open("logs/access.log", "r") as file:
    logs = file.readlines()

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

# Attack counters
sql_count = 0
xss_count = 0
traversal_count = 0

#Attacker IPs
attacker_ips = {}

#check log file
for line in logs:

    # Skip empty lines
    if line.strip() == "":
        continue

    # Skip malformed logs
    if "[" not in line or "]" not in line:
        continue

    # Extract IP
    ip = line.split(" ")[0]

    # Extract timestamp
    timestamp = line.split("[")[1].split("]")[0]
    # SQL Injection Detection
    for pattern in sql_patterns:
        if pattern.lower() in line.lower():

            print("\n========== ALERT ==========")
            print("Attack Type : SQL Injection")
            print("Attacker IP :", ip)
            print("Time        :", timestamp)
            print("Payload     :", pattern)
            print("===========================\n")
            sql_count += 1

            if ip in attacker_ips:
                attacker_ips[ip] += 1
            else:
                attacker_ips[ip] = 1

            with open("alerts.log", "a") as alert_file:
                alert_file.write(f"[SQL Injection] IP: {ip} | Time: {timestamp} | Payload: {pattern}\n")


    # XSS Detection
    for pattern in xss_patterns:
        if pattern.lower() in line.lower():

            print("\n========== ALERT ==========")
            print("Attack Type : XSS Attack")
            print("Attacker IP :", ip)
            print("Time        :", timestamp)
            print("Payload     :", pattern)
            print("===========================\n")
            xss_count += 1

            if ip in attacker_ips:
                attacker_ips[ip] += 1
            else:
                attacker_ips[ip] = 1

            with open("alerts.log", "a") as alert_file:
                alert_file.write(f"[XSS Attack] IP: {ip} | Time: {timestamp} | Payload: {pattern}\n")

    # Directory Traversal Detection
    for pattern in traversal_patterns:
        if pattern.lower() in line.lower():

            print("\n========== ALERT ==========")
            print("Attack Type : Directory Traversal")
            print("Attacker IP :", ip)
            print("Time        :", timestamp)
            print("Payload     :", pattern)
            print("===========================\n")
            traversal_count += 1

            if ip in attacker_ips:
                attacker_ips[ip] += 1
            else:
                attacker_ips[ip] = 1

            with open("alerts.log", "a") as alert_file:
                alert_file.write(f"[Directory Traversal] IP: {ip} | Time: {timestamp} | Payload: {pattern}\n")

#Attack Summary
print("\n===== ATTACK SUMMARY =====")

print("SQL Injection Attacks :", sql_count)
print("XSS Attacks           :", xss_count)
print("Traversal Attacks     :", traversal_count)

#Top Attackers
print("\n===== TOP ATTACKERS =====")

for ip, count in attacker_ips.items():
    print(ip, "→", count, "attacks")

most_dangerous_ip = ""
max_attacks = 0

for ip,count in attacker_ips.items():
    if count > max_attacks:
        max_attacks = count
        most_dangerous_ip = ip

print("\n===== MOST DANGEROUS ATTACKER =====")

print("IP Address   :", most_dangerous_ip)
print("Total Attacks:", max_attacks)