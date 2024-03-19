import argparse
# import paramiko
import subprocess
import multiprocessing

def run_command(command, output_file):
    with open(output_file, "a") as f:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            decoded_line = line.decode().strip()
            if "0.990625" in decoded_line:
                f.write(decoded_line + "\n")
        process.stdout.close()
        process.stderr.close()

def run_cmd(gen_work_cmd, output_file):
    process1 = multiprocessing.Process(target=run_command, args=(gen_work_cmd,output_file))
    # process2 = multiprocessing.Process(target=run_command, args=(command2,))

    process1.start()
    # process2.start()

    process1.join()
    # process2.join()

def refresh():
    refresh_cmd = "sudo docker service update --force test_jaeger-collector"
    subprocess.run(refresh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a command on a remote server via SSH")
    parser.add_argument("gen_work_cmd", help="Remote server hostname")
    parser.add_argument("output_file", help="Remote server username")
    parser.add_argument("for_sn", help="Remote server hostname")
    args = parser.parse_args()
    with open(args.output_file, "a") as f:
        f.write("------new_config------\n")
    print(args.gen_work_cmd)
    for i in range(5):
        run_cmd(args.gen_work_cmd, args.output_file)
    if args.for_sn:
        refresh()