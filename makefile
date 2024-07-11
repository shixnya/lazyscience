.PHONY: build upload clean

build:
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

clean:
	rm -rf dist build *.egg-info