# Baromètre Île-de-France

## Installation des pré-requis sur CentOS

Pour fonctionner le projet a besoin de certains binaires installables via EPEL :
```bash
rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm || true
yum groupinstall -y "Development Tools"
yum install -y python python-virtualenv python-devel mysql-devel mysql zlib zlib-devel openssl mod_wsgi python-lxml libxslt-python libxslt-devel python-argparse python-boto python-chardet Django14 python-django-appconf python-django-compressor python-gunicorn python-mimeparse mysql-connector-python MySQL-python python-dateutil pytz python-six python-django-south   
```

Voici la liste binaires installés
* mod_wsgi
* mysql
* openssl
* python
* pytz
* zlib
* zlib-devel
* libxslt-python
* libxslt-devel
* **divers modules Python** listés dans ```requirements.txt```.

## Téléchargement et installation du livrable auto-suffisant

Une fois les dépendances ci-dessus installées, vous pouvez télécharger l'archive suivante :

```bash
wget https://www.dropbox.com/s/72jmplf1n8ji3nl/idf-barometre-latest.tar.gz?dl=1 -O idf-barometre.tar.gz
mkdir -p idf-barometre && tar -xzvf idf-barometre.tar.gz -C idf-barometre
```

### Configuration de la base de données

Le fichier ``app/settings_prod.py`` vous permet d'éditer la confugration du projet. Dans ce fichier,
éditez les valeurs de DATABASE_URL en fonction de votre base de données:

```python
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        # Adaptez ici les valeurs
        'USER': '',
        'PASSWORD': '', 
        'NAME': '',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```


### Synchronisation de la base de données

**La base de données doit être synchronisée au moins une fois lorsque l'application est instalée :**

```bash
make database-prod
```

### Configuration de apache

Utilisez la configuration suivante dans vos virutal hosts (en remplaçant les valeurs ```<DOMAIN>``` et ```<CHEMIN_VERS_LE_PROJET>```) :

    <VirtualHost *:80>
        ServerName <DOMAIN>
        ServerAlias www.<DOMAIN>
        DocumentRoot <CHEMIN_VERS_LE_PROJET>
        LogLevel warn
        WSGIScriptAlias / <CHEMIN_VERS_LE_PROJET>/app/wsgi.py

        WSGIDaemonProcess <DOMAIN> python-path=<CHEMIN_VERS_LE_PROJET>
        WSGIProcessGroup <DOMAIN>

        Alias /static/ <CHEMIN_VERS_LE_PROJET>/app/static/
        <Directory <CHEMIN_VERS_LE_PROJET>/app/static/>
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Enfin, redémarrez Apache pour accéder à l'application.