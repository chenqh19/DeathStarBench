echo -e "\n+++++++++++++frontend++++++++++++++"
sudo docker logs hotel_reserv_frontend > frontend_logs.txt
echo -e "\n++++++++++++++user++++++++++++++"
sudo docker logs hotel_reserv_user > user_logs.txt
echo -e "\n+++++++++++++reservation++++++++++++++"
sudo docker logs hotel_reserv_reservation > reservation_logs.txt
echo -e "\n+++++++++++++recommendation++++++++++++++"
sudo docker logs hotel_reserv_recommendation > recommendation_logs.txt
echo -e "\n+++++++++++++search++++++++++++++"
sudo docker logs hotel_reserv_search > search_logs.txt
echo -e "\n+++++++++++++geo++++++++++++++"
sudo docker logs hotel_reserv_geo > geo_logs.txt
echo -e "\n+++++++++++++rate++++++++++++++"
sudo docker logs hotel_reserv_rate > rate_logs.txt
echo -e "\n+++++++++++++profile++++++++++++++"
sudo docker logs hotel_reserv_profile > profile_logs.txt
# sudo docker logs hotel_reserv_ > _logs.txt
# sudo docker logs hotel_reserv_ > _logs.txt
# sudo docker logs hotel_reserv_ > _logs.txt
# sudo docker logs hotel_reserv_ > _logs.txt
# sudo docker logs hotel_reserv_ > _logs.txt
# sudo docker logs hotel_reserv_ > _logs.txt