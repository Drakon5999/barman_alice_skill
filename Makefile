all: clean dependencies package

clean:
	rm -rf dist/

dirs:
	mkdir -p dist/

dependencies: dirs
	pip3 install -r requirements.txt --target dist/ --system

install-code: dirs
	cp api.py dist/api.py
	cp tmp.py dist/tmp.py
	cp dumped_cocktails.json dist/dumped_cocktails.json

package: dirs install-code
	rm -f dist.zip
	cd dist && zip --exclude '*.pyc' -r ../dist.zip ./*

.PHONY: clean dirs dependencies install-code package all