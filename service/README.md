## Development
#### download the model to service/models_places

http://places2.csail.mit.edu/models_places365/alexnet_places365.caffemodel

#### create file in service/models_places 
```bash
cd models_places
touch deploy_alexnet_places365.prototxt
```

#### docker build
```bash
docker build -t scene_labeling:v2 .
```

#### docker run
```bash
docker rm -f scene
docker run -v "C:\Users\ycwei\PycharmProjects\nas\places365\service\data:/root/caffe/data" -p 8888:8888 --name scene scene_labeling python app.py  
```

#### docker run in background
```bash
docker rm -f scene
docker run -d -v "C:\Users\ycwei\PycharmProjects\nas\places365\service\data:/root/caffe/data" -p 8888:8888 -e API_BASE="172.20.1.240:8888" --name scene scene_labeling python app.py 
```


#### docker remove unnecessary containers
```bash
docker rm -f $(docker ps -a -q)
```

#### debug or dev
```bash
docker run -v "C:\Users\ycwei\PycharmProjects\nas\places365\service\data:/root/caffe/data" -v "C:\Users\ycwei\PycharmProjects\nas\places365\service:/root/caffe/service" -p 8888:8888 scene_labeling:v2 python service/app.py
```


### Deployment
```bash
docker run --restart always -itd -v "C:\Users\ycwei\PycharmProjects\nas\places365\service\data:/root/caffe/data" -p 8888:8888 -e API_BASE="localhost:8888" --name scene scene_labeling:v2
```
Modify the -v, -p and -e options to achieve your custom deployment.
(API_BASE is just for local demonstration, as we now have an all-in-one frontend, it doesn't matter anymore.)


if necessary
```bash
docker rm -f scene
```