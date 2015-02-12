release:
	python setup.py sdist register upload
	python2.6 setup.py bdist_egg register upload
	python2.7 setup.py bdist_egg register upload

test:
	@pip install pytest mock
	py.test -v tests/
