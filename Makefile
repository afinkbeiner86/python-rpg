build-exe:
		python setup.py build

build-msi:
		python setup.py bdist_msi

cleanup:
		rm -rf ./build/*
		rm -rf ./dist/*