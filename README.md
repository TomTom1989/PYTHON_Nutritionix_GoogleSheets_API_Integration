This Python code tracks exercises by interacting with the Nutritionix and Google Sheets APIs. Users can input their exercise details, and the script will record each exercise duration and calories burned in a Google Sheets document.

Features:
1) Nutritionix API Integration: Retrieves exercise information (calories burned, duration) based on user input, using personal metrics like weight, height, and age.
2) Google Sheets API Integration: Appends the exercise data, including exercise name, duration, and calories burned, to a specified Google Sheets document for easy tracking and logging.
3) Google Authentication: Uses OAuth2 credentials to authorize access to Google Sheets, storing tokens for future runs.
