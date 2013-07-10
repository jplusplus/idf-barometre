# Baromètre Île-de-France

## Installation

### Dépendance logiciels
Pour fonctionner l'application a besoin de :

* **Python** 2.7.+
* **MySQL** 14.+
* A database connector/interface for python (Ex: *python-mysqldb*)
* **Pip** (package manager)
* **Virtualenv** 1.8.4

#### Ubuntu/Debian
Installez les packages suivants pour utiliser MySQL :

    $ sudo apt-get install build-essential python python-pip python-dev mysql nodejs npm
    
Installer Virtualenv en root avec pip

    $ sudo pip install virtualenv
    
#### CentOS
Ajouter d'abord les dépôts EPEL (depuis *root*) :

    $ su -
    $ cd /opt
    $ wget http://mirrors.nl.eu.kernel.org/fedora-epel/6/i386/epel-release-6-8.noarch.rpm
    $ rpm -Uvh epel-release-6-8.noarch.rpm
    $ rm epel-release-6-8.noarch.rpm -f

Désormais, vous pouvez installer les packages suivants (toujours en *root*) :

    $ yum groupinstall "Development Tools"
    $ yum install python python-pip python-devel mysql-devel mysql zlib zlib-devel openssl nodejs npm
    $ python-pip virtualenv
    
    
### Installer ```lessc``` et ```coffee```

Revenez à la racine du projet :
    
    $ cd <CHEMIN_VERS_LE_PROJECT>

Puis compiler les assets (feuilles de style et javascript), installez les dépendances *node* suivantes :

    $ cat npm_requirements.txt | xargs npm -g install

### Initialiser Virtualenv
Toujours depuis la racine du projet, lancez cette commande pour initialiser l'environement virtuel dans ce dossier :

    $ virtualenv venv --distribute

Puis activez le :
    
    $ source venv/bin/activate


### Package python
Pour télécharger et installer les dépendances du projet dans l'environement virtuel, lancez depuis ça racine...

Sur Ubuntu/Debian :

    $ pip install -r requirements.txt

Sur CentOS :

    $ ./venv/bin/pip install -r requirements.txt


### Configuration
La configuration du projet se fait en deux étapes

#### 1. Variables d'environement 
Utilisez des variables d'environement pour configurer le projet :

* **DATABASE_URL** définie le `Universal Resource Locator` qui permet d'accéder à la base de données (ex: *mysql://user:psswd@localhost/barometre*)
* **DJANGO\_SETTINGS\_MODULE** définie le fichier de configuration alternatif à utiliser (ex: *settings_prod.py*)


*Astuce: vous pouvez égualement utiliser [autoenv](https://github.com/kennethreitz/autoenv) pour charger virtualenv et ces variables d'environement automatiquement lorsque vous atteignez le dossier avec `cd`.*

#### 2. Modifier le fichier de configuration
À l'aide de la variable **DJANGO\_SETTINGS\_MODULE**, vous pouvez éditer les réglages par défaut du projet dans un nouveau fichier. Un exemple d'utilisation de Amazon S3 pour la gestion des fichiers statiques et disponible dans `/app/settings_heroku.py`.

### Synchroniser la base de données
Une fois que vous avez configuré la variable **DATABASE_URL**, lancez la commande suivante pour synchroniser la base de données avec le projet :

    $ python manage.py syncdb

### Lancement
Pour lancer le projet sur le port 8000 et vérifier que tout fonctionne, entrez :

    $ python manage.py runserver 8000

Vous devriez voir un résultat proche du suivant :

    Validating models...

    0 errors found
    Django version 1.4.3, using settings 'settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Votre application est désormais accéssible sur [http://127.0.0.1:8000](http://127.0.0.1:8000) !

## Format de fichier pour upload

Veillez à respecter cette struture de fichier, le format des dates (colonne *date*) et celui des poourcentages (colonne *ratio*) :

date | question | profil |ratio
--- | --- | --- | ---
01/02/2011 | Transport | Total | 57
01/02/2011 | Transport | Homme | 58
01/02/2011 | Transport | Femme | 58
... |

## License
Copryright © Region île-de-France
