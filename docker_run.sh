docker rm -f video
docker rmi video:v1
docker build -t video:v1 .
docker run -itd --name video  --restart=always video:v1 python main.py
docker logs -f video
