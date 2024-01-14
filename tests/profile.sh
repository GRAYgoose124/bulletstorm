#!/bin/bash

# pip install poetry snakeviz
# poetry install
poetry run python -m cProfile -o program.prof bulletstorm/__main__.py

snakeviz program.prof

