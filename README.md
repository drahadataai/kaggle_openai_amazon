# kaggle_openai_amazon

## 1. How to create new branch from main:
### 1.1 create clone the repo
* creata a new folder: "DrAha"
* open folder from vscode, then do init repo
* from teminal do \
``` git clone https://github.com/drahadataai/kaggle_openai_amazon.git ```\
(this is the main branch url)

### 1.2 Create a new branch from main:
* Make sure you're on the main branch, in the bash terminal run the following\
``` git checkout main ```\
Update your local main branch with the latest remote changes\
``` git pull origin main ```\
Create and switch to a new branch (replace 'my-feature-branch' with your branch name) \
``` git checkout -b my-feature-branch ```\
then confirm ur current branch:\
``` git branch ```   

* create virtual venv, install dependencies from project
(if no peotry , install poetry first:  ```pip install poetry``` )\
``` poetry install ```
add a .gitignore to the root to avoid upload environment related files

now every thing is ready, next is to run main
## 2. Run main
* use your own api key to replace the ap_key in model_clients.py
* then, select interpreter as ur own virtual environment
* make sure ur current dir is under kaggle_openai_amazon, then run the following code in terminal\
``` poetry run python -m src.main ```\
if you can see the ZAgent response, it is successful.

## 3. yolo_pred.py
This is a yolo_v11 model to predict if there is a archae sites for a given lat,long.

To run this, you need api from roboflow and google static maps, you can set it in terminal by running:\
    ``` export GOOGLE_STATIC_MAPS_API_KEY="your_api_key_here"```

To use it, imput lat, long using comma seperation

Results pictures will be saved in Robo_Predict_dataset.\
A hisory of all checked files are saved in  "Predictions.json" under the same workfolder.\
The index.txt is a temp file to store how many images has been checked.
