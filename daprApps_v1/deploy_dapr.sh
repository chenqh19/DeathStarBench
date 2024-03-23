cd ../scripts
./install_dependencies.sh
cd kuber-deploy/
./kuber_install.sh 1
cd ../../daprApps_v1

curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm

sudo helm repo add bitnami https://charts.bitnami.com/bitnami
kubectl create namespace yanqizhang
