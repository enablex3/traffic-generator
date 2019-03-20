from paramiko import SSHClient
from scp import SCPClient
import paramiko

def transfer_script(host, username, password, script):
	ssh = SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,username=username,password=password)

    loc = "/home/{}".format(username)

    with SCPClient(ssh.get_trasport()) as scp:
    	scp.put(script, loc)

host = "192.168.126.129"
username = "root"
password = "root"
script = "bot_dos.py"
