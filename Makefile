# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jpedra-v <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/08 11:12:48 by jpedra-v          #+#    #+#              #
#    Updated: 2026/06/08 11:12:50 by jpedra-v         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

.PHONY: install run run-debug clean lint

# Variables por defecto para que 'make run' funcione directamente
FUNCTIONS_DEF = data/input/functions_definition.json
INPUT_FILE = data/input/function_calling_tests.json
OUTPUT_FILE = data/output/function_calls.json

install:
	# Instala dependencias respetando el uv.lock
	uv sync

run:
	# Ejecución estándar con los argumentos obligatorios
	uv run python -m src -f $(FUNCTIONS_DEF) -i $(INPUT_FILE) -o $(OUTPUT_FILE)

run-debug:
	# Ejecuta usando el depurador estándar de Python (pdb) con los argumentos obligatorios
	uv run python -m pdb -m src -f $(FUNCTIONS_DEF) -i $(INPUT_FILE) -o $(OUTPUT_FILE)

clean:
	# Limpieza de caché y archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache
	rm -rf .venv

lint:
	# Ejecución estricta de linters según normativa
	flake8 src
	mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
