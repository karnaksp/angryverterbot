REQUIREMENTS_FILE = ./requirements.txt

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = ./source
BUILDDIR      = ./build
VENV_DIR      = myenv

.PHONY: all clean create_venv html Ex00 Ex01 install_req install_dep check_lint

all: cat clean

create_venv:
	@./cat.sh "Create virtual env..." 10
	@python3 -m venv $(VENV_DIR)
	@bash -c "source $(VENV_DIR)/bin/activate && \
	pip install -r $(REQUIREMENTS_FILE)"

start_bot:
	@./cat.sh "Start play game..." 10
	@bash -c "source $(VENV_DIR)/bin/activate && \
	python3 bot.py"

html:
	@bash -c "source $(VENV_DIR)/bin/activate && \
	$(VENV_DIR)/bin/$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS)"

cat:
	@chmod +x cat.sh

clean:
	@./cat.sh "Cleaning up..." 10
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name 'htmlcov' -exec rm -rf {} +
	@rm -rf */.coverage */*.log myenv
	@rm -rf $(BUILDDIR)/doctrees $(BUILDDIR)/html $(VENV_DIR)

run_in_docker:
	docker build -t game_bot .
	docker run --rm -it game_bot /bin/bash
