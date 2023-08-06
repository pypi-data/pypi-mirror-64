'''
Direct conversion scripts which are too complicated to do through our classes.
Most of conversions are done through data_import and data_export
'''

from typing import List, Dict, Any, Callable
import logging, os
import csv
from tqdm import tqdm
import syncvtools.utils.file_tools as ft
from syncvtools.utils.data_export import COCOExport, CSVExport
from syncvtools.utils.data_import import TFRecords
from syncvtools.utils._dependencies import dep


def tfrecord_to_coco(tfrecord_src, out_json_path, out_img_path, label_map=None):
    '''
    Takes TF Record and converts it to MSCOCO format for BBOX detection without loading TF record to memory.
    :param tfrecord_file: input tf record
    :param annotation_file: output JSON file for MSCOCO annotations
    :param out_img_path: output directory to store images extracted from TF record
    :return:
    '''

    label_map_direct = ft.pbmap_read_to_dict(label_map)
    label_map_inverse = {v: k for k, v in label_map_direct.items()}

    # LOADING ITERATIVELY TF RECORD. We can't just read the whole thing to memory using data_import.
    # tf = dep('tf')
    # tf_obj_det_decoder = dep('tf_obj_det_decoder')
    # raw_dataset = tf.data.TFRecordDataset([tfrecord_src])
    # decoder = tf_obj_det_decoder()

    output, counters = COCOExport.generate_coco_header()
    coco_images = []
    coco_annotations = []
    counter_written = 0
    for img_key, imgdet_obj in tqdm(TFRecords.to_det_col_iter(tfrecord_src=tfrecord_src)):
        # img_key, imgdet_obj = TFRecords.record_to_object(decoder=decoder, tf_one_record=raw_record)
        imgdet_obj.process_labelmap(label_map=label_map_direct,
                                    inverse_label_map=label_map_inverse)

        coco_image, coco_annotation = COCOExport.convert_one(img_det=imgdet_obj, counters=counters)
        coco_images.append(coco_image)
        coco_annotations += coco_annotation
        assert imgdet_obj.img.img_filename
        ft.img_np_to_disk(img_np=imgdet_obj.img.img_np,
                          save_path=os.path.join(out_img_path, imgdet_obj.img.img_filename))
        counter_written += 1

    categories_list = []
    categories_set = set()
    for coco_annotation in coco_annotations:
        if coco_annotation['category_id'] in categories_set:
            continue
        categories_set.add(coco_annotation['category_id'])
        categories_list.append({'supercategory': "threat",
                                'id': coco_annotation['category_id'],
                                'name': coco_annotation['category_txt']}
                               )
    output['categories'] = categories_list
    output['annotations'] = coco_annotations
    output['images'] = coco_images
    logging.info("Dumping annotations to file {}".format(out_json_path))
    ft.json_object_to_file(path_src=out_json_path, data_obj=output)
    logging.info("Done. {} written".format(counter_written))


def tfrecord_to_csv(tfrecord_src, out_name, label_map=None) -> None:
    '''
    Takes TF Record and converts it to CSV format (i.e. keras retinanet)
    :param tfrecord_file: input tf record
    :param  out_name: should be dir+name (no ext), i..e /tmp/hs-threats: stores [name].csv and [name]/images_here
    :return:
    '''
    label_map = ft.cache_file(label_map)
    label_map_direct = ft.pbmap_read_to_dict(label_map)
    label_map_inverse = {v: k for k, v in label_map_direct.items()}
    counter_written = 0
    img_dir_name =os.path.basename(out_name)
    out_dir = os.path.dirname(out_name)
    os.makedirs(out_dir,exist_ok=True)
    with open(os.path.join(out_dir,"class_map.class"), 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for label in label_map_direct:
            csv_writer.writerow([label_map_direct[label],label-1])


    with open("{}.csv".format(out_name), 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for img_key, imgdet_obj in tqdm(TFRecords.to_det_col_iter(tfrecord_src=tfrecord_src)):
            csv_rows, img_path = CSVExport.convert_one(imgdet_obj,img_key= img_key, img_dir=img_dir_name)
            ft.img_np_to_disk(img_np=imgdet_obj.img.img_np,
                              save_path=os.path.join(out_dir, img_path))
            for csv_row in csv_rows:
                csv_writer.writerow(csv_row)
                counter_written += 1
    logging.info("Done. Boxes {} written".format(counter_written))