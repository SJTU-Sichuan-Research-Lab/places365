FROM floydhub/dl-docker:cpu
MAINTAINER wyc

# copy script and models_places dir into working directory
COPY . /root/caffe

# fetch pretrained model prototxt and weights
WORKDIR /root/caffe
#RUN wget http://places2.csail.mit.edu/models_places365/alexnet_places365.caffemodel
#RUN wget https://raw.githubusercontent.com/metalbubble/places365/master/deploy_alexnet_places365.prototxt
#RUN mv alexnet_places365.caffemodel deploy_alexnet_places365.prototxt models_places
RUN pip install --upgrade certifi
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host pypi.io -r requirements.txt

# clean up
# RUN rm -rf matlab models js docker examples docs cmake data python src tools
RUN rm INSTALL.md Dockerfile Makefile Makefile.config.example CMakeLists.txt LICENSE CONTRIBUTORS.md README.md