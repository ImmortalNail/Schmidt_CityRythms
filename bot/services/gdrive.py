from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from config import Config
import io
import logging

class GoogleDriveService:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file(
            Config.GOOGLE_CREDS,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def upload_photo(self, photo_file, user_id):
        try:
            # Download photo
            photo_bytes = io.BytesIO()
            photo_file.download(out=photo_bytes)
            photo_bytes.seek(0)
            
            # Upload to Drive
            file_metadata = {
                'name': f"passport_{user_id}_{int(photo_file.file_size)}.jpg",
                'parents': [Config.DRIVE_FOLDER_ID]
            }
            media = MediaIoBaseUpload(photo_bytes, mimetype='image/jpeg')
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()
            
            return file.get('webViewLink')
        except Exception as e:
            logging.error(f"Drive upload error: {e}")
            raise