# lkk-website

## Develop

### Setup Env

Add .env file to project root with following variables
```
SOCIAL_AUTH_FACEBOOK_KEY=<App ID from Facebook app thiamsu-development>
SOCIAL_AUTH_FACEBOOK_SECRET=<App Secret from Facebook app thiamsu-development>
```

### Run server
```
python manage.py runserver
```

### Other commands
Update locale file
```
python manage.py makemessages --add-location file
```

## Deploy

### Staging (Heroku)
```
heroku login
heroku git:remote -a lkk-website-staging
git push heroku <local_branch>:master
heroku run python manage.py compilemessages
```

### Heroku Notes
* other useful commands
```
heroku ps
heroku ps:scale web=1
heroku logs --tail
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```
