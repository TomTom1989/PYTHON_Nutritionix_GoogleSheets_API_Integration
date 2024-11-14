from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from datetime import datetime
import requests

# Nutritionix API credentials
GENDER = "male"
WEIGHT_KG = 89
HEIGHT_CM = 175
AGE = 35
APP_ID = "27f905b5"
API_KEY = "14e1dd3bede0b27ccb7c5f43f8070367"
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1SPH8pH3lb9cqbT15VoBdBJ31kGZGtnburVjkEb4Nu_M'
RANGE = 'workouts'  

# Function to authenticate with Google Sheets API
def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_136482652718-29uunihtn7o01v7r9r3h8b0ai93ft7e9.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future runs
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def update_google_sheet(exercise_data):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    body = {
        'values': exercise_data
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updates').get('updatedCells')} cells appended.")

# Nutritionix API request
exercise_text = input("Tell me which exercises you did: ")
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

# Process data to append to Google Sheets
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
exercise_data = []
for exercise in result["exercises"]:
    exercise_data.append([
        today_date,
        now_time,
        exercise["name"].title(),
        exercise["duration_min"],
        exercise["nf_calories"]
    ])

# Update Google Sheets with the exercise data
update_google_sheet(exercise_data)
