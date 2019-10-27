

# Heroku

```
heroku create
heroku rename trabase
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY="`< /dev/urandom tr -dc 'a-zA-Z0-9' | head -c16`"
heroku config:set FLASK_APP=trabase

git push heroku master

heroku open

heroku pg:psql 
```

# Add user

## Create hashed passwd

Use the python console

```    
from werkzeug.security import generate_password_hash
password='somepasswd'
generate_password_hash(password, method='sha256')
'sha256$8yn7UtoG$862d802f936b61dc7347b7ac60f5e2853b3ff5b717a970c0a1fb3305d8752bc5'
```    

```
heroku pg:psql 

INSERT INTO "user" (name, email,password, created_on)
VALUES ('Steffen Vinther Sørensen', 'svinther@gmail.com', 'sha256$....', now())
;
```