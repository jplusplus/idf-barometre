# Makefile

VIRTUALENV = venv/
TIME = `date +%s`

centos-packages:
	# Activate EPEL respositiory
	cd /opt
	rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm || true
	# Install python dependencies
	yum groupinstall -y "Development Tools"
	yum install -y python python-pip python-devel mysql-devel mysql zlib zlib-devel openssl mod_wsgi libxml2 libxml2-devel python-lxml  libxslt-python  libxslt-devel
	# Install virtual env
	python-pip install virtualenv

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

run:
	. $(VIRTUALENV)bin/activate; python ./manage.py runserver

distribute:
	mkdir dist -p
	tar -czvf dist/idf-barometre-$(TIME).tar.gz * --exclude=dist --exclude=.git --exclude=*.db