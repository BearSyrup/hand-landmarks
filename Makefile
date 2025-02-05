.ONESHELL:
.DEFAULT_GOAL := run
.PHONHY: venv run clean 

APPNAME := src/app.py
ENVNAME := handenv

create: requirements.txt
		@echo "Creating environment..."
		mamba create -n ${ENVNAME}
		mamba activate ${ENVNAME}
		@echo "installing requirements..."
		conda install --file requirements.txt

venv:create
		@echo "activating the environment..."
		mamba activate ${ENVNAME}
run: 
		python ${APPNAME}


clean:
		@echo "Cleaning cache..."
		rm -rf __pycache__
		@echo "Cleaning environment..."
		mamba env remove -n ${ENVNAME}
