#docker build . -t getaround-app --platform linux/amd64
docker run -it \
    -v "$(pwd):/home/app"\
    -e PORT=80 \
    -p 4001:80 \
    getaround-app