.PHONY: clean

clean:
	find . -name '__pycache__' -exec rm -rf {} +
	rm -rf gen
	rm -rf htmlcov
	rm -f .coverage
