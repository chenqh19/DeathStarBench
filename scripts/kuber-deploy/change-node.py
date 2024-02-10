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

# 1-node
deploy = {
    "frontend" : [["frontend"], [1]],
    "reccomend" : [["recommendation", "mongodb-recommendation"], [1, 1]],
    "reserve" : [["reservation", "mongodb-reservation", "memcached-reservation"], [1, 1, 1]],
    "user" : [["user", "mongodb-user"], [1, 1]],
    "search" : [["search"], [1]],
    "geo" : [["geo", "mongodb-geo"], [1, 1]],
    "profile" : [["profile", "mongodb-profile", "memcached-profile"], [1, 1, 1]],
    "rate" : [["rate", "mongodb-rate", "memcached-rate"], [1, 1, 1]],
    "jaeger": [["jaeger"], [0]],
    "consul": [["consul"], [0]]
}

# all-remote 3
# deploy = {
#     "frontend" : [["frontend"], [3]],
#     "reccomend" : [["recommendation", "mongodb-recommendation"], [1, 3]],
#     "reserve" : [["reservation", "mongodb-reservation", "memcached-reservation"], [1, 3, 2]],
#     "user" : [["user", "mongodb-user"], [1, 3]],
#     "search" : [["search"], [1]],
#     "geo" : [["geo", "mongodb-geo"], [2, 1]],
#     "profile" : [["profile", "mongodb-profile", "memcached-profile"], [2, 1, 3]],
#     "rate" : [["rate", "mongodb-rate", "memcached-rate"], [2, 1, 3]],
#     "jaeger": [["jaeger"], [0]],
#     "consul": [["consul"], [0]]
# }

# all-remote 2
# deploy = {
#     "frontend" : [["frontend"], [3]],
#     "reccomend" : [["recommendation", "mongodb-recommendation"], [1, 3]],
#     "reserve" : [["reservation", "mongodb-reservation", "memcached-reservation"], [1, 3, 3]],
#     "user" : [["user", "mongodb-user"], [1, 3]],
#     "search" : [["search"], [1]],
#     "geo" : [["geo", "mongodb-geo"], [3, 1]],
#     "profile" : [["profile", "mongodb-profile", "memcached-profile"], [3, 1, 1]],
#     "rate" : [["rate", "mongodb-rate", "memcached-rate"], [3, 1, 1]],
#     "jaeger": [["jaeger"], [0]],
#     "consul": [["consul"], [0]]
# }

# search-away
# deploy = {
#     "frontend" : [["frontend"], [3]],
#     "reccomend" : [["recommendation", "mongodb-recommendation"], [3, 3]],
#     "reserve" : [["reservation", "mongodb-reservation", "memcached-reservation"], [3, 3, 3]],
#     "user" : [["user", "mongodb-user"], [3, 3]],
#     "search" : [["search"], [1]],
#     "geo" : [["geo", "mongodb-geo"], [1, 1]],
#     "profile" : [["profile", "mongodb-profile", "memcached-profile"], [1, 1, 1]],
#     "rate" : [["rate", "mongodb-rate", "memcached-rate"], [1, 1, 1]],
#     "jaeger": [["jaeger"], [0]],
#     "consul": [["consul"], [0]]
# }


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
