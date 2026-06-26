# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jpedra-v <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/08 11:12:48 by jpedra-v          #+#    #+#              #
#    Updated: 2026/06/11 15:10:14 by jpedra-v         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

.PHONY: install run run-debug clean fclean lint

# Variables de rutas del proyecto
FUNCTIONS_DEF = data/input/functions_definition.json
INPUT_FILE = data/input/function_calling_tests.json
OUTPUT_FILE = data/output/function_calls.json
MODEL_NAME = Qwen/Qwen3-0.6B

# Configuración de entornos para UV (Apuntando a sgoinfre)
export UV_CACHE_DIR = /sgoinfre/students/jpedra-v/uv_cache
export UV_PROJECT_ENVIRONMENT = /sgoinfre/students/jpedra-v/uv_envs/callme_venv
export HF_HOME = /sgoinfre/students/jpedra-v/hf_cache

install:
	# Instala dependencias respetando el uv.lock usando el entorno de sgoinfre
	uv sync

run:
	# Ejecución estándar con el modelo correcto y variables aplicadas
	uv run python -m src -f $(FUNCTIONS_DEF) -i $(INPUT_FILE) -o $(OUTPUT_FILE) -m $(MODEL_NAME)

run-debug:
	# Ejecuta usando el depurador estándar de Python (pdb)
	uv run python -m pdb -m src -f $(FUNCTIONS_DEF) -i $(INPUT_FILE) -o $(OUTPUT_FILE) -m $(MODEL_NAME)

clean:
	# Limpieza de caché local y archivos temporales de Python en tu repositorio
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache

lint:
	# Ejecución estricta de linters según normativa
	flake8 src
	mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
