# Makefile

VIRTUALENV = venv/

centos-packages:
	yum groupinstall -y "Development Tools"
	yum install -y python python-pip python-devel mysql-devel mysql zlib zlib-devel openssl mod_wsgi libxml2 libxml2-de python-lxml  libxslt-python  libxslt-devel
	python-pip virtualenv

virtualenv:
	virtualenv venv --no-site-packages --distribute
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt

staticfiles:
	. $(VIRTUALENV)bin/activate; python ./manage.py collectstatic --noinput
	. $(VIRTUALENV)bin/activate; python ./manage.py compress --force

