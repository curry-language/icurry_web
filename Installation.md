Prerequisite: python3 and pip3 (package manager for python3) are installed ``sudo apt install python3 python3-pip``

move the webapp directory ('webapp') into the directory intended to be used for the wsgi-app, for example /var/www: ``cp -r /path/to/icurry_web/webapp /var/www/icurry_web/``

Install Flask *globally*: ``sudo pip3 install Flask==2.3.1``

create and grant read and write-priviliges of cache-directories ``/path/to/webapp/svgs`` and ``[...]/progs`` to the webserver-user (www-data with apache). The webapp can technically create those by itself, but apache will not execute any setup script within the app:
```
sudo mkdir /var/www/icurry_web/svgs
sudo mkdir /var/www/icurry_web/progs
sudo chown www-data:www-data /var/www/icurry_web/svgs
sudo chown www-data:www-data /var/www/icurry_web/progs
```



place icurry executable somewhere on the system after having compiled it from the icurry package, for example directly into /bin or /usr/bin

Set the ``ICURRY_PATH`` and ``WEBAPP_PATH`` settings in ``webapp_settings.py`` (not forgetting a forwardslash at the end of the paths). ``ICURRY_PATH`` can be left empty, if icurry is in the system-wide path.



## For Apache

install mod-wsgi for apache and python3: ``sudo apt install libapache2-mod-wsgi-py3``

activate mod-wsgi: ``sudo a2enmod wsgi``

copy icurry_web.conf to ``/etc/apache2/sites-available``, and integrate TLS configuration if needed

deactivate apache default-site (usually ``sudo a2dissite 000-default.conf``)

activate icurry_web site: ``sudo a2ensite icurry_web.conf``

restart apache: ``sudo service apache2 restart``



## External cache cleaning

In order to clean the webapps cache in regularly spaced intervals and not every time a visualisation request happens to be received by the server, the following can be set as a cronjob:

```
# m h  dom mon dow   command
  0 *  *   *   *     python3 /var/www/icurry_web/cache_cleaner.py
```

This needs to be run with elevated privileges or as the weserver-user, as the cache entries are owned by that user.

When this cronjob is installed, the internal cache cleaner of the webapp can be disabled by setting the ``INTERNAL_CACHE_CLEANER`` variable inside the ``webapp_settings.py`` to False