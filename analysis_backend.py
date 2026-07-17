# Imports 
import json
import os
import base64

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS, IFD

from dotenv import load_dotenv
from openai import OpenAI

from pprint import pprint

import folium
from math import radians, cos, sin, asin, sqrt

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

# Clusting Logic
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * 6371 * asin(sqrt(a))  # km

def cluster_points(points, radius_km=0.5):
    """Groups nearby points into clusters and returns centroid + count for each."""
    clusters = []
    used = [False] * len(points)

    for i, p in enumerate(points):
        if used[i]:
            continue
        group = [p]
        used[i] = True
        for j, q in enumerate(points):
            if not used[j] and haversine(p["lat"], p["lon"], q["lat"], q["lon"]) <= radius_km:
                group.append(q)
                used[j] = True
        avg_lat = sum(pt["lat"] for pt in group) / len(group)
        avg_lon = sum(pt["lon"] for pt in group) / len(group)
        clusters.append({"lat": avg_lat, "lon": avg_lon, "count": len(group)})

    return clusters

def get_color(count):
        return "#ae2012"    # high — red

def get_raw_points(list_of_photos: dict):
    raw_points = []

    for photo_data in list_of_photos:
        if photo_data['severity'] == "high" or photo_data['severity'] == "critical":
            photo_dict = {'lat': photo_data['lat'], 'lon': photo_data['lng']}
            raw_points.append(photo_dict)


    return raw_points

def process_bubble_map(list_of_photos: dict) -> str:
    raw_points = get_raw_points(list_of_photos)
    clusters = cluster_points(raw_points, radius_km=0.5)
    location = [0,0]
    try:
        location = [raw_points[0]['lat'], raw_points[0]['lon']]
    except:
        pass

    if len(raw_points) == 0:
        return ""
    
    m = folium.Map(location=location, zoom_start=13)
    for c in clusters:
        radius = 5 + (c["count"] * 4)   # base size + growth per case
        folium.CircleMarker(
            location=[c["lat"], c["lon"]],
            radius=radius,
            color="#ae2012",
            fill=True,
            fill_color="#ae2012",
            fill_opacity=0.65,
            popup=f"High/Critical Cases: {c['count']}",
            width="100%",
        ).add_to(m)

    # Force filling the div container
    m.get_root().width = "100%"
    m.get_root().height = "100%"

    return m._repr_html_()


# Photo Metadata
def decode_exif_bytes(raw_comment) -> str:
    """Remove starting bytes for json string"""
    if not isinstance(raw_comment, bytes):
        return ""
        
    if raw_comment.startswith(b'ASCII\x00\x00\x00') or raw_comment.startswith(b'UNICODE\x00'):
        clean_bytes = raw_comment[8:]
    else:
        clean_bytes = raw_comment
        
    return clean_bytes.decode('utf-8', errors='ignore').strip()


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

        exif_ifd = exif.get_ifd(IFD.Exif)

        try:
            user_comment = exif_ifd.get(EXIF_USER_COMMENT_ID)

            user_comment = decode_exif_bytes(user_comment)
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

# OpenAI Prompt
def run_openai(filepath:str, metadata: dict, message: str) -> dict:

    with open(filepath, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        sensor_data = ""
        for param in VALID_SENSOR_DATA:
            param_value = metadata.get(param)
            if param_value is not None:
                sensor_data = sensor_data + f"{param}: {param_value}\n"

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
            # tools=[{
            #     "type": "file_search",
            #     "vector_store_ids": [os.getenv("OPENAI_VECTOR_STORE_ID")],
            #     "max_num_results": OPENAI_VECTOR_STORE_ITEMS 
            #     }],
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

# Statistics on Severity
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
