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

install:
	# Instala dependencias respetando el uv.lock
	uv sync

run:
	# Ejecución estándar
	uv run python -m src

run-debug:
	# Ejecuta usando el depurador estándar de Python (pdb)
	# (Si prefieres gestionar el debug dentro de tu código, cámbialo a: uv run python -m src --debug)
	uv run python -m pdb -m src

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
