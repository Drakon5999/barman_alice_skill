all: clean dependencies package

clean:
	rm -rf dist/

dirs:
	mkdir -p dist/

dependencies: dirs
	pip3 install -r requirements_ycf.txt --target dist/

install-code: dirs
	cp api.py dist/api.py
	cp -r sources dist/sources
	cp -r data dist/data

package: dirs install-code
	rm -f dist.zip
	cd dist && zip --exclude '*.pyc' -r ../dist.zip ./*

.PHONY: clean dirs dependencies install-code package all