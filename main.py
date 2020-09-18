# python3 obligatory !!!
from PIL import Image
import pytesseract
import pandas as pd
import cv2
from skimage import io
import logging
import datetime
from ocr import extract_data

import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
def main(path):
    time_start = datetime.datetime.now()
    print(time_start)
    logging.warning('Excution Started %s ', time_start)
    extraction = extract_data(path)
    extraction.extract()
    extraction.preprocess()
    name = extraction.get_name()
    adhaar_number = extraction.get_adhaar()
    dob = extraction.get_dob()
    father_name = extraction.get_father_name()
    gender = extraction.get_gender()
    time_end = datetime.datetime.now() - time_start
    logging.warning('Excution Ended took %s ', time_end)
    return {"name": name,
            "dob": dob,
            "adhaar_number": adhaar_number,
            "father_name": father_name,
            "gender": gender}

main('/path/to/image')
