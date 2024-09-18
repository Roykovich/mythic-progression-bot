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

async def add_booster(email, user_name, user_id):
    try:
        sheet = get_sheets()
        sheet_last_row = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'Pagos Semanales!A2:A').execute()
        
        last_row = len(sheet_last_row.get('values')) + 2

        values = [
            [
                email,
                None,
                user_name,
                f'=CONTAR.SI(Ordenes!R:U;C{last_row})',
                f'=SI.ERROR(IFS(D{last_row}<20;"Booster";D{last_row}<100;"Gold Booster";D{last_row}<200;"Veteran Booster";D{last_row}<500;"Elite Booster";D{last_row}<700;"Master Booster"))',
                str(user_id)
            ]
        ]
        body = {"values": values}
        result = (
            get_sheets()
            .values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"[+] {(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as e:
        print(f"An error occurred: {e}")