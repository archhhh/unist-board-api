mkdir ~/data/db -p
rm mongod.log
touch mongod.log
sudo mongod --dbpath ~/data/db --bind_ip 0.0.0.0 -v > ./mongod.log &