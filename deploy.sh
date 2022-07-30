%%bash
git add .
git commit -m "Automated commit"
git push heroku master
heroku ps:scale web=1