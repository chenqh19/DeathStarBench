import os
import argparse
import shutil
import stat

# should use Social Network, since Hotel Reservation has ~1% LLC miss rate
# directory_b_list = ["frontend", "search"]
directory_b_list = ["text", "userTL"]

cpu_partitions = {}
llc_partitions = {}

cpu_partitions[directory_b_list[0]] = "00000\n"
llc_partitions[directory_b_list[0]] = "0007f\n"

cpu_partitions[directory_b_list[1]] = "00000\n"
llc_partitions[directory_b_list[1]] = "00080\n"

def create_directory_and_files(directory_a, directory_b_list):
    for directory_b in directory_b_list:
        # Create directory b
        directory_b_path = os.path.join(directory_a, directory_b)
        os.makedirs(directory_b_path, exist_ok=True)

        # Create files c and d in directory b (you can write content as needed)
        file_c = os.path.join(directory_b_path, "cpus")
        file_d = os.path.join(directory_b_path, "schemata")

        # Create files c and d (you can write content as needed)
        with open(file_c, "w") as f_c:
            f_c.write(cpu_partitions[directory_b])

        with open(file_d, "w") as f_d:
            f_d.write("L3:0="+llc_partitions[directory_b])

def clean_directory_and_files(directory_a):
    def del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        shutil.rmtree(name)
    if os.path.exists(directory_a):
        shutil.rmtree(directory_a, onerror=del_rw)

if __name__ == "__main__":
    # Create a command line argument parser
    parser = argparse.ArgumentParser(description="Create directories b and files c and d in directory a.")
    parser.add_argument("directory_a", help="Path to directory a")
    parser.add_argument("create_or_clean", help="whether to create or clean the folder")

    # Parse command line arguments
    args = parser.parse_args()
    if args.create_or_clean == "create":
        create_directory_and_files(args.directory_a, directory_b_list)
    elif args.create_or_clean == "clean":
        clean_directory_and_files(args.directory_a)

    
