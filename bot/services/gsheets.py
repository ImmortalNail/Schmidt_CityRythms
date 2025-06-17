import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import Config
from datetime import datetime
import logging

class GoogleSheetsService:
    def __init__(self):
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(Config.GOOGLE_CREDS, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(Config.SPREADSHEET_ID).sheet1
    
    def add_participant(self, user_id, name, age, route):
        try:
            self.sheet.append_row([
                str(user_id),
                name,
                age,
                route,
                datetime.now(Config.TIMEZONE).isoformat(),
                0,  # photos submitted
                datetime.now(Config.TIMEZONE).isoformat(),
                False  # winner status
            ])
            return True
        except Exception as e:
            logging.error(f"Error adding participant: {e}")
            return False
    
    def find_participant(self, user_id):
        try:
            records = self.sheet.get_all_records()
            for i, record in enumerate(records, start=2):
                if str(record.get('Telegram ID', '')) == str(user_id):
                    return i
            return None
        except Exception as e:
            logging.error(f"Error finding participant: {e}")
            return None
    
    def update_photo_count(self, user_id):
        row = self.find_participant(user_id)
        if row:
            try:
                current_count = int(self.sheet.cell(row, 6).value)
                self.sheet.update_cell(row, 6, current_count + 1)
                self.sheet.update_cell(row, 7, datetime.now(Config.TIMEZONE).isoformat())
                return True
            except Exception as e:
                logging.error(f"Error updating photo count: {e}")
        return False