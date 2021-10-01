# Vending machine API

Test vending machine Rest APIs.

`.env` file is visible because of easier testing of the project

Installation without Docker
Vending Machine API requires:

- [Python 3.8.2](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)

When you meet specified requirements, it's necessary to manually create two postgres databases named vending_machine_amir and vending_machine_amir_test.

After database creation, modify .env file to make sure your database credentials are correct.

Installation on MacOS/Linux
Navigate to the project root and type in your preferred terminal:

```
$ make all
```
This command will install the required dependencies, run migrations and flask application

Verify the installation by navigating to link below in your preferred browser.

```http://127.0.0.1:5000/```

Installation on Windows
Navigate to the project root and type in your preferred terminal:

```
> py -3 -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> flask db init
> flask db migrate -m 'Initial migration'
> flask db upgrade
> flask run
```

# Testing

## Testing on MacOS/Linux
To run tests navigate to the project root and type in your preferred terminal:

```
$ make coverage
```
## Testing on Windows
To run tests navigate to the project root and type in your preferred terminal:

```
> venv\Scripts\activate
> coverage run -m pytest
> coverage report
```
