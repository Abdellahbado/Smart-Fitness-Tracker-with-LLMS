from googleapiclient.discovery import build
import json
import json
import os
from google.cloud import vision
from google.oauth2 import service_account
import pandas as pd

# Set up Google Cloud Vision client
credentials = service_account.Credentials.from_service_account_file(
    "Calorie Calculator IAM Admin.json"
)
client = vision.ImageAnnotatorClient(credentials=credentials)


def search_youtube_videos(query, max_results=1):
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    search_response = (
        youtube.search()
        .list(q=query, type="video", part="id,snippet", maxResults=max_results)
        .execute()
    )

    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(
                f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
            )

    return videos


def detect_food(image):
    image = vision.Image(content=image)
    response = client.label_detection(image=image)
    print("response", response)
    labels = response.label_annotations
    return [label.description for label in labels if label.score > 0.7]


PROGRESS_DATA_FILE = "data/user_progress_data.json"


def load_progress_data(username):
    if os.path.exists(PROGRESS_DATA_FILE):
        with open(PROGRESS_DATA_FILE, "r") as f:
            all_progress_data = json.load(f)
            user_data = all_progress_data.get(username, [])
            df = pd.DataFrame(user_data)

            # Check if the DataFrame is not empty and contains the 'Date' column
            if not df.empty and "Date" in df.columns:
                # Convert string dates back to datetime objects
                df["Date"] = pd.to_datetime(df["Date"])
            else:
                # If the DataFrame is empty or doesn't have a 'Date' column,
                # return an empty DataFrame with the expected columns
                return pd.DataFrame(
                    columns=["Date", "Weight", "Body Fat %", "Muscle Mass", "Notes"]
                )

            return df
    return pd.DataFrame(
        columns=["Date", "Weight", "Body Fat %", "Muscle Mass", "Notes"]
    )


def save_progress_data(username, data):
    all_progress_data = {}
    if os.path.exists(PROGRESS_DATA_FILE):
        with open(PROGRESS_DATA_FILE, "r") as f:
            all_progress_data = json.load(f)

    # Convert date objects to strings
    data["Date"] = data["Date"].apply(lambda x: x.strftime("%Y-%m-%d"))

    all_progress_data[username] = data.to_dict("records")

    with open(PROGRESS_DATA_FILE, "w") as f:
        json.dump(all_progress_data, f)
