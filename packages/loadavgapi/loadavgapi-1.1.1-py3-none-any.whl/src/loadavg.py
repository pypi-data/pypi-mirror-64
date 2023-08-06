from flask import Flask, jsonify
import psutil
from sys import argv, exit
import os
from shutil import disk_usage

app = Flask(__name__)

@app.route('/')
def my_app():
    disk = disk_usage("/")
    _res = {}
    _res['cpu_percent'] = psutil.cpu_percent()
    _res['memory_percent'] = psutil.virtual_memory()[2]
    _res['disk_percent'] = int(int(disk[1] // (2**30)) / int(disk[0] // (2**30)) * 100)
    _res['disk_usage'] = f"{disk[1] // (2**30)}GB/{disk[0] // (2**30)}GB"
    return jsonify(_res)


if os.name != 'posix':
    if os.name == 'nt':
        os.system('cls')
    print('work on linux only')
    exit(True)


if os.getuid() != 0:
    os.system('clear')
    print("Run in root user")
    exit(True)

try:
    get_command = argv[1]
except IndexError:
    os.system('clear')
    print('''
-----------------------------------------------
- Usage: loadavg [option]                     -
-                                             -
- for install: loadavg install                -
- for start: loadavg start                    -  
- for stop: loadavg stop                      -
- for restart: loadavg restart                -
-----------------------------------------------
    ''')
    exit(True)


def installer():
    current_directory = os.getcwd()
    try:
        os.mkdir('.loadavg_runer')
    except FileExistsError:
        pass
    os.chdir('.loadavg_runer')
    with open("run.sh", mode="w") as bash_file:
        bash_file.write("loadavg start_service")
        bash_file.close()
    
    with open("/etc/systemd/system/loadavg.service", mode="w") as service:
        service.write(f"""
[Unit]
Description=loadavg daemon

[Service]
ExecStart=/bin/bash {current_directory}/.loadavg_runer/run.sh
StandardOutput=syslog
StandardError=syslog
syslogIdentifier=loadavg

[Install]
WantedBy=multi-user.target
        """)
    
    os.system('systemctl enable loadavg')
    
    os.system('clear')
    print("[+]Loadavg api installed\n[!]For start service use this command ->\nloadavg start")


def main():
    if get_command == "install":
        installer()

    elif get_command == "start":
        os.system('systemctl start loadavg')
    
    elif get_command == "stop":
        os.system("systemctl stop loadavg")
    
    elif get_command == "restart":
        os.system("systemctl restart loadavg")

    elif get_command == "start_service":
        app.run(host='0.0.0.0', port='30789')
        


if __name__ == "__main__":
    main()
