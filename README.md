# Email Send Template (Using Python)

### Environment variable settings

```
1. copy `.env.example` to `.env`
2. Replace the credentials of `.env` file with your email credentials
```

### Google app password generate

```
Here we are using google app password for the email password.
You can create your own google app password from your account.
Note, you must have to 2FA on.
```

### Virtual environment & dependencies

#### Create virtualenv

```
python -m venv venv
```

#### Install dependencies

```
pip install -r requirements.txt
```

### Run the app

Update the receiver email address, subject, and body and you are good to go.
<br>
Here we go!!!

```
python app.py
```
