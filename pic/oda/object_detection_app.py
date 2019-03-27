import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
import sys

sys.path.insert(0, "/home/rajath/api1/yolo/pic/oda/utils")
sys.path.append("/home/rajath/api1/yolo/pic/")
from pic.oda  import utils

from .utils.app_utils import FPS, WebcamVideoStream, HLSVideoStream
from multiprocessing import Queue, Pool
from .object_detection.utils import label_map_util
from .object_detection.utils import visualization_utils as vis_util

CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = os.path.join('pic','oda', 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('pic','oda', 'object_detection', 'data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return image_np


def worker(input_q, output_q):
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)

    frame=cv2.imread(input_q)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    saved_image=detect_objects(frame_rgb,sess,detection_graph)
    cv2.imwrite(output_q,saved_image)
    sess.close()
    #output_q.put(detect_objects(frame_rgb, sess, detection_graph))
    #fps = FPS().start()
    #while True:
    #fps.update()
    #    frame = input_q.get()
#   frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #output_q.put(detect_objects(frame_rgb, sess, detection_graph))

    #fps.stop()

#logger = multiprocessing.log_to_stderr()
#logger.setLevel(multiprocessing.SUBDEBUG)

def decode(img_string):
    import base64
    image_64_decode = base64.decodestring(img_string)
    image_result = open('original_image.jpeg', 'wb')
    image_result.write(image_64_decode)
    image_result.close()



def run(img_string):
    decode(img_string)
    input_q = 'original_image.jpeg'
    output_q = 'captioned_image.jpeg' #pool = Pool(2, worker, (input_q, output_q))
    worker(input_q,output_q)
    print('Image captioning completed')
#video_capture = WebcamVideoStream(src=0,
#                                      width=480,
#                                      height=360).start()


#fps = FPS().start()
"""
while True:  # fps._numFrames < 120
    frame = video_capture.read()
    input_q.put(frame)
    t = time.time()
    output_rgb = cv2.cvtColor(output_q.get(), cv2.COLOR_RGB2BGR)
    cv2.imshow('Video', output_rgb)
    fps.update()

    print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
"""

#fps.stop()
#print('[INFO] elapsed time (total): {:.2f}'.format(fps.elapsed()))
#print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))
#pool.terminate()
#video_capture.stop()
#cv2.destroyAllWindows()
