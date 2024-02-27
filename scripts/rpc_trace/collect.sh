sudo docker cp socialnetwork-home-timeline-service-1:/social-network-microservices/ReadPostsA.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-home-timeline-service-1:/logs/write_log.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-post-storage-service-1:/social-network-microservices/ReadPostsB.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-post-storage-service-1:/logs/read_log.txt ~/DeathStarBench/scripts/rpc_trace/

sed -i 's/[^[:print:]\t]//g' ~/DeathStarBench/scripts/rpc_trace/*