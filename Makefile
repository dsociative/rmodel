ENV=$(PWD)/env

all: clean env

env:
	virtualenv env
	. $(ENV)/bin/activate; easy_install pip; pip install --process-dependency-links --download-cache ~/pip -r $(PWD)/requirements.txt

clean:
	rm -rf $(ENV)

test:
	nosetests --config nosetests.cfg rmodel

