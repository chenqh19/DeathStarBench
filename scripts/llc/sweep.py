import subprocess

core_llc = [20, 20] # number of cores & LLC ways, respectively
max_part = 16 # max number of LLC partitions
do_part = False # whether to do partition
key_words = ["socialnetwork-user-timeline-service-1", "socialnetwork-post-storage-service-1"]
merged_ = ["socialnetwork-jaeger-agent-1", "socialnetwork-user-timeline-redis-1", 
            "socialnetwork-user-timeline-mongomerged_-1", "socialnetwork-post-storage-memcached-1", 
            "socialnetwork-post-storage-mongomerged_-1"]

def setPart(core_part, llc_part):
    processes = []
    merged_procs = []
    # add nginx processes
    get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} socialnetwork-nginx-thrift-1"
    process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(process.stdout)
    for k in range(len(key_words)):
        get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} socialnetwork-" + str(key_words[k]) + "-service-1"
        process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        processes.append(process.stdout)
    for k in range(len(merged_)):
        get_merged_proc_cmd = "sudo docker inspect -f {{.State.Pid}} " + str(merged_[k])
        merged_proc = subprocess.run(get_merged_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        merged_procs.append(merged_proc.stdout)

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
        print("partition:", final_hex)
        return final_hex

    llc_hex = to_hex(llc_part)

    core_str = "\""
    llc_str = ""
    cdp_str = ""
    set_core_cmds = []

    cnt_core = 0
    for i in range(len(llc_hex)):
        core_str = core_str + "llc:" + str(i) + "=" + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + ";"
        llc_str = llc_str + "\"llc:" + str(i) + "=" + str(llc_hex[i]) + ";\""
        if i < len(processes):
            set_core_cmds.append("sudo taskset -cp " + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + " " + processes[i])
        cnt_core += core_part[i]
    for i in range(len(llc_hex), max_part):
        llc_str = llc_str + "\"llc:" + str(i) + "=" + str(hex(2**core_llc[1]-1)) + ";\""
    core_str = core_str + "\""

    core_cmd = "sudo pqos -a " + core_str
    llc_cmd = "sudo pqos -e " + llc_str

    subprocess.run("sudo pqos -R l3cdp-off", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    partition_cmd = llc_cmd
    if do_part:
        subprocess.run(core_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        subprocess.run(partition_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for cmd in set_core_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for merged_proc in merged_procs:
        merged_cmd = "sudo taskset -cp 0-"+str(core_part[0]-1) + " " + str(merged_proc)
        print(merged_cmd)
        subprocess.run(merged_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# start sweeping
for 