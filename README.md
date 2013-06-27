# Baromètre Île-de-France

## Installation

### Dépendance logiciels
Pour fonctionner l'application a besoin de :

* **Python** 2.7.+
* **MySQL** 14.+
* A database connector/interface for python (Ex: *python-mysqldb*)
* **Pip** (package manager)
* **Virtualenv** 1.8.4

Sur Ubuntu/Debian, installez les packages suivants pour utiliser MySQL :

    $ sudo apt-get install build-essential python-pip python-dev libjpeg-dev mysql 

### Initialiser Virtualenv
À la racine du projet lancez cette commande pour initialiser l'environement virtuel dans ce dossier :

    $ virtualenv venv --distribute

Puis activer le :
    
    $ source venv/bin/activate


### Package python
Pour télécharger et installer les dépendances du projet dans l'environement virtuel, lancez depuis ça racine:

    $ pip install -r requirements.txt

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

date | question | profil | reponse  | ratio
--- | --- | --- | --- | ---
01/02/2011 | Transport | Total | ratio | 57
01/02/2011 | Transport | Homme | ratio | 58
01/02/2011 | Transport | Femme | ratio | 58
... |

## License
Copryright © Region île-de-France
