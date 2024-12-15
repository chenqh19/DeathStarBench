# Add Docker's official GPG key:
yes | sudo apt-get update
yes | sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
tes | sudo apt-get update

yes | sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
yes | sudo apt install docker-compose
yes | sudo apt-get install luarocks
yes | sudo luarocks install luasocket
sudo apt install htop
sudo apt install intel-cmt-cat
yes | sudo apt install pip

sudo docker run hello-world

cd ../wrk2
make
cd ../scripts

yes | sudo apt-get install pqos
sudo modprobe msr
sudo pqos -s

sudo apt install linux-tools-common
yes | sudo apt install linux-tools-5.4.0-196-generic

cd ../socialNetwork
sudo docker build -t qihang-sn .
cd ../scripts

cd ../hotelReservation
sudo docker build -t qihang-hr .
cd ../scripts

sudo chmod +x kuber-deploy/kuber_install.sh
# ./kuber_install.sh

pip install aiohttp
pip install prometheus-api-client
pip install pytz
pip install gurobipy
pip install gevent
pip install scipy
