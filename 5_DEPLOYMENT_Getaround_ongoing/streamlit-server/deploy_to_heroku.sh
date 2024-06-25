heroku login
heroku container:login
heroku create getaround-analytics
docker build . -t getaround-analytics --platform linux/amd64
docker tag getaround-analytics registry.heroku.com/getaround-analytics/web
docker push registry.heroku.com/getaround-analytics/web
heroku container:release web -a getaround-analytics