init: compile
	@echo "Creating a new virtual environment"
	python3 -m venv venv
	python3 setup.py install
	. venv/bin/activate; pip install -r requirements.txt

# Компиляция C-расширения
compile:
	@echo "Compiling C extension"
	gcc -shared -fPIC cjson.c -o cjson.so -lpython3.10


# Запуск юнит-тестов
test: install
	@echo "Running tests"
	. venv/bin/activate; python3 -m unittest discover -s test.py

# Задача по умолчанию - инициализация виртуального окружения
.DEFAULT_GOAL := init