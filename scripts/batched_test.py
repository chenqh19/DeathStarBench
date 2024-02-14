import subprocess

def set_range(low, high, interval):
    rpss = []
    rps = low
    while rps < high:
        rpss.append(rps)
        rps += interval
    rpss.append(high)
    return rpss


output_file = "../kuber-deploy/test_rps.txt"
rpss = set_range(1900, 2200, 100)
for rps in rpss:
    cmd = "../../wrk2/wrk -D exp -t 100 -c 100 -d 20 -L -s ../../hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://192.168.0.194:5000 -R " + str(rps)
    call_py_cmd = "cd llc ; python gen_work.py \"" + cmd + "\" " + output_file + " 0"
    print(call_py_cmd)
    subprocess.run(call_py_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)