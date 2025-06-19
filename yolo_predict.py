"""
Roboflow model prediction script.
This script loads a Roboflow model and uses it to make predictions on an image.
It requires the Roboflow API key to be set as an environment variable.
Make sure to set the environment variable ROBOFLOW_API_KEY and GOOGLE_STATIC_MAPS_API_KEY
# You can set it in your terminal by running:
    export ROBOFLOW_API_KEY="your_api_key_here"
    export GOOGLE_STATIC_MAPS_API_KEY="your_api_key_here"
"""

from roboflow import Roboflow
import cv2
import os
import matplotlib.pyplot as plt
import requests
import json
import sys
from datetime import datetime


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
# define function to extract ee static image from url

def get_image_from_url(url, image_name, data_folder):
    response = requests.get(url)
    if response.status_code == 200:
        with open( os.path.join(data_folder, image_name), "wb") as file:
            file.write(response.content)
        print(f"✅ Satellite image '{image_name}' saved successfully! ✅")
    else:
        print(" ❌ Error:", response.text)

# get api keys
ee_API_KEY = os.environ.get("GOOGLE_STATIC_MAPS_API_KEY")
robo_api_key = os.environ.get("ROBOFLOW_API_KEY")

# get the  latitude and longitude of the location
test = {}
lat_long = input("Enter the latitude and longitude of the location (comma separated): ")
lat, long = lat_long.strip().split(",")
lat = lat.strip()
long = long.strip()

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

get_image_from_url(test['url'], f"{test_image}.png", data_folder)

# Load Roboflow model
rf = Roboflow(api_key=robo_api_key)
project = rf.workspace("draha").project("ee-archae_sites").version(4)
model = project.model
folder_path=data_folder
image_name = f"{test_image}.png"
image_path = "{}/{}".format(folder_path, image_name)

test['path'] = image_path 
test['image_name'] = image_name 

prediction = model.predict(image_path).json()
print(prediction)
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

# Show image
plt.savefig(os.path.join(data_folder, f"{test_image}_predictions.png"), bbox_inches='tight', pad_inches=0.1)
plt.imshow(img)
plt.axis('off')
plt.show()


test['predictions'] = preds

output_json = {
    "index": index,
    "image_name": test['image_name'],
    "predictions": test['predictions'],
    "url": test['url'],
    "lat": test['lat'],
    "long": test['long'],
    "path": test['path'],
    "check_time": datetime.now().isoformat()
}

json_file_path = os.path.join(data_folder, "Predictions.json")
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump([], json_file)  # Initialize with an empty list

with open(json_file_path, 'a') as json_file: 
    json.dump(output_json, json_file, indent=4)

index += 1
with open(index_file, "w") as f:
    f.write(str(index))
