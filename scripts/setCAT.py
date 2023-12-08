import subprocess

max_part = 16
core_llc = [20, 20] # number of core & llc ways
core_part = [] 
llc_part = [] 
key_words = []

processes = []
for k in range(len(key_words)):
    get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} socialnetwork-" + str(key_words[k]) + "-service-1"
    process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(process.stdout)

core_rest = core_llc[0]
for core in core_part:
    core_rest -= core
core_part.append(core_rest)

llc_rest = core_llc[1]
for llc in llc_part:
    llc_rest -= llc
llc_part.append(llc_rest)


llc_hex = []

cnt_llc = 0
for part in llc_part:
    bool_array = []
    for i in range(core_llc[0]):
        bool_array.insert(0, cnt_llc <= i < (cnt_llc + part))
    cnt_llc += part
    binary_str = "".join("1" if x else "0" for x in bool_array)
    binary_int = int(binary_str, 2)
    hex_str = hex(binary_int)
    llc_hex.append(hex_str)
print("llc_partition:", llc_hex)

core_str = ""
llc_str = ""
set_core_cmds = []

cnt_core = 0
for i in range(len(llc_hex)):
    core_str = core_str + "\"llc:" + str(i) + "=" + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + ";\""
    llc_str = llc_str + "\"llc:" + str(i) + "=" + str(llc_hex[i]) + ";\""
    if i < len(processes):
        set_core_cmds.append("sudo taskset -cp " + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + " " + processes[i])
    cnt_core += core_part[i]
for i in range(len(llc_hex), max_part):
    llc_str = llc_str + "\"llc:" + str(i) + "=" + str(hex(2**core_llc[1]-1)) + ";\""
print(core_str, llc_str)

core_cmd = "sudo pqos -a " + core_str
llc_cmd = "sudo pqos -e " + llc_str
# CDP example: pqos -e "llc:1d=0xfff;llc:1c=0xfff00;" (add d(data) or c(code) after LLC index)
# ref: https://github.com/intel/intel-cmt-cat/wiki/Usage-Examples

core = subprocess.run(core_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(core.stderr)
subprocess.run(llc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
for cmd in set_core_cmds:
    print(cmd)
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


