install:
	poetry install

lint:
	poetry run flake8 gendiff

build:
	poetry build

publish:
	poetry publish

package-install:
	python -m pip install --user dist/*.whl

check:
	pytest
