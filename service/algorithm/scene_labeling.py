import time
import os
import glob
import fnmatch
import urllib2
import json


import numpy as np
import sys
import caffe
import cv2

net = None
transformer = None
labels = None
# fetch pretrained models
fpath_design = 'models_places/deploy_alexnet_places365.prototxt'
fpath_weights = 'models_places/alexnet_places365.caffemodel'
# fpath_labels = 'resources/labels.pkl'
# fpath_labels = 'resources/labels2.txt'
fpath_labels = 'resources/labels_with_chinese.txt'

def load_model():
    # initialize net
    global net, transformer

    if net is None:
        net = caffe.Net(fpath_design, fpath_weights, caffe.TEST)

        # load input and configure preprocessing
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        transformer.set_mean('data', np.load('python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(
            1))  # TODO - remove hardcoded path
        transformer.set_transpose('data', (2, 0, 1))
        transformer.set_channel_swap('data', (2, 1, 0))
        transformer.set_raw_scale('data', 255.0)

        # since we classify only one image, we change batch size from 10 to 1
        net.blobs['data'].reshape(1, 3, 227, 227)


def read_labels():
    global labels
    if labels is None:
        with open(fpath_labels, 'r') as f:
            labels = f.readlines()


def classify_scene(im):
    global net, transformer, labels
    load_model()
    read_labels()


    t0 = time.time()
    # print "start: " + str(t0)

    # load the image in the data layer
    net.blobs['data'].data[...] = transformer.preprocess('data', im)

    # compute
    out = net.forward()

    t1 = time.time()
    # print "end: " + str(t1)
    # print "cost: " + str(t1 - t0) + " seconds"

    # print top 5 predictions - TODO return as bytearray?
    # with open(fpath_labels, 'rb') as f:
    #
    # 	labels = pickle.load(f)
    # 	top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
    #
    # 	for i, k in enumerate(top_k):
    # 		print i, labels[k]

    probs = net.blobs['prob'].data[0].flatten()
    top_k = probs.argsort()[-1:-6:-1] # k = 5, take top 5
    top_k_props = probs[top_k]
    # print(top_k, top_k_props)

    top_k_result_lst = []
    for i, k in enumerate(top_k):
        # print i, labels[k], probs[k]
        top_k_result_lst.append({
            "idx": i,
            "class_idx": k,
            "label": labels[k].strip(),
            "confidence": float(probs[k])
        })
    return top_k_result_lst, t1 - t0


def find_jpg_files(directory):
    jpg_files = []

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, '*.jpg'):
                # If the file is a jpg, add it to the list
                jpg_files.append(os.path.join(root, file))

    return jpg_files


'''
perform scene recognition on a single image file which has been store in the disk
'''
def serve(img_pth):

    # fetch image
    # todo use the image buffer directly
    if img_pth.endswith(".bmp"):
        im = cv2.imread(img_pth)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = im.astype(float) / 255.0
    else:
        im = caffe.io.load_image(img_pth)

    # predict
    return classify_scene(im)


def main():
    ########################## test data ###############################################################################
    test_dir = 'data/test'
    test_img_lst = []
    ## use other data
    # test_data_dir = test_dir + '/data' # fixme
    # pattern = os.path.join(test_data_dir, '**.jpg')
    # test_img_lst = glob.glob(pattern)

    # use changhong test data
    test_changhong = test_dir + '/changhong_data'  # fixme
    test_img_lst = find_jpg_files(test_changhong)

    print "received " + str(len(test_img_lst)) + " images"
    ####################################################################################################################

    cnt = 0
    output = []
    for img_pth in test_img_lst:
        print cnt, "/", len(test_img_lst)
        cnt += 1

        img = caffe.io.load_image(img_pth)
        result, cost_time = classify_scene(img)
        res_line = img_pth + "\n"
        for scene in result:
            res_line += str(scene['idx']) + " " + str(scene['label']) + " " + str(scene['confidence']) + "\n"
        res_line += "cost time: " + str(cost_time) + "s"
        output.append(res_line)
    with open(test_dir + "/test_result_" + str(time.time()) + ".txt", 'w') as f:
        for line in output:
            f.write(str(line))
            f.write("\n")
            f.write("\n")

    print "v1"

if __name__ == '__main__':
    # main()
    print(serve("data/test/changhong_data/ia_100000000.jpg"))