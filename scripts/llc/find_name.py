import docker

def find_containers_with_haha():
    # 创建 Docker 客户端
    client = docker.from_env()

    try:
        # 获取所有容器
        containers = client.containers.list()

        # 遍历容器，找到名字中包含"haha"的容器
        for container in containers:
            if "haha" in container.name:
                print("Container name:", container.name)
    except docker.errors.APIError as e:
        print("An error occurred while communicating with the Docker daemon:", e)

if __name__ == "__main__":
    find_containers_with_haha()