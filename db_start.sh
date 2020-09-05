# run as sudo

mkdir ~/data/db -p
mongod --dbpath ~/data/db --bind_ip 0.0.0.0 -v > mongod.log &