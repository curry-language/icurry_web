webapp ins verzeichnis für die wsgi-app bewegen, zB: /var/www: cp -r /path/to/icurry_web/webapp /var/www/icurry_web/

pip3 install: sudo apt install python3-pip

Flask *global* installieren: sudo pip3 install Flask



! cache-verzeichnisse /path/to/webapp/svgs and /progs dem webserver-nutzer zuschreiben / bzw. entsprechende lese/schreibrechte einräumen (www-data bei apache)

Einstellungen für ICURRY_PATH und WEBAPP_PATH in icurry_web.py setzen



## Für Apache

Mod-wsgi für apache installieren: libapache2-mod-wsgi-py3

mod-wsgi aktivieren: sudo a2enmod wsgi

icurry_web.conf in ``/etc/apache2/sites-available`` kopieren, ggf. konfiguration für TLS integrieren

apache default-site deaktivieren (normalerweise ``sudo a2dissite 000-default.conf``)

icurry_web site aktivieren: ``sudo a2ensite icurry_web.conf``

