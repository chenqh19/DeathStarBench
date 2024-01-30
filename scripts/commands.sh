# sock shop
sudo docker run --net=host weaveworksdemos/load-test -h localhost -r 100 -c 2

# social network
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/read-home-timeline.lua http://localhost:8080/wrk2-api/home-timeline/read -R 2000
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/read-user-timeline.lua http://localhost:8080/wrk2-api/user-timeline/read -R 2000
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 2000
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/social-network/mixed-workload.lua http://localhost:8080 -R 2000
# hotel reservation
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://127.0.0.1:5000 -R 3000
# kubernetes
sudo kubeadm token create --print-join-command # on the host
kubectl patch svc frontend -p '{"spec":{"externalIPs":["192.168.0.194"]}}'
../wrk2/wrk -D exp -t 100 -c 100 -d 30 -L -s ./wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://192.168.0.194:5000 -R 3000