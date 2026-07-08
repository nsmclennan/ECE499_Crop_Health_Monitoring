# Imports 
import json
import os
import base64

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from dotenv import load_dotenv
from openai import OpenAI

from pprint import pprint

# Constants
EXIF_GPS_ID = 34853
EXIF_USER_COMMENT_ID = 37510

VALID_SENSOR_DATA = ['humidity', 'temperature', 'pressure']
VALID_PARAM_LEVELS = {
    'severity': ['low', 'medium', 'high', 'critical', 'uncertain'],
}


# API Configuration
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_API_MODEL = "gpt-5.4-mini"
OPENAI_VECTOR_STORE_ITEMS = 2


def get_photo_metadata(filepath: str) -> list[float]:
    """
    Obtain all metadata injected into image from hardware team. 
    Hardware sensor data is optional as may not be available depending on applicaiton
    """
    user_comment = None
    user_metadata = {}

    with Image.open(filepath) as img:
        exif = img.getexif()
        gps_info = exif.get_ifd(EXIF_GPS_ID)
        # Optional metadata.
        try: user_comment = exif.get_ifd(EXIF_USER_COMMENT_ID)
        except: pass

    if not gps_info or 2 not in gps_info or 4 not in gps_info:
        user_metadata["lat"] = 0
        user_metadata["lng"] = 0
        return user_metadata

    def dms_to_decimal(dms, ref):
        d, m, s = dms
        decimal = d + (m / 60.0) + (s / 3600.0)
        return -decimal if ref in ['S', 'W'] else decimal

    if user_comment is not None and user_comment:
        user_metadata = json.loads(user_comment)

    user_metadata["lat"] = dms_to_decimal(gps_info[2], gps_info.get(1, 'N'))
    user_metadata["lng"] = dms_to_decimal(gps_info[4], gps_info.get(3, 'E'))

    return user_metadata




def run_openai(filepath:str, metadata: dict, message: str) -> dict:

    with open(filepath, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        sensor_data = ""
        for param in VALID_SENSOR_DATA:
            param_value = metadata.get(param)
            if param_value is not None:
                sensor_data = sensor_data + f"{param}: {paramvalue}\n"

        if sensor_data:
            sensor_data = f"\n\nAlso use additional sensor data:\n" + sensor_data
        mildew_prompt_with_hardware = message + sensor_data

        response = client.responses.create(
            model=OPENAI_API_MODEL,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": mildew_prompt_with_hardware},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_b64}"
                    }
                ]
            }],
            tools=[{
                "type": "file_search",
                "vector_store_ids": [os.getenv("OPENAI_VECTOR_STORE_ID")],
                "max_num_results": OPENAI_VECTOR_STORE_ITEMS 
                }],
            store=True,
        )
        
        # Please see prompt_path for details on openai API output format.
        return json.loads(response.output_text)


def run(photos: list, message: str, results_folder: str) -> list:
    """
    Entry point called by app.py /api/analyze.
    Replace the stub body below with your real analysis logic.
    """
    results = []

    for photo in photos:
        metadata = get_photo_metadata(photo["filepath"])
        openai_response = run_openai(photo["filepath"], metadata, message)
        result = {
            "id":            photo["id"],
            "photo_id":      photo["id"],
            "original_name": photo["original_name"],
            "photo_url":     photo["url"],
            "location":      {"lat": metadata["lat"], "lng": metadata["lng"]},
            "notes":         (
                f"Analysis message: {message}\n",
                f"Confidence: {openai_response['confidence']}\n" 
            ),
        }

        result.update(metadata)
        result.update(openai_response)

        # Write per-photo JSON to results folder
        json_filename = f"{photo['id']}_result.json"
        json_path = os.path.join(results_folder, json_filename)
        with open(json_path, "w") as fh:
            json.dump(result, fh, indent=2)

        result["json_path"] = json_path
        results.append(result)

    return results




def count_param(statistics_dict: dict, photo_dict: dict, param: str) -> None:
    if param not in statistics_dict:
        statistics_dict[param] = {}
    param_value = photo_dict.get(param)

    if param_value:
        if param_value not in statistics_dict[param]:
            statistics_dict[param][param_value] = {}
            statistics_dict[param][param_value]['count'] = 0
        statistics_dict[param][param_value]['count'] += 1

def pull_statistics(list_of_photos: list[dict]) -> dict:
    """ Obtain statistics based on image."""
    statistics_dict = {}

    for photo_data in list_of_photos:
            count_param(statistics_dict, photo_data, "severity")
    
    for severity_level in VALID_PARAM_LEVELS['severity']:
        if 'severity' not in statistics_dict:
            statistics_dict['severity'] = {}

        if severity_level not in statistics_dict['severity']:
            statistics_dict['severity'][severity_level] = {}
            statistics_dict['severity'][severity_level]['count'] = 0
        
        total_items = len(list_of_photos)
        percent = 0 if total_items == 0 else round((statistics_dict['severity'][severity_level]['count']/ total_items) * 100, 1)
        statistics_dict['severity'][severity_level]['percent'] = percent
    return statistics_dict
