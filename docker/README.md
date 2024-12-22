## what is this?
a docker image containing:

* Ubuntu 14.04
* [Caffe](http://caffe.berkeleyvision.org/)
* [Numpy](http://www.numpy.org/), [SciPy](https://www.scipy.org/), [Pandas](http://pandas.pydata.org/), [Scikit Learn](http://scikit-learn.org/), [Matplotlib](http://matplotlib.org/)

## run

first, build container from docker image.

```
git clone https://github.com/metalbubble/places365
cd places365/docker
docker build -t places365_container .
```

then, from command line, do

```
docker run places365_container python run_scene.py images/mountains.jpg

```

## for batch testing
```bash
docker run -v "C:\Users\ycwei\Desktop\scene_recognition_test:/root/caffe/test" -v "C:\Users\ycwei\PycharmProjects\nas\places365\docker\run_scene.py:/root/caffe/test/run_scene.py" places365_container python test/run_scene.py images/mountains.jpg 
```