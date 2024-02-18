import subprocess

def set_range(low, high, interval):
    rpss = []
    rps = low
    while rps < high:
        rpss.append(rps)
        rps += interval
    rpss.append(high)
    return rpss

test_type = "ps" 
output_file = "../lat_files/"+test_type+"_rps.txt"
rpss = set_range(1000, 2200, 100)
for rps in rpss:
    if test_type == "hr":
        cmd = "../../wrk2/wrk -D exp -t 100 -c 100 -d 20 -L -s ../../hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://192.168.0.194:5000 -R " + str(rps)
    elif test_type == "htl" or test_type == "ps":
        cmd = "../../wrk2/wrk -D exp -t 100 -c 100 -d 20 -L -s ../../socialNetwork/wrk2/scripts/social-network/read-home-timeline.lua http://localhost:8080/wrk2-api/home-timeline/read -R " + str(rps)
    elif test_type == "utl":
        cmd = "../../wrk2/wrk -D exp -t 100 -c 100 -d 20 -L -s ../../socialNetwork/wrk2/scripts/social-network/read-user-timeline.lua http://localhost:8080/wrk2-api/user-timeline/read -R " + str(rps)
    call_py_cmd = "cd llc ; python gen_work.py \"" + cmd + "\" " + output_file 
    if test_type == "hr":
        call_py_cmd = call_py_cmd + " 0"
    else:
        call_py_cmd = call_py_cmd + " 1"
    print(call_py_cmd)
    subprocess.run(call_py_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)