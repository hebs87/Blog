# Blog

A Django app that explores customisation of the Django admin panel.

## Running the project locally

To run the project locally, you will need to follow the below steps:

1. Create and activate a virtual environment
2. Install the requirements by running `pip install -r requirements.txt`
3. Create a `.env` file in the project directory with the following environment variables:

```
SECRET_KEY='your_secret_key_goes_here'
```

4. Run `python manage.py migrate` to run the database migrations
5. Run `python manage.py createsuperuser` and enter a username, email and password to create a superuser
7. Run `python manage.py runserver` to run the project
8. Finally, head over to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and login with the superuser credentials

## Creating test data

To create test data for each model, you will need to follow the below steps:

1. Open the Django shell by running `python manage.py shell`
2. In the Django shell, run the following code block

```
from seed.seed_data import generate_seed_data

generate_seed_data()
```
