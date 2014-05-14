# Makefile

VIRTUALENV = venv/
TIME = `date +%s`
PWD = `pwd`


centos-install:
	make centos-packages
	make virtualenv
	make pip
	make database-prod

centos-install-nopip:
	make centos-packages	
	make centos-nopip
	make virtualenv
	make database-prod	

centos-packages:
	# Activate EPEL respositiory
	rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm || true
	# Install python dependencies
	yum groupinstall -y "Development Tools"
	yum install -y python python-pip python-virtualenv python-devel mysql-devel mysql zlib zlib-devel openssl mod_wsgi python-lxml libxslt-python libxslt-devel
		
centos-nopip:
	# Package usually manage with PIP
	yum install -y python-argparse python-boto python-chardet Django14 python-django-appconf python-django-compressor python-gunicorn python-mimeparse mysql-connector-python MySQL-python python-dateutil pytz python-six python-django-south	

load-vendor:
	# Create a vendor directory with dependancies outside EPEL
	mkdir vendor -p	
	cd vendor; wget https://github.com/mjtorn/wadofstuff-django-serializers/archive/master.zip -O wds.zip; unzip wds.zip
	cd vendor; wget https://github.com/mazelife/django-redactor/archive/master.zip -O dr.zip; unzip dr.zip
	cd vendor; rm *.zip	

pip:
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt --allow-all-external --allow-unverified wadofstuff-django-serializers || . venv/bin/activate; pip install -r requirements.txt

virtualenv:	
	virtualenv venv --system-site-packages --distribute

database:
	python ./manage.py syncdb --noinput
	python ./manage.py migrate
	
database-prod:
	python ./manage.py syncdb --noinput --settings=app.settings_prod
	python ./manage.py migrate --settings=app.settings_prod

staticfiles:
	. $(VIRTUALENV)bin/activate; python ./manage.py collectstatic --noinput --settings=app.settings_prod
	. $(VIRTUALENV)bin/activate; python ./manage.py compress --force --settings=app.settings_prod

setup_staticfiles:
	ln -sfT `pwd`/app/barometre/static/barometre/img/ ./app/static/CACHE/img

run:
	. $(VIRTUALENV)bin/activate;  python ./manage.py runserver

simulate-prod: 
	. $(VIRTUALENV)bin/activate; python ./manage.py runserver --insecure --settings=app.settings_prod

distribute:
	mkdir dist -p
	make load-vendor
	make staticfiles
	tar -czvf dist/idf-barometre-$(TIME).tar.gz * --exclude=dist --exclude=.git --exclude=*.db --exclude=venv
	cp dist/idf-barometre-$(TIME).tar.gz dist/idf-barometre-latest.tar.gz	