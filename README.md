# xhs-download-web
小红书视频无水印解析下载，该项目可视为[XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader)的扩展插件。
**本项目仅实现web界面，核心功能仍由[XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader)提供。**
开发这个项目是因为本人觉得每次下载视频都要开电脑，比较麻烦，所以部署在云端，通过浏览器访问下载。

# 实现效果

1、主界面

![图片](https://github.com/user-attachments/assets/d2f71fc1-c271-4dbc-97cc-0439a6e4ba41)

2、解析界面

![图片](https://github.com/user-attachments/assets/7ea7c53d-0189-4642-ae9d-1ebca193e485)

3、解析完成界面

![图片](https://github.com/user-attachments/assets/94c43cd5-c3d7-4d36-961b-a6db2bc615ce)


# 运行方式
1、修改source/main.py中的`xhs_server = "http://127.0.0.1:8000/xhs/"`修改为自己的[XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader)地址。
以docker方式运行
```bash
./docker_run.sh
```

2、使用浏览器打开https://url:8888
![图片](https://github.com/user-attachments/assets/d2f71fc1-c271-4dbc-97cc-0439a6e4ba41)
