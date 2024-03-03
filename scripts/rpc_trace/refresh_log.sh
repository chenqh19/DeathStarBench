sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep home-timeline-service) rm -rf /social-network-microservices/*.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep home-timeline-service) rm -rf /logs/*
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep post-storage-service) rm -rf /social-network-microservices/*.txt
sudo docker exec $(sudo docker ps --format "{{.Names}}" | grep post-storage-service) rm -rf /logs/*