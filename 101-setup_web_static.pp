# This script sets up webservers for the deployment of the webstatic

exec {'update':
  provider => shell,
  command  => 'apt-get -y update',
}
package {'nginx':
  ensure   => installed,
  provider => 'apt',
}
exec {'folders':
  provider => shell,
  command  => 'mkdir -p /data/web_static/releases/test/ /data/web_static/shared/',
}
exec {'test':
  command => '/bin/echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\t<h1>Hello ALX</h1>\n\t</body>\n</html>" > /data/web_static/releases/test/index.html',
  path    => '/bin',
}
exec {'remove-old-link':
  provider => shell,
  command  => 'rm -rf /data/web_static/current; ln -s /data/web_static/releases/test/ /data/web_static/current',
}
exec {'ownership':
  provider => shell,
  command  => 'chown -R ubuntu:ubuntu /data/',
}
service {'nginx':
  ensure  => 'running',
  enable  => true,
  require => Package['nginx'],
}
exec {'configure':
  command => '/bin/sed -i "s/^\\s*location \\/ {/\\tlocation \\/hbnb_static {\\n\\t\\talias \\/data\\/web_static\\/current\\/;\\n\\t}\\n\\n&/" /etc/nginx/sites-enabled/default',
  path    => '/bin',
  unless  => '/bin/grep -q "^\\s*location \\/hbnb_static {" /etc/nginx/sites-enabled/default',
}
exec {'restart':
  command     => '/usr/sbin/service nginx restart',
  refreshonly => true,
  subscribe   => Service['nginx'],
}
