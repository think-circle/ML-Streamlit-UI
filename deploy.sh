#!/bin/bash
git init
heroku login
heroku create ai-thinkcircle
git add .
git commit -m "Automated commit"
git push heroku master
heroku ps:scale web=1