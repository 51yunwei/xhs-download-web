FROM python:3.12-slim

WORKDIR /app

LABEL name="Video-Downloader" authors="51yunwei" repository="https://github.com/51yunwei/"

COPY source /app

#RUN pip install -i https://pypi.doubanio.com/simple/ --no-cache-dir -r /app/requirements.txt

VOLUME /app

EXPOSE 8888

CMD ["python", "main.py"]
