import subprocess
import multiprocessing

core_llc = [20, 20] # number of cores & LLC ways, respectively
max_part = 16 # max number of LLC partitions
workload = "htl"
output_file = "llc_sweep-"+workload+".txt"

if workload == "utl":
    core_part = [5, 10, 5]
    gen_work_cmd = "../../wrk2/wrk -D exp -t 100 -c 100 -d 10 -L -s ../../socialNetwork/wrk2/scripts/social-network/read-user-timeline.lua http://localhost:8080/wrk2-api/user-timeline/read -R 2000"
    key_words = ["user-timeline-service", "spost-storage-service"]
    merged_ = ["user-timeline-redis", "user-timeline-mongodb", 
                "post-storage-memcached", "post-storage-mongodb"]
elif workload == "htl":
    core_part = [14, 1, 5]
    gen_work_cmd = "../../wrk2/wrk -D exp -t 100 -c 100 -d 10 -L -s ../../socialNetwork/wrk2/scripts/social-network/read-home-timeline.lua http://localhost:8080/wrk2-api/home-timeline/read -R 2000"
    key_words = ["home-timeline-service", "post-storage-service"]
    merged_ = ["home-timeline-redis", "post-storage-memcached", 
                "post-storage-mongodb"]

import paramiko

def execute_remote_command(hostname, username, private_key_path, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh_client.connect(hostname=hostname, username=username, pkey=private_key)

        # execution
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # # print output
        # print("Command output:")
        # for line in stdout:
        #     print(line.strip())
        
        if stderr.channel.recv_exit_status() != 0:
            print("Error:", stderr.read().decode())
    except Exception as e:
        print("An error occurred:", e)
    finally:
        ssh_client.close()

remote_hostname = "hp197.utah.cloudlab.us"
remote_username = "chenqh23"
private_key_path = "/users/chenqh23/.ssh/id_rsa"

command_to_execute = "echo \"hello\""


def setPart(core_part, llc_part, do_part):
    processes = []
    merged_procs = []
    # add nginx processes
    get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} $(sudo docker ps --format \"{{.Names}}\" | grep nginx)"
    process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(process.stdout)
    # processes.append(0)
    for k in range(len(key_words)):
        get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} $(sudo docker ps --format \"{{.Names}}\" | grep " + str(key_words[k]) + ")"
        process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        processes.append(process.stdout)
    for k in range(len(merged_)):
        get_merged_proc_cmd = "sudo docker inspect -f {{.State.Pid}} $(sudo docker ps --format \"{{.Names}}\" | grep " + str(merged_[k]) + ")"
        merged_proc = subprocess.run(get_merged_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        merged_procs.append(merged_proc.stdout)
    sub_nginx_cmd = "sudo docker top $(sudo docker ps --format \"{{.Names}}\" | grep nginx)  | awk \'NR>1 {print $2}\'"
    # nginx subprocesses
    process = subprocess.run(sub_nginx_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pids = process.stdout
    pid_lines = pids.strip().split("\n")
    for pid in pid_lines:
        merged_procs.append(pid+'\n')

    # unset
    for process in processes+merged_procs:
        unset_cmd = "sudo taskset -cp 0-19 " + process
        subprocess.run(unset_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # if we do not use all cores, the rest of the cores should be put into the last partition
    core_rest = core_llc[0]
    for core in core_part:
        core_rest -= core
    if core_rest != 0:
        core_part.append(core_rest)

    # if we do not use all LLC ways, the rest of the ways should be put into the last partition
    llc_rest = core_llc[1]
    for llc in llc_part:
        llc_rest -= llc
    if llc_rest != 0:
        llc_part.append(llc_rest)

    def to_hex(part_array):
        final_hex = []
        cnt_llc = 0
        for part in part_array:
            bool_array = []
            for i in range(core_llc[0]):
                bool_array.insert(0, cnt_llc <= i < (cnt_llc + part))
            cnt_llc += part
            binary_str = "".join("1" if x else "0" for x in bool_array)
            binary_int = int(binary_str, 2)
            hex_str = hex(binary_int)
            final_hex.append(hex_str)
        return final_hex

    llc_hex = to_hex(llc_part)

    core_str = "\""
    llc_str = "\""
    cdp_str = ""
    set_core_cmds = []

    cnt_core = 0
    for i in range(len(llc_hex)):
        core_str = core_str + "llc:" + str(i) + "=" + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + ";"
        llc_str = llc_str + "llc:" + str(i) + "=" + str(llc_hex[i]) + ";"
        if i < len(processes):
            set_core_cmds.append("sudo taskset -cp " + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + " " + processes[i])
        cnt_core += core_part[i]
    for i in range(len(llc_hex), max_part):
        llc_str = llc_str + "llc:" + str(i) + "=" + str(hex(2**core_llc[1]-1)) + ";"
    core_str = core_str + "\""
    llc_str = llc_str + "\""

    core_cmd = "sudo pqos -a " + core_str
    llc_cmd = "sudo pqos -e " + llc_str

    subprocess.run("sudo pqos -R l3cdp-off", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    partition_cmd = llc_cmd
    if do_part:
        subprocess.run(core_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        subprocess.run(partition_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for cmd in set_core_cmds:
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for merged_proc in merged_procs:
        merged_cmd = "sudo taskset -cp 0-"+str(core_part[0]-1) + " " + str(merged_proc)
        subprocess.run(merged_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# start sweeping
setPart(core_part, [7, 7, 6], False)
remote_gen_work_cmd = "cd DeathStarBench/scripts/llc ; python gen_work.py \"" + gen_work_cmd + "\" " + output_file
print(remote_gen_work_cmd)
execute_remote_command(remote_hostname, remote_username, private_key_path, remote_gen_work_cmd)
for part1 in range(1, core_llc[1]):
    for part2 in range(1, core_llc[1]-part1-1):
        print(part1, part2)
        llc_part = [part1, part2, core_llc[1]-part1-part2]
        setPart(core_part, llc_part, True)
        remote_gen_work_cmd = "cd DeathStarBench/scripts/llc ; python gen_work.py \"" + gen_work_cmd + "\" " + output_file
        print(remote_gen_work_cmd)
        execute_remote_command(remote_hostname, remote_username, private_key_path, remote_gen_work_cmd)