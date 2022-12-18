# Courses Catalog
A web application to share courses and exams made with Django.

## Installation
```
pip install pipenv
```
At the project's root (same directory as `manage.py`) run the following command:
```
pipenv install --dev
```
If you don't want to install dev packages you can omit the `--dev`

### Environment variables
- SECRET_KEY (str): The Django [secret key setting](https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key)
- DEBUG (True|False): Enable or disable django's [debug mode](https://docs.djangoproject.com/en/4.1/ref/settings/#debug)
- MAX_PDF_SIZE_MB (float): Maximum size (in MB) for Courses or Exams' pdf files 
