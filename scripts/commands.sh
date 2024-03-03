# sock shop
sudo docker run --net=host weaveworksdemos/load-test -h localhost -r 100 -c 2
# kubernetes
kubectl create namespace sock-shop
kubectl apply -f complete-demo.yaml
kubectl patch svc front-end -p '{"spec":{"externalIPs":["192.168.0.194"]}}' -n sock-shop


# social network
python3 scripts/init_social_graph.py --compose --graph=socfb-Reed98, ego-twitter, or soc-twitter-follows-mun
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/read-home-timeline.lua http://localhost:8080/wrk2-api/home-timeline/read -R 2000
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/read-user-timeline.lua http://localhost:8080/wrk2-api/user-timeline/read -R 2000
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 2000
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/mixed-workload.lua http://localhost:8080 -R 2000

# jaeger
ssh -L 16686:127.0.0.1:16686 chenqh23@hp***.utah.cloudlab.us

# swarm
sudo docker swarm init --advertise-addr 10.0.1.1

# hotel reservation
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://127.0.0.1:5000 -R 3000
# kubernetes
sudo kubeadm token create --print-join-command # on the host
sudo docker login
./kubernetes/scripts/build-docker-images.sh
sudo kubectl apply -Rf ./kubernetes/
kubectl patch svc frontend -p '{"spec":{"externalIPs":["192.168.0.194"]}}'
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://192.168.0.194:5000 -R 3000
kubectl delete --all deployments
crictl inspect --output go-template --template '{{.info.pid}}' <container-id>

sudo docker exec -it <container-name> bash
