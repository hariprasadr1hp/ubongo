.PHONY: all clean test

all:
	python main.py
	
clean:
	rm -f *.pyc

test:
	mypy .