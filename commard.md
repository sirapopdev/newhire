```sh setup
# create venv
python -m venv venv

# activate venv
source venv/bin/activate

# install uv
pip install uv

# install dependencies
# remove "psycopg[c]==3.3.4" first if error and unremore if success
uv sync

# if window use wsl in vs code, install wsl extension first and go to right bottom and select wsl
```

```sh
# create app
just manage startapp dashboard

python ../manage.py startapp api

# generate sample data
just manage generate_sample_data --n 100

# run pytest
just pytest

# run pytest for specific folder
just pytest newhire/blog/tests

# run pytest for specific file
just pytest newhire/blog/tests/test_models.py

# run coverage
just pytest-cov

# run coverage for specific folder
just pytest-cov newhire/blog/tests

just isort
just isort newhire/users/models.py
just isort newhire/users tests

just flake8
just flake8 newhire/users/views.py

just lint
just lint newhire/users
just lint newhire/users tests/test_users.py
```