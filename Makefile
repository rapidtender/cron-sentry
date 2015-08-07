release:
	python setup.py sdist register upload

test:
	@pip install pytest mock raven
	PYTHONPATH=. py.test -v tests/
