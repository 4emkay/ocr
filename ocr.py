# python3 obligatory !!!
from PIL import Image
import pytesseract
import pandas as pd
import cv2
from skimage import io
import logging
import datetime

import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class extract_data:
    def __init__(self, path):
        self.path = path

    def extract(self):
        img = io.imread(self.path)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        print(img)
        # convert the image to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(img)
        # the following command uses the tesseract directory path to get the trained data in the config option
        text = pytesseract.image_to_string(img, lang='eng')
        print(text)
        result = text.split("\n")
        data = pd.DataFrame(result, columns=['data'])
        assert isinstance(self.path, object)
        logging.warning('DATA EXTRACTION DONE WITH %s', self.path)
        self.result = data

    def preprocess(self):
        result = self.result[self.result['data'].str.contains('[A-Za-z0-9]', na=False)]
        result['data'] = result['data'].str.replace('\W', ' ')
        result = result.drop_duplicates()
        result.dropna(subset=["data"], inplace=True)
        result = result.reset_index(drop=True)
        logging.info('Extracted data  %s Pre-rocessed', result)
        self.result = result

    def get_name(self):
        try:
            source_index = self.result[self.result['data'].astype(str).str.match(r'^.*India$')].index[0]
            name = self.result[source_index + 2]
            return name
        except Exception as e:
            logging.error('Error at %s', 'NO NAME DETECTED')
            pass

    def get_adhaar(self):
        adhhar_number = self.result[self.result['data'].astype(str).str.match(r'^\d{4}\s\d{4}\s\d{4}$')].values[0]
        return adhhar_number[0]

    def get_dob(self):
        DOB = self.result[self.result['data'].astype(str).str.match(r'^.*DOB.*$')]
        dob = DOB['data'].str.replace(r'[^\d.]+', '').values[0]
        return dob

    def get_gender(self):
        try:
            if self.result[self.result['data'].astype(str).str.match(r'^.*Male')].values[0]:
                return 'MALE'
        except:
            if self.result[self.result['data'].astype(str).str.match(r'^.*FEMALE')].values[0]:
                return 'FEMALE'

    def get_father_name(self):
        try:
            father_name = self.result[self.result['data'].astype(str).str.match(r'^.*Father')].values[0]
            return father_name
        except:
            return None

