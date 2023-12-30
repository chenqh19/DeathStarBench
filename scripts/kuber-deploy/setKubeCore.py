import subprocess

key_words = ["search"]
core_part = [4, ]

processes = []
for k in range(len(key_words)):
    get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} socialnetwork-" + str(key_words[k]) + "-service-1"
    process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(process.stdout)

set_core_cmds = []

cnt_core = 0
for i in range(len(processes)):
    set_core_cmds.append("sudo taskset -cp " + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + " " + processes[i])

for cmd in set_core_cmds:
    print(cmd)
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


