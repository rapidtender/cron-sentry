release:
	python setup.py sdist register upload

test: install_test_deps
	PYTHONPATH=. py.test -v tests/

install_test_deps:
	@pip install pytest mock raven