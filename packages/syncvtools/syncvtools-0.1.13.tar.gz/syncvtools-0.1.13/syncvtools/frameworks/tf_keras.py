'''
TensorFlow Inference. Right now supports Object Detection API models only.
'''
from typing import Dict, List, Tuple, Any, Union
import numpy as np, cv2
from syncvtools.utils.image import img_rot90, img_flip, img_rotate
from syncvtools.utils._dependencies import dep
#from syncvtools.data import detections as det_mod
#from syncvtools.utils import file_tools as ft
#from syncvtools.utils.draw_detections import DrawDetections, imshow
from syncvtools.utils.bbox import restore_boxes, norm_y1x1y2x1_to_abs_x1y1x2y2, abs_x1y1x2y2_to_norm_y1x1y2x1
from syncvtools.utils.center_point import backward_rotation_bbox_tf
#from syncvtools.frameworks.tf_classifier import TFInferenceClassifier
from syncvtools.frameworks.tf import TensorflowInference
#from syncvtools import config
import logging
import operator

tf = dep('tf')

def compute_resize_scale(image_shape, min_side=800, max_side=1333):
    """ Compute an image scale such that the image size is constrained to min_side and max_side.

    Args
        min_side: The image's min side will be equal to min_side after resizing.
        max_side: If after resizing the image's max side is above max_side, resize until the max side is equal to max_side.

    Returns
        A resizing scale.
    """
    (rows, cols, _) = image_shape

    smallest_side = min(rows, cols)

    # rescale the image so the smallest side is min_side
    scale = min_side / smallest_side

    # check if the largest side is now greater than max_side, which can happen
    # when images have a large aspect ratio
    largest_side = max(rows, cols)
    if largest_side * scale > max_side:
        scale = max_side / largest_side

    return scale

def resize_image(img, min_side=800, max_side=1333):
    """ Resize an image such that the size is constrained to min_side and max_side.

    Args
        min_side: The image's min side will be equal to min_side after resizing.
        max_side: If after resizing the image's max side is above max_side, resize until the max side is equal to max_side.

    Returns
        A resized image.
    """
    # compute scale to resize the image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    scale = compute_resize_scale(img.shape, min_side=min_side, max_side=max_side)

    # resize the image with the computed scale
    img = cv2.resize(img, None, fx=scale, fy=scale)

    return img, scale

def preprocess_image(input_image: np.ndarray) -> Tuple[np.ndarray,float]:
    '''
    preprocessing script according to ObjectDetection API
    :param input_image: RGB image, preferably in uint8
    :return: np array which has binary of encoded PNG image
    '''
    # the input should be BGR
    #input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
    #ret, img_buf = cv2.imencode('.png', input_image)
    input_image = input_image.astype(np.float32)
    input_image, scale = resize_image(input_image, min_side=480, max_side=704)
    input_image -= [103.939, 116.779, 123.68]
    input_image = np.expand_dims(input_image, axis=0)
    # images_encoded = img_buf.tostring()
    return input_image, scale


class KerasInference(TensorflowInference):
    def _initialize_inference_graph(self, graph_src: str,
                                    read_func=lambda x: tf.gfile.GFile(x, 'rb').read(),
                                    input_tensor_name: str = 'input_1:0',
                                    output_tensor_names: tuple = ("filtered_detections/map/TensorArrayStack/TensorArrayGatherV3:0",
                                                                  "filtered_detections/map/TensorArrayStack_1/TensorArrayGatherV3:0",
                                                                  "filtered_detections/map/TensorArrayStack_2/TensorArrayGatherV3:0")
                                    ):
        '''
        Inits detection graph to memory.
        :param graph_src: path to PB graph (Frozen_inference_graph). Supports local path
        :param read_func: default tf.gfile.GFile(x, 'rb')
        :param input_tensor_name: name of input tensors in detection graph
        :param output_tensor_names: tuple with names of output tensors
        :return:
        '''
        # get a pointer to default graph
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            # make a serializable graph
            od_graph_def = tf.GraphDef()
            # graph can be written to string by any function (read_func param). Default is gfile.GFile
            serialized_graph = read_func(graph_src)
            # load from string to serializabl graph
            try:
                od_graph_def.ParseFromString(serialized_graph)
            except Exception:
                print("Graph is not frozen/readble: {}".format(graph_src))
            # import this text-graph to real default one (which is currently detection_graph)
            tf.import_graph_def(od_graph_def, name='')
            # create TF session
            self.session = tf.Session(graph=detection_graph)
            # get a pointer to input image from the graph
            try:
                self.input_tensor = detection_graph.get_tensor_by_name(input_tensor_name)
            except:
                print([n.name for n in tf.get_default_graph().as_graph_def().node])
                raise

            self.output_tensors = [detection_graph.get_tensor_by_name("%s" % t) for t in output_tensor_names]

    def _initialize_from_checkpoint(self, checkpoint_path,
                                    input_tensor_name='encoded_image_string_tensor:0',
                                    output_tensor_names=("detection_boxes",
                                                         "detection_scores",
                                                         "detection_classes",
                                                         "num_detections")
                                    ):
        raise NotImplemented

    def detect_image(self,
                     input_image: np.ndarray,
                     preprocess_func=preprocess_image,
                     rot90: int = None,
                     flip: int = None,
                     rotate: int = 0,
                     padding: int = 0,
                     ):
        return super().detect_image(
                     input_image,
                     preprocess_func,
                     rot90,
                     flip,
                     rotate,
                     padding)

    def detect_image_raw(self,
                         input_image: np.ndarray,
                         preprocess_func=preprocess_image,
                         rot90: int = None,
                         flip: int = None,
                         rotate: int = 0,
                         padding: int = 0,
                         ):
        '''
        All detections happens here. Returns dictionary with numpy arrays of TF Obj Det format.
        :param input_image: RGB image (numpy array)
        :param preprocess_func: should output an encoded BGR PNG in bytes
        :param rot90: 1,2,3 to return 90 degrees CCW.
        :param flip: 1,2,3 to flip horizontally, vertically, or both
        :param rotate: random rotation, instead of box center point of box will be returned
        :param padding: for inference white padding will be added.
        :return: dict of values. BOXES ARE IN ymin, xmin, ymax, xmax format
        '''
        if not self.graph_loaded:
            raise Exception(
                "Graph is not loaded! Run either constructor with graph_src param or initialize_inference_graph()")
        orig_size = input_image.shape[:2][::-1]
        if rotate:
            input_image = img_rotate(img_np=input_image, degree=rotate)
            rotated_size = input_image.shape[:2][::-1]

        if flip:
            input_image = img_flip(img_np=input_image, d=flip)

        if rot90:
            input_image = img_rot90(img_np=input_image, factor=rot90)

        if padding:
            input_image = cv2.copyMakeBorder(input_image, padding, padding, padding, padding,
                                             cv2.BORDER_CONSTANT, value=(255, 255, 255))

        images_encoded, scale = preprocess_func(input_image)
        boxes, scores, classes  = self.session.run(self.output_tensors,
                                                       feed_dict={self.input_tensor: images_encoded})
        boxes /= scale
        indices = np.where(scores[0, :] > 0.0)[0] #empty boxes get -1 score
        scores_filtered = scores[0][indices]
        scores_sort = np.argsort(-scores_filtered)

        #boxes_count = len(boxes[(np.amin(boxes,axis=-1)>-1.0)==True])
        boxes = boxes[:,scores_sort,:]
        scores = scores[:, scores_sort]
        classes = classes[:, indices[scores_sort]]

        classes += 1 #indices start from 1 in label map
        boxes = abs_x1y1x2y2_to_norm_y1x1y2x1(boxes, img_size=(input_image.shape[1],input_image.shape[0]))

        boxes, scores, classes, clsfr_src_scores = self.classifier_fusion(input_image, boxes, scores, classes)
        boxes, scores, classes, clsfr_src_scores = self.nms(boxes, scores, classes, clsfr_src_scores)

        if rot90 or flip or padding:
            logging.debug("Restoring boxes..")
            boxes = restore_boxes(boxes=boxes,
                                  rot90=rot90,
                                  flip=flip,
                                  org_size=orig_size,
                                  modified_img_size=input_image.shape[:2][::-1],
                                  padding=padding)

        if rotate:
            logging.debug("Restoring original center points from rotated boxes..")
            points = backward_rotation_bbox_tf(bbox_norm=boxes, angle=rotate, org_size=orig_size, rot_size=rotated_size)
            return {'points': points, 'scores': scores, 'classes': classes, 'img_inf_size': input_image.shape,
                    'clsfr_src_scores': clsfr_src_scores}

            # boxes - (batch, num, min_y, min_x, max_y, max_x)
        return {'boxes': boxes, 'scores': scores, 'classes': classes, 'img_inf_size': input_image.shape,
                'clsfr_src_scores': clsfr_src_scores}


if __name__ == '__main__':
    from syncvtools.utils.data_export import ProdDetectionsExport
    from syncvtools.utils.data_import import TFRecords
    from tqdm import tqdm
    import os


