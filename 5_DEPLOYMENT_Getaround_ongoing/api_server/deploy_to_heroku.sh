heroku login
heroku container:login
heroku create getaround-api-demo
docker build . -t getaround-api-demo --platform linux/amd64
docker tag getaround-api-demo registry.heroku.com/getaround-api-demo/web
docker push registry.heroku.com/getaround-api-demo/web
heroku container:release web -a getaround-api-demo