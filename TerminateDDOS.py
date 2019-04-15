# user will need to be sure python is installed on each bot
# BE SURE TO INCLUDE WORKAROUND IN README IF THIS FAILS !!!
from paramiko import SSHClient
from Inputs import get_bot_info
import paramiko, sys, getpass

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
        verification = str(error) + "\n"
        sys.stderr.write(verification)
        sys.stderr.flush()

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
        verification = "Process terminated on bot: {}.\n".format(bot)
        sys.stdout.write(verification)
        sys.stdout.flush()
    else:
        verification = "Process has not been terminated on bot: {}.\n".format(bot)
        sys.stderr.write(verification)
        sys.stderr.flush()

    return("break")

username = getpass.getuser()

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

for bot, bot_credentials in botnet.items():
    username = bot_credentials[0]
    password = bot_credentials[1]

    try:
        terminate_bot_dos(bot, username, password)
    except Exception as error:
        verification = "Nothing to do on: {}\n".format(bot)
        sys.stderr.write(verification)
        sys.stderr.flush()

sys.exit(0)