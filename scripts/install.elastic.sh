#!/bin/sh

sudo apt-get --yes --assume-yes install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
sudo apt-get --yes --assume-yes update && sudo apt-get --yes --assume-yes --allow-unauthenticated install elasticsearch
sudo systemctl start elasticsearch.service