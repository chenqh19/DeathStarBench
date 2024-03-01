sudo docker cp socialnetwork-home-timeline-service-1:/social-network-microservices/ReadPostsA.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-home-timeline-service-1:/logs/write_log.txt ~/DeathStarBench/scripts/rpc_trace/htl-write_log.txt
sudo docker cp socialnetwork-home-timeline-service-1:/social-network-microservices/ReadPostsB.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-home-timeline-service-1:/logs/read_log.txt ~/DeathStarBench/scripts/rpc_trace/htl-read_log.txt

sudo docker cp socialnetwork-post-storage-service-1:/social-network-microservices/ReadPostsC.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-post-storage-service-1:/logs/read_log.txt ~/DeathStarBench/scripts/rpc_trace/ps-read_log.txt
sudo docker cp socialnetwork-post-storage-service-1:/social-network-microservices/ReadPostsD.txt ~/DeathStarBench/scripts/rpc_trace/
sudo docker cp socialnetwork-post-storage-service-1:/logs/write_log.txt ~/DeathStarBench/scripts/rpc_trace/ps-write_log.txt

sed -i 's/[^[:print:]\t]//g' ~/DeathStarBench/scripts/rpc_trace/*
grep -E -a 'ReadPosts|uber-trace-id' ReadPostsA.txt > tmp.txt && mv tmp.txt ReadPostsA.txt
grep -E -a 'ReadPosts|uber-trace-id' ReadPostsB.txt > tmp.txt && mv tmp.txt ReadPostsB.txt
grep -E -a 'ReadPosts|uber-trace-id' ReadPostsC.txt > tmp.txt && mv tmp.txt ReadPostsC.txt
grep -E -a 'ReadPosts|uber-trace-id' ReadPostsD.txt > tmp.txt && mv tmp.txt ReadPostsD.txt

grep -E -a 'ReadPosts|uber-trace-id' htl-read_log.txt > tmp.txt && mv tmp.txt htl-read_log.txt
grep -E -a 'ReadPosts|uber-trace-id' htl-write_log.txt > tmp.txt && mv tmp.txt htl-write_log.txt
grep -E -a 'ReadPosts|uber-trace-id' ps-read_log.txt > tmp.txt && mv tmp.txt ps-read_log.txt
grep -E -a 'ReadPosts|uber-trace-id' ps-write_log.txt > tmp.txt && mv tmp.txt ps-write_log.txt