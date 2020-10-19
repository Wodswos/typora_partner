import json
import oss2
import os


def upload_img2oss(config):
    auth = oss2.Auth(config['oss']['accessKey']['ID'], config['oss']['accessKey']['Secret'])
    bucket = oss2.Bucket(auth, config['oss']['endpoint'], config['oss']['bucket'])
    upload_path = config['oss']['path']

    image_dir = config['imgPath']
    for img_name in os.listdir(image_dir):
        item = image_dir + '/' + img_name
        cloud_item = upload_path + '/' + img_name
        bucket.put_object_from_file(cloud_item, item)
        print(item + " has been uploaded to cloud successfully.")


with open('../config.json') as f:
    config = json.load(f)

if "imgPath" in config and "oss" in config:
    print("Upload processing may take a long time, please be patient....")
    upload_img2oss(config)
    print("Completed uploading successfully!")
else:
    print("No imgPath or oss Configuration in config file")