setup:
	pip3 install -r utilities/dependencies.txt
	chmod u+x main.py

run:
	./main.py ''

clean:
	rm -rf __pycache__