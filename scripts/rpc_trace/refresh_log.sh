sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep home-timeline-service) rm -rf /social-network-microservices/ReadPostsA.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep home-timeline-service) rm -rf /social-network-microservices/ReadPostsB.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep home-timeline-service) rm -rf /logs/write_log.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep post-storage-service) rm -rf /social-network-microservices/ReadPostsC.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep post-storage-service) rm -rf /social-network-microservices/ReadPostsD.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep post-storage-service) rm -rf /logs/read_log.txt
sudo rm -rf *.txt