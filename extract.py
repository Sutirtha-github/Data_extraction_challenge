# Your imports go here
import os
import logging
import json
import re
import numpy as np

logger = logging.getLogger(__name__)

'''
    Given a directory with receipt file and OCR output, this function should extract the amount

    Parameters:
    dirpath (str): directory path containing receipt and ocr output

    Returns:
    float: returns the extracted amount

'''
def extract_amount(dirpath: str) -> float:

    logger.info('extract_amount called for dir %s', dirpath)
    # your logic goes here
    ocr_filepath = os.path.join(dirpath, 'ocr.json')
    with open(ocr_filepath, mode='r', encoding="utf-8") as f:
        data = json.load(f)
    s=[]
    for key, values in data.items():
        if key=='Blocks':
            for dictionary in values:
                for subkey, subvalue in dictionary.items():
                    if subkey=="Text":
                        s.append(subvalue)
    a = [w for w in s if re.search(r'^\$[0-9]+\.[0-9]+[0-9]$',w)]
    b = [w for w in s if re.search(r'^[0-9]+\.[0-9]+[0-9]$',w)] 
    e = [w for w in s if re.search(r'^\$[\d,]+\.\d+$',w)]
    f = []
    c = []
    d = []
    for w in a:
        c.append(float(w[1:]))
    for w in b:
        d.append(float(w))
    for w in e:
        str=""
        for ch in w:
            if ch not in ('$',','):
                str+=ch
        f.append(float(str))
    #Change1
    amount = 0
    if len(c)==0 and len(d)!=0:
        amount=np.max(d)
    elif len(d)==0 and len(c)!=0:
        amount=np.max(c)
    elif len(c)==0 and len(d)==0:
        amount = np.max(f)
    else:
        amount=np.max(np.max(d),np.max(c))
           
    return amount
