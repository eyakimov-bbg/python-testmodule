all: build

build:
	python3.6 setup.py build_ext --inplace

clean:
	rm -Rf build *.so
	

