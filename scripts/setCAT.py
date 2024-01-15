import subprocess

cdp = False
only_cdp = False

max_part = 16
core_llc = [20, 20] # number of core & llc ways
core_part = [6, 1, 13] 
llc_part = [5, 1, 14]
if cdp:
    cdp_d_part = [1, 2, 3]
    assert len(cdp_d_part) == len(llc_part)
    cdp_c_part = []
    for i in range(len(llc_part)):
        cpart = llc_part[i] - cdp_d_part[i]
        assert cpart >= 0
        cdp_c_part.append(cpart)

key_words = ["home-timeline", "post-storage"]

processes = []
# add nginx processes
get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} socialnetwork-nginx-thrift-1"
process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
processes.append(process.stdout)
for k in range(len(key_words)):
    get_proc_cmd = "sudo docker inspect -f {{.State.Pid}} socialnetwork-" + str(key_words[k]) + "-service-1"
    process = subprocess.run(get_proc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(process.stdout)

# unset
for process in processes:
    unset_cmd = "sudo taskset -cp 0-19 " + process
    subprocess.run(unset_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

'''
# if we do not use all cores, the rest of the cores should be put into the last partition
core_rest = core_llc[0]
for core in core_part:
    core_rest -= core
core_part.append(core_rest)

# if we do not use all LLC ways, the rest of the ways should be put into the last partition
llc_rest = core_llc[1]
for llc in llc_part:
    llc_rest -= llc
llc_part.append(llc_rest)
if cdp:
    cdp_d_part.append(llc_rest)
    cdp_c_part.append(0)

if only_cdp:
    processes = []
    core_part = [20]
    llc_part = [20]
    cdp_d_part = [12]
    cdp_c_part = [llc_part[0]-cdp_d_part[0]]


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
if cdp:
    mixed_part = []
    for i in range(len(llc_part)):
        mixed_part.append(cdp_d_part[i])
        mixed_part.append(cdp_c_part[i])
    mixed_hex = to_hex(mixed_part)
    # print(len(llc_part), len(mixed_part), len(mixed_hex))
    cdp_c_hex = []
    cdp_d_hex = []
    for i in range(len(llc_part)):
        print(i)
        cdp_d_hex.append(mixed_hex[2*i])
        cdp_c_hex.append(mixed_hex[2*i+1])
core_str = "\""
llc_str = ""
cdp_str = ""
set_core_cmds = []

cnt_core = 0
for i in range(len(llc_hex)):
    core_str = core_str + "llc:" + str(i) + "=" + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + ";"
    llc_str = llc_str + "\"llc:" + str(i) + "=" + str(llc_hex[i]) + ";\""
    if cdp:
        cdp_str = cdp_str + "\"llc:" + str(i) + "d=" + str(cdp_d_hex[i]) + ";"+ "llc:" + str(i) + "c=" + str(cdp_c_hex[i]) + ";\""
    if i < len(processes):
        set_core_cmds.append("sudo taskset -cp " + str(cnt_core) + "-" + str(cnt_core+core_part[i]-1) + " " + processes[i])
    cnt_core += core_part[i]
for i in range(len(llc_hex), max_part):
    llc_str = llc_str + "\"llc:" + str(i) + "=" + str(hex(2**core_llc[1]-1)) + ";\""
    if cdp:
        cdp_str = cdp_str + "\"llc:" + str(i) + "d=" + str(hex(2**core_llc[1]-1)) + ";"+ "llc:" + str(i) + "c=" + str(hex(2**core_llc[1]-1)) + ";\""
core_str = core_str + "\""

print(core_str)
print(llc_str)
core_cmd = "sudo pqos -a " + core_str
llc_cmd = "sudo pqos -e " + llc_str
if cdp:
    cdp_cmd = "sudo pqos -e " + cdp_str
# CDP example: pqos -e "llc:1d=0xfff;llc:1c=0xfff00;" (add d(data) or c(code) after LLC index)
# ref: https://github.com/intel/intel-cmt-cat/wiki/Usage-Examples

if cdp:
    subprocess.run("sudo pqos -R l3cdp-on", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    partition_cmd = cdp_cmd
else:
    subprocess.run("sudo pqos -R l3cdp-off", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    partition_cmd = llc_cmd
subprocess.run(core_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
subprocess.run(partition_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
for cmd in set_core_cmds:
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
subprocess.run("sudo pqos -s", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
'''