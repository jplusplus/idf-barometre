# Baromètre Île-de-France

## Installation sur CentOS

### 1. Téléchargement du projet

Depuis le dossier qui contiendra votre projet :

```bash
wget https://dl.dropboxusercontent.com/s/5le8l1aah47y080/idf-barometre-1385733476.tar.gz -O idf-barometre.tar.gz
mkdir -p idf-barometre && tar -xzvf idf-barometre.tar.gz -C idf-barometre
```

Cette dernière commande va extraire le projet dans le dossier idf-barometre.

### 2. Configuration du projet
Utilisez des variables d'environnement pour configurer le projet :

* **DATABASE_URL** définit le `Universal Resource Locator` qui permet d'accéder à la base de données (ex: *mysql://user:psswd@localhost/barometre*)
* **DJANGO\_SETTINGS\_MODULE** (facultatif) définit le fichier de configuration alternatif à utiliser (ex: *settings_heroku.py*)


### 3. Installation des dépendances et de la base

**En root** et depuis le dossier **idf-barometre**  :

```bash
make centos-install
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

### 4bis. Tester le bon fonctionnement du projet

Si vous voulez tester le bon fonctionnement du projet avant la mise en production, lancez :

```bash
make run
```

## Licence
Copryright © Region île-de-France
