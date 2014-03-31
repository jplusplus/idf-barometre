# Baromètre Île-de-France

## Installation sur CentOS

### 1. Téléchargement du projet

Depuis le dossier qui contiendra votre projet :

```bash
wget https://www.dropbox.com/s/72jmplf1n8ji3nl/idf-barometre-latest.tar.gz?dl=1 -O idf-barometre.tar.gz
mkdir -p idf-barometre && tar -xzvf idf-barometre.tar.gz -C idf-barometre
```

Cette dernière commande va extraire le projet dans le dossier idf-barometre.

### 2. Configuration du projet
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

### 3. Installation des dépendances et de la base

**En root** et depuis le dossier **idf-barometre**  :

```bash
make centos-install-nopip
```

### 4. Configuration d'Apache

Utilisez la configuration suivante dans vos virutal hosts (en remplaçant les valeurs ```<DOMAIN>``` et ```<CHEMIN_VERS_LE_PROJET>```) :

    <VirtualHost *:80>
        ServerName <DOMAIN>
        ServerAlias www.<DOMAIN>
        DocumentRoot <CHEMIN_VERS_LE_PROJET>
        LogLevel warn
        WSGIScriptAlias / <CHEMIN_VERS_LE_PROJET>/app/wsgi.py

        WSGIDaemonProcess <DOMAIN> python-path=<CHEMIN_VERS_LE_PROJET>:<CHEMIN_VERS_LE_PROJET>/venv/lib/python2.7/site-packages
        WSGIProcessGroup <DOMAIN>

        Alias /static/ <CHEMIN_VERS_LE_PROJET>/app/static/
        <Directory <CHEMIN_VERS_LE_PROJET>/app/static/>
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Enfin, redémarrez Apache pour accéder à l'application.


## Licence
Copryright © Region île-de-France
