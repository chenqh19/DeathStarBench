import subprocess
import multiprocessing

keywords=["frontend", "geo", "profile", "rate", "recommendation", "reservation", "search", "user"]
all_pids = []
for keyword in keywords:
    cmd = "crictl inspect --output go-template --template \'{{.info.pid}}\' $(crictl ps --name \"" + keyword + "*\" -q)"
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pid = output.stdout.strip().split("\n")
    if pid[0] != '':
        all_pids += pid
pid_str = ""
for pid in all_pids:
    pid_str += "\""
    pid_str += pid
    pid_str += "\" "
print(pid_str)
# for pid in all_pids:
#     profile_cmd = "../profile.sh \"searchaway-" + str(pid) + "-\" \"sudo perf record -e cycles -F 999 -p\" \"-- sleep 2\" " + str(pid)
#     print(profile_cmd)
#     subprocess.run(profile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='ignore')