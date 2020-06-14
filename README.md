0. `pipenv` is used as the virtual environment of choice for this application and you cna install it using `pip install pipenv`
1. You can install the proper virtual environment with `pipenv install`. As long as the pipenv.lock file is located within the root directory, you will also be able to install all of the necessary packages.
1. To initialize the app with data, run `npm run init`
1. To start the server: `npm run server` or `pipenv run python app.py`
2. The server is started and you can navigate to 127.0.0.1:7999

## Database Migrations

* Run `npm run db-migrate` to create a new migration script whenever changing the database models
* Run `npm run db-upgrate` to upgrade the Posgresql database that you're connecting to
