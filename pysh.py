import paramiko
import getpass

def execute_remote_command(host, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)
    
    transport = client.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    
    command_with_x11 = f"DISPLAY=:0 {command}"
    session.exec_command(command_with_x11)
    
    stdout = session.makefile('r', -1)
    output = stdout.read().decode()
    session.close()
    client.close()
    
    return output

def user_selection():
    host = input("Enter the remote host IP: ")
    port = int(input("Enter the port (default 22): ") or 22)
    username = input("Enter the username: ")
    password = getpass.getpass("Enter the password: ")

    while True:
        command = input("Enter the command to execute or 'exit' to quit: ")
        if command.lower() == 'exit':
            break
        output = execute_remote_command(host, port, username, password, command)
        print("Output:\n", output)

user_selection()
