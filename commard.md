```sh
# create app
just manage startapp dashboard

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
```