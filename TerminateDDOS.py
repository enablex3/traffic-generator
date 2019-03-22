# will need to pull bot info from Inputs
# BE SURE TO INCLUDE WORKAROUND IN README IF THIS FAILS !!!
from paramiko import SSHClient
import paramiko, sys

def terminate_bot_dos(bot, username, password):
        # obtain the process ID of the bot_dos.py execution first
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_system_host_keys()
        
        command = "ps -ef | grep bot_dos.py"
        ssh.connect(hostname=bot, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        
        output = stdout.read()
        output = output.decode()
        error = stderr.read()
        error = error.decode()

        output = output.split('\n')
        try:
            dos_process = [process for process in output if "python bot_dos.py" in process]
            dos_process = dos_process[0]
            dos_process = dos_process.split(" ")
        except Exception as error:
            verification = str(error)
            print(verification)
            sys.exit(1)

        evaluate = []

        for element in dos_process:
            try:
                element = int(element)
                evaluate.append(element)
            except Exception as error:
                pass

        dos_pid = max(evaluate)

        # kill the process via its PID
        command = "kill -9 {}".format(str(dos_pid))
        stdin, stdout, stderr = ssh.exec_command(command)

        # verify the command executed successfully
        command = "ps -ef | grep bot_dos.py"
        ssh.connect(hostname=bot, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read()
        output = output.decode()

        if not "python bot_dos.py" in output:
            verification = "Process terminated on bot: {}.".format(bot)
        else:
            verification = "Process has not been terminated on bot: {}.".format(bot)

        return(verification)

bot1 = "192.168.3.131"
bot2 = "192.168.3.130"

username = "root"
password = "root"

botnet = { bot1: [username, password], bot2: [username, password] }

for bot, bot_credentials in botnet.items():
    username = bot_credentials[0]
    password = bot_credentials[1]
    
    verification = terminate_bot_dos(bot, username, password)

    print(verification)