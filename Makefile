## Installs development requirements
install:
	python3 -m pip install --upgrade pip
	# Packaging
	pip3 install setuptools wheel
	# Linting
	pip3 install flake8 isort
	# Testing
	pip3 install pytest
	# Basic requirements
	pip3 install -r tools/requirements.txt
	# Logs directory
	#mkdir -p logs

## Runs flake8 on module, exit if critical rules are broken
lint:
	isort src tests --diff --color --check-only
	flake8 src tests --ignore=E501

## Executes robot logic
start:
	uvicorn src.main:app --reload

## Removes cache files
clean:
	rm -rf .pytest_cache
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

## Runs pytest
test:
	pytest tests -p no:logging -p no:warnings


.PHONY: install lint package clean test