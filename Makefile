.PHONY: clean setup setup_venv virtualenv build clean_build uninstall install test publish_test publish_prod print_version help get_env

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

uninstall:
	@echo "Uninstalling proactive package..."
	@. env/bin/activate && $(PYTHON) -m pip uninstall -y proactive
	@echo "Proactive package uninstalled."

install: uninstall
	@echo "Installing proactive from dist..."
	@. env/bin/activate && $(PYTHON) -m pip install dist/proactive*.zip
	@echo "Proactive installed."

test: get_env
	@echo "Running tests..."
	@. env/bin/activate && $(PYTHON) -m pytest --metadata proactive_url $(PROACTIVE_URL) --metadata username $(PROACTIVE_USERNAME) --metadata password $(PROACTIVE_PASSWORD) --junit-xml=build/reports/TEST-report.xml
	@echo "Tests completed."

test_using_secrets:
	@echo "Running tests using GitHub Secrets..."
	@. env/bin/activate && $(PYTHON) -m pytest --metadata proactive_url $(GITHUB_PROACTIVE_URL) --metadata username $(GITHUB_PROACTIVE_USERNAME) --metadata password $(GITHUB_PROACTIVE_PASSWORD) --junit-xml=build/reports/TEST-report.xml
	@echo "Tests completed using GitHub Secrets."

publish_test:
	@echo "Publishing to TestPyPI..."
	@. env/bin/activate && twine upload --repository-url https://test.pypi.org/legacy/ dist/* --config-file .pypirc
	@echo "Publishing completed."

publish_test_using_secrets:
	@echo "Publishing to TestPyPI..."
	@. env/bin/activate && twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	@echo "Publishing completed."

publish_prod:
	@echo "Publishing to PyPI..."
	@. env/bin/activate && twine upload dist/* --config-file .pypirc
	@echo "Publishing completed."

publish_prod_using_secrets:
	@echo "Publishing to PyPI..."
	@. env/bin/activate && twine upload dist/*
	@echo "Publishing completed."

print_version:
	@. env/bin/activate && $(PYTHON) -m pip show proactive
	@. env/bin/activate && $(PYTHON) -c "import proactive; print(proactive.__version__)"

help:
	@cat Makefile

get_env:
	$(eval PROACTIVE_URL := $(shell grep PROACTIVE_URL .env | cut -d '=' -f2))
	$(eval PROACTIVE_USERNAME := $(shell grep PROACTIVE_USERNAME .env | cut -d '=' -f2))
	$(eval PROACTIVE_PASSWORD := $(shell grep PROACTIVE_PASSWORD .env | cut -d '=' -f2))
