from typing import List
import logging
from roboflow import Roboflow
from src.utils.constant import google_api_key 
import requests
import os
import sys
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt



async def get_image_from_url(url, image_name, data_folder):
    response = requests.get(url)
    if response.status_code == 200:
        with open( os.path.join(data_folder, image_name), "wb") as file:
            file.write(response.content)
        print(f"✅ Satellite image '{image_name}' saved successfully! ✅")
    else:
        print(" ❌ Error:", response.text)
    
    return os.path.join(data_folder, image_name)


async def save_detection_image(image_path: str, test_image: str, prediction, data_folder: str) -> str:
    """
    Save the detection results as an image with bounding boxes.

    Args:
        image_path (str): The path to the original image.
        detections (List[dict]): The detection results containing bounding box coordinates.
        output_folder (str): The folder where the output image will be saved.

    Returns:
        str: The path to the saved image with detections.
    """

    # Load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    preds = prediction.get('predictions', [])
    if preds:
        # Draw predictions
        for pred in preds:
            x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
            class_name = pred['class']
            conf = pred['confidence']
            # Calculate box coordinates
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)
            # Draw rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
            # Put label
            label = f"{class_name} confidence: {conf:.2f}"
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    else:
        # Put "no archae_sites detected" in the center of the image
        h, w, _ = img.shape
        text = "no archae_sites detected"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_x = (w - text_size[0]) // 2
        text_y = (h + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 0), thickness, cv2.LINE_AA)
    # Save the image with detections
    cv2.imwrite(os.path.join(data_folder, f"{test_image}_prediction.png"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    print(f"✅ Detection image saved as {test_image}_prediction.png in {data_folder} ✅")




async def get_satellite_images(lat: float, long: float) -> List[dict]:
    """
    Get satellite images covering the area based on the provided location.

    Args:
        location (str): The location to search for satellite images.
        width_km (int): The width of the area in kilometers.
        length_km (int): The length of the area in kilometers.

    Returns:
        List[dict]: A list of satellite images with their URLs and coordinates.
    """

    # get api keys
    ee_API_KEY = google_api_key

    # create a test dataset folder to store the images
    data_folder = f"{os.getcwd()}/Robo_Predict_dataset"


    index_file = os.path.join(data_folder, "index.txt")
    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            index = int(f.read().strip())
    else:
        index = 0
        
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created directory: {data_folder}")

    # get the  latitude and longitude of the location
    test = {}

    if not lat or not long:
        print("  ❌  Invalid input. Please enter both latitude and longitude.")
        sys.exit(1)
    try:
        lat = float(lat)
        long = float(long)
        if not (-90 <= lat <= 90) or not (-180 <= long <= 180):
            print("  ❌  Invalid latitude or longitude. Latitude must be between -90 and 90, and longitude must be between -180 and 180.")
            sys.exit(1) 
    except ValueError:
        print("  ❌  Invalid input. Please enter valid numbers for latitude and longitude.")
        sys.exit(1)

    test={'lat': lat, 'long': long}
    test_image = f"Image_{index}"

    # define the image related parameter before getting images
    zoom = 16
    size = "640x640"
    test['index'] = index
    test['url'] = f"https://maps.googleapis.com/maps/api/staticmap?center={test['lat']},{test['long']}&zoom={zoom}&size={size}&maptype=satellite&key={ee_API_KEY}"

    print(f"  ✅  Fetching satellite image for location: {test['lat']}, {test['long']}...")

    img_path = await get_image_from_url(test['url'], f"{test_image}.png", data_folder)

    return img_path, test_image, data_folder


    # This is a placeholder implementation. Replace with actual logic to fetch satellite images.
    return [
        {
            "image_url": f"https://example.com/satellite_image_{location}.jpg",
            "coordinates": f"Coordinates for {location} with width {width_km}km and length {length_km}km"
        }
    ]

async def detect_sites_in_image(image_path: str) -> List[dict]:
    """
    Detect potential archaeological sites in the provided satellite image.

    Args:
        image_url (str): The URL of the satellite image to analyze.

    Returns:
        List[dict]: A list of detected archaeological sites with their coordinates.
    """

    model = YOLO("src/model/weights.pt") 

    prediction = model.predict(image_path).json()
    print(prediction)

    return prediction

    # return [
    #     {
    #         "site": "Site A",
    #         "coordinates": "(12.34, 56.78)"
    #     },
    #     {
    #         "site": "Site B",
    #         "coordinates": "(23.45, 67.89)"
    #     }
    # ]


async def get_archaeological_sites_candidates(lat:float, long:float) -> List[dict]:
    """
    Get a list of potential archaeological sites candidates based on the provided location.

    Args:
        location (str): The location to search for archaeological sites.

    Returns:
        List[dict]: A list of potential archaeological sites candidates with site info.
    """

    # Example: get_satellite_images returns a list of dicts with 'image_url' and 'coordinates'
    img_path, test_image, data_folder = await get_satellite_images(lat, long)

    candidates = []
    # for img_path in img_paths:
        # Step 2: Run YOLO detection on each image
    detections = await detect_sites_in_image(img_path)
    # detections: list of dicts with 'site', 'coordinates', etc.

    # save the detection image
    await save_detection_image(img_path, test_image, detections, data_folder)

    for det in detections:
        candidate = {
            "predictions": det,
            "coordinates": {"lat": lat, "long": long}
        }
        candidates.append(candidate)
    return candidates

async def check_archaeological_site_validity(site: str) -> bool:
    """
    Check if the provided archaeological site is valid.
    Args:
        site (str): The archaeological site to check.
    Returns:
        bool: True if the site is valid, False otherwise.
    """
    # This is a placeholder implementation. Replace with actual logic to check site validity.
    valid_sites = ["Site A: Coordinates (12.34, 56.78)", "Site C: Coordinates (34.56, 78.90)"]
    return site in valid_sites

async def analyze_satellite_image(image_url: str) -> str:
    """
    Analyze the provided satellite image and return a description of the findings.
    Args:
        image_url (str): The URL of the satellite image to analyze.
    Returns:
        str: A description of the findings from the satellite image analysis.
    """
    # This is a placeholder implementation. Replace with actual logic to analyze the satellite image.
    return f"Analysis of the satellite image at {image_url} indicates potential archaeological features."

async def get_archaeological_sites(lat:float, long:float) -> List[str]:
    """
    Get a list of potential archaeological sites based on the provided location.

    Args:
        location (str): The location to search for archaeological sites.

    Returns:
        List[str]: A list of potential archaeological sites with their validity status and analysis.
    """
    logging.info(f"Searching for archaeological sites in location: {lat}, {long}...")

    candidates = await get_archaeological_sites_candidates(lat, long)
    # results = []
    # for site_info in candidates:
    #     site_name = site_info.get("site")
    #     site_image_url = site_info.get("image_url")
    #     is_valid = await check_archaeological_site_validity(site_name)
    #     analysis = await analyze_satellite_image(site_image_url)
    #     results.append(f"{site_name} - Valid: {is_valid}. Analysis: {analysis}")
    return candidates


if __name__ == "__main__":
    model = YOLO("src/model/weights.pt") 
    print("Model loaded successfully.")
    # Run inference with GPU
    results = model("src/model/image_1126.png", device="mps")
    results[0].show()
