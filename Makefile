.PHONY: certs clean run

certs:
	python scripts/generate_certs.py

run: certs
	python app.py

clean:
	-rm -f *.pem *.crt *.key
