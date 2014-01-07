# Makefile

VIRTUALENV = venv/
TIME = `date +%s`

centos-packages:
	yum groupinstall -y "Development Tools"
	yum install -y python python-pip python-devel mysql-devel mysql zlib zlib-devel openssl mod_wsgi libxml2 libxml2-de python-lxml  libxslt-python  libxslt-devel
	python-pip virtualenv
	make database

virtualenv:
	virtualenv venv --no-site-packages --distribute
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt

database:
	. $(VIRTUALENV)bin/activate; python ./manage.py syncdb --noinput
	. $(VIRTUALENV)bin/activate; python ./manage.py migrate

staticfiles:
	. $(VIRTUALENV)bin/activate; python ./manage.py collectstatic --noinput
	. $(VIRTUALENV)bin/activate; python ./manage.py compress --force

distribute:
	mkdir dist -p
	tar -czvf dist/idf-barometre-$(TIME).tar.gz * --exclude=dist --exclude=.git --exclude=*.db
