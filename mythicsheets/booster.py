from mythicsheets.main import get_sheets
from googleapiclient.errors import HttpError

import settings

SPREADSHEET_ID = settings.GOOGLE_SHEET_ID
RANGE = "Pagos Semanales!A2:H"

async def get_boosters(user_id):
    try:
        sheet = get_sheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        values = result.get("values", [])

        if not values:
            print("No data found.")

        user = None
        for row in values:
            if user_id in row:
                user = values.index(row)
                break

        if user is not None:
            return values[user]

        else:
            return None

    except HttpError as e:
        print(f"An error occurred: {e}")
