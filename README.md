# Baromètre Île-de-France

## Installation

Ce manuel d'installation détaille la procédure pour les distributions Ubuntu et CentOS en 8 étapes :

1. [Installation des dépendances logicielles](#1-installation-des-dpndances-logicielles)
1. [Installation des compilateurs *Less* et *CoffeeScript*](#2-installation-des-compilateurs-less-et-coffeescript)
1. [Initialisation de Virtualenv](#3-initialisation-de-virtualenv)
1. [Installation des packages python](#4-installation-des-packages-python)
1. [Configuration du projet](#5-configuration-du-projet)
1. [Synchronisation de la base de données](#6-synchronisation-de-la-base-de-donnes)
1. [Lancement](#7-lancement-en-dveloppement-facultatif)
1. [Configuration d'Apache](#8-configuration-dapache)


### 1. Installation des dépendances logicielles

#### Ubuntu/Debian
Installez les packages suivants pour :

    $ sudo apt-get install build-essential python python-pip python-dev mysql nodejs npm libapache2-mod-wsgi
    
Installer Virtualenv en root avec pip

    $ sudo pip install virtualenv
    
#### CentOS
Ajoutez d'abord les dépôts EPEL (depuis *root*) :

    $ su -
    $ cd /opt
    $ wget http://mirrors.nl.eu.kernel.org/fedora-epel/6/i386/epel-release-6-8.noarch.rpm
    $ rpm -Uvh epel-release-6-8.noarch.rpm
    $ rm epel-release-6-8.noarch.rpm -f

Désormais, vous pouvez installer les packages suivants (toujours en *root*) :

    $ yum groupinstall "Development Tools"
    $ yum install python python-pip python-devel mysql-devel mysql zlib zlib-devel openssl nodejs npm mod_wsgi
    $ python-pip virtualenv
    
    
### 2. Installation des compilateurs *Less* et *CoffeeScript*

Revenez à la racine du projet :
    
    $ cd <CHEMIN_VERS_LE_PROJECT>

Puis compilez les assets (feuilles de style et javascript), installez les dépendances *node* suivantes :

    $ cat npm_requirements.txt | xargs npm -g install

### 3. Initialisation de Virtualenv
Toujours depuis la racine du projet, lancez cette commande pour initialiser l'environnement virtuel dans ce dossier :

    $ virtualenv venv --distribute

Puis activez le :
    
    $ source venv/bin/activate


### 4. Installation des packages python
Pour télécharger et installer les dépendances du projet dans l'environement virtuel, lancez depuis sa racine...

Sur Ubuntu/Debian :

    $ pip install -r requirements.txt

Sur CentOS :

    $ ./venv/bin/pip install -r requirements.txt


### 5. Configuration du projet
La configuration du projet se fait de deux manières :

#### 5.1. Utiliser des variables d'environement 
Utilisez des variables d'environnement pour configurer le projet :

* **DATABASE_URL** définit le `Universal Resource Locator` qui permet d'accéder à la base de données (ex: *mysql://user:psswd@localhost/barometre*)
* **DJANGO\_SETTINGS\_MODULE** définit le fichier de configuration alternatif à utiliser (ex: *settings_heroku.py*)

*Astuce: vous pouvez égualement utiliser [autoenv](https://github.com/kennethreitz/autoenv) pour charger virtualenv et ces variables d'environnement automatiquement lorsque vous atteignez le dossier avec `cd`.*

#### 5.2. Modifier le fichier de configuration
À l'aide de la variable **DJANGO\_SETTINGS\_MODULE**, vous pouvez éditer les réglages par défaut du projet dans un nouveau fichier. Un exemple d'utilisation de Amazon S3 pour la gestion des fichiers statiques est disponible dans `/app/settings_heroku.py`.

### 6. Synchronisation de la base de données
Une fois que vous avez configuré la variable **DATABASE_URL**, lancez la commande suivante pour synchroniser la base de données avec le projet :

    $ python manage.py syncdb

### 7. Lancement en développement (facultatif)
Pour lancer le projet sur le port 8000 et vérifier que tout fonctionne, entrez :

    $ python manage.py runserver 0.0.0.0:8000

Vous devriez voir un résultat proche du suivant :

    Validating models...

    0 errors found
    Django version 1.4.3, using settings 'settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Votre application est désormais accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000) !

### 8. Configuration d'Apache

Utilisez la configuration suivante dans vos virutal hosts (en remplaçant les valeurs ```<DOMAIN>``` et ```<CHEMIN_VERS_LE_PROJET>```) :

    <VirtualHost *:80>
        ServerName <DOMAIN>
        ServerAlias www.<DOMAIN>
        DocumentRoot <CHEMIN_VERS_LE_PROJET>
        LogLevel warn
        WSGIScriptAlias / <CHEMIN_VERS_LE_PROJET>/app/wsgi.py

        Alias /static/ <CHEMIN_VERS_LE_PROJET>/app/static/
        <Directory <CHEMIN_VERS_LE_PROJET>/app/static/>
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Enfin, redémarrez Apache pour accéder à l'application.


## Format de fichier pour upload

Veillez à respecter cette struture de fichier, le format des dates (colonne *date*) et celui des poourcentages (colonne *ratio*) :

date | question | profil |ratio
--- | --- | --- | ---
01/02/2011 | Transport | Total | 57
01/02/2011 | Transport | Homme | 58
01/02/2011 | Transport | Femme | 58
... |

## Licence
Copryright © Region île-de-France
