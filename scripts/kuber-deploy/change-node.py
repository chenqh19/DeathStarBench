import os

def replace_line(file_path, search_content, new_line):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if search_content in line:
                    file.write(new_line + '\n')
                else:
                    file.write(line)
        print(f"Replacement successful: {file_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")

deploy = {
    "frontend" : [["frontend"], [0]],
    "reccomend" : [["recommendation", "mongodb-recommendation"], [1, 0]],
    "reserve" : [["reservation", "mongodb-reservation", "memcached-reservation"], [1, 0, 0]],
    "user" : [["user", "mongodb-user"], [1, 0]],
    "search" : [["search"], [1]],
    "geo" : [["geo", "mongodb-geo"], [0, 1]],
    "profile" : [["profile", "mongodb-profile", "memcached-profile"], [0, 1, 1]],
    "rate" : [["rate", "mongodb-rate", "memcached-rate"], [0, 1, 1]]
}


for name in deploy.keys():
    folder_path = "/users/chenqh23/DeathStarBench/hotelReservation/kubernetes/" + name + "/"
    search_content = ".qihang-winter0.ragger-pg0.utah.cloudlab.us"
    
    for i in range(len(deploy[name][0])):
        nickname = deploy[name][0][i]
        new_line = "      nodeName: node-" + str(deploy[name][1][i]) + ".qihang-winter0.ragger-pg0.utah.cloudlab.us"
        file_name = nickname + "-deployment.yaml"
        file_path = os.path.join(folder_path, file_name)
        replace_line(file_path, search_content, new_line)



# if __name__ == "__main__":
#     folder_path = "/users/chenqh23/DeathStarBench/hotelReservation/kubernetes/" + name  # Replace with your folder path
#     file_name = name + "-deployment.yaml"  # Replace with your file name
#     target_key = "node-0.qihang-winter0.ragger-pg0.utah.cloudlab.us"  # Replace with the key you want to replace
#     old_value = "original_value"  # Replace with the old value you want to replace
#     new_value = "new_value"  # Replace with the new value you want to replace with

#     process_files(folder_path, file_name, target_key, old_value, new_value)
