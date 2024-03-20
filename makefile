# Directory where the file will be saved
SAVE_DIR = data

setup:
	@echo "Setting up the environment..."
	
		pipreqs ./scripts && \
		pipenv install -r scripts/requirements.txt

.PHONY: setup
# Target to download and save the file
download:
	@mkdir -p $(SAVE_DIR)
	pipenv run python ./scripts/file_downloader.py $(SAVE_DIR)

.PHONY: download
