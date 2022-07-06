#!/usr/bin/env python3
import paramiko
import argparse

def get_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-ipa', '--ip_address', required=True)
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-p', '--password', required=True, help="if password contains '$', ensure to wrap password in single quotes")
    parser.add_argument('-c', '--command', required=True)
    args = parser.parse_args() 

    return args
    
def execute_command(ip_addr, username, password, command):
    ssh = paramiko.SSHClient()
    # Load SSH host keys.
    ssh.load_system_host_keys()
    # Add SSH host key when missing.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    attempts = 3
    for attempt in range(attempts):
        try:
            #print("Attempt to connect: {}".format(attempt))
            # Connect to router using username/password authentication.
            ssh.connect(ip_addr, 
                        username=username, 
                        password=password,
                        look_for_keys=False )
            # Run command.
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            # Read output from command.
            output = ssh_stdout.readlines()
            # Close connection.
            ssh.close()
            return output

        except Exception as error_message:
            print("Unable to connect")
            print(error_message)

def main():
    args = get_args()
    command_output = execute_command(ip_addr=args.ip_address, username=args.username, password=args.password, command=args.command)
    print(command_output)

if __name__ == "__main__":
    main()
