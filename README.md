# django-auth-backend

![CI](https://github.com/Sirneij/django-auth-backend/actions/workflows/django.yml/badge.svg) ![Test coverage](coverage.svg)

Django session-based authentication system with SvelteKit frontend and GitHub actions-based CI.

This app uses minimal dependencies (pure Django - no REST API framework) to build a secure, performant and reliable (with 100% automated test coverage, enforced static analysis using Python best uniform code standards) session-based authentication REST APIs which were then consumed by a SvelteKit-based frontend Application.

Users' profile images are uploaded directly to AWS S3 (in tests, we ditched S3 and used Django's [InMemoryStorage](https://docs.djangoproject.com/en/4.2/ref/files/storage/#django.core.files.storage.InMemoryStorage) for faster tests).

A custom password reset procedure was also incorporated, and Celery tasks did email sendings.

## Run locally

- To run the application, clone it:

    ```shell
    git clone https://github.com/Sirneij/django-auth-backend.git
    ```

    You can, if you want, grab its [frontend counterpart](https://github.com/Sirneij/rust-auth/tree/main/frontend).

- Change the directory into the folder and create a virtual environment using either Python 3.9, 3.10 or 3.11 (tested against the three versions). Then activate it:

    ```shell
    ~django-auth-backend$ virtualenv -p python3.11 virtualenv

    ~django-auth-backend$ source virtualenv/bin/activate 
    ```

- Install the dependencies, change the directory to `src` and run the code:

    ```shell
    ~(virtualenv) django-auth-backend$ pip install -r requirements_dev.txt

    ~(virtualenv) django-auth-backend$ cd src

    ~(virtualenv) django-auth-backend/src$ python manage.py runserver 8080
    ```

## Tests and static analysis

To run tests and static analysis, change the directory to the root folder and, using the bash scripts in the `scripts/` folder, run tests and static analysis:

```shell
~(virtualenv) django-auth-backend/src$ cd ..

~(virtualenv) django-auth-backend$ ./scripts/test.sh # runs test

~(virtualenv) django-auth-backend$ ./scripts/static_validation.sh # runs static analysis
```
