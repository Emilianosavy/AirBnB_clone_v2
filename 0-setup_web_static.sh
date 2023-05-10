#!/usr/bin/env bash
# This script sets up webservers for deployment of AirBnB webstatic
apt-get -y update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test/ 
mkdir -p /data/web_static/shared/
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\t<h1>Hello ALX</h1>\n\t</body>\n</html>" > /data/web_static/releases/test/index.html
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i "s/^\s*location \/ {/\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}\n\n&/" /etc/nginx/sites-enabled/default
service nginx restart
