.PHONY: clean setup virtualenv build clean_build uninstall install test publish_test publish_prod help setup_venv uninstall_proactive

PYTHON=python3

clean:
	@echo "Cleaning up project..."
	@./gradlew -q clean
	@echo "Project clean complete."

setup:
	@echo "Setting up project..."
	@./gradlew -q setup
	@echo "Project setup complete."

setup_venv:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv env
	@. env/bin/activate && $(PYTHON) -m pip install --upgrade pip setuptools twine
	@. env/bin/activate && $(PYTHON) -m pip install -r requirements.txt
	@. env/bin/activate && $(PYTHON) -m pip -V
	@echo "Virtual environment is ready."

virtualenv:
	@if [ -d "env" ]; then \
		echo "Virtual environment already exists."; \
		read -p "Do you want to delete it and create a new one? [y/N] " answer; \
		case $$answer in \
			[Yy]* ) \
				echo "Deleting and recreating the virtual environment..."; \
				rm -rf env; \
				$(MAKE) setup_venv;; \
			* ) \
				echo "Using the existing virtual environment.";; \
		esac \
	else \
		$(MAKE) setup_venv; \
	fi

build:
	@echo "Building package..."
	@rm -rf dist
	@. env/bin/activate && $(PYTHON) build.py sdist --formats=zip
	@echo "Package built."

clean_build: setup virtualenv build

uninstall_proactive:
	@echo "Uninstalling proactive package..."
	@. env/bin/activate && $(PYTHON) -m pip uninstall -y proactive
	@echo "Proactive package uninstalled."

install: uninstall_proactive
	@echo "Installing proactive from dist..."
	@. env/bin/activate && $(PYTHON) -m pip install dist/proactive*.zip
	@echo "Proactive installed."

test: get_env
	@echo "Running tests..."
	@. env/bin/activate && $(PYTHON) -m pytest --metadata proactive_url $(PROACTIVE_URL) --metadata username $(PROACTIVE_USERNAME) --metadata password $(PROACTIVE_PASSWORD) --junit-xml=build/reports/TEST-report.xml
	@echo "Tests completed."

publish_test:
	@echo "Publishing to TestPyPI..."
	@. env/bin/activate && twine upload --repository-url https://test.pypi.org/legacy/ dist/* --config-file .pypirc
	@echo "Publishing completed."

publish_prod:
	@echo "Publishing to PyPI..."
	@. env/bin/activate && twine upload dist/* --config-file .pypirc
	@echo "Publishing completed."

help:
	@cat Makefile

get_env:
	$(eval PROACTIVE_URL := $(shell grep PROACTIVE_URL .env | cut -d '=' -f2))
	$(eval PROACTIVE_USERNAME := $(shell grep PROACTIVE_USERNAME .env | cut -d '=' -f2))
	$(eval PROACTIVE_PASSWORD := $(shell grep PROACTIVE_PASSWORD .env | cut -d '=' -f2))
