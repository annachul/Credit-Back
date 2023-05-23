# Credit-Back
Backend for an app for tracking expenses, loading bills automatically from bank statement csv files and displaying it in form of pie charts. (Django+PostgreSQL+pandas)

How to run
```
git clone https://github.com/annachul/Credit-Back
cd Credit-Back
```

Create virtual environment (optional)

```
python3 -m venv dtb_venv
source dtb_venv/bin/activate
```

Install all requirements:

```
pip install -r requirements.txt
```

Run migrations to setup PostgreSQL database:

```
python manage.py migrate
```


Start app
```
./manage.py runserver
```
