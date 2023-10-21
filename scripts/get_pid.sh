#!/bin/bash

# 获取所有运行中的 Docker 容器的 ID
container_ids=$(sudo docker ps -q)

# 指定多个关键词
keywords=("Text")

# 初始化变量来存储所有的 PID
all_pids=""

# 循环遍历每个容器 ID 并运行 sudo docker top
for container_id in $container_ids; do
    echo "Running sudo docker top for container $container_id"
    top_result=$(sudo docker top $container_id)
    
    found=false
    
    # 使用 awk 和 grep 提取包含关键词的行，并获取 PID
    for keyword in "${keywords[@]}"; do
        pid_list=$(echo "$top_result" | awk -v keyword="$keyword" '$8 ~ keyword {print $2}')
        if [ -n "$pid_list" ]; then
            found=true
            if [ -n "$all_pids" ]; then
                all_pids="${all_pids},${pid_list}"
            else
                all_pids="${pid_list}"
            fi
            break
        fi
    done
    
    if [ "$found" = true ]; then
        echo "Container $container_id contains processes with one of the keywords: ${keywords[*]}"
    fi
done

# 输出所有提取的 PID，用逗号隔开
echo "All PIDs with one of the keywords: ${keywords[*]}: $all_pids"
