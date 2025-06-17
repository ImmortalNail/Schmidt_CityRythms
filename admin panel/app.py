from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template_string  # render_template_string для безопасности
from bot.services.gsheets import GoogleSheetsService
from config import Config
import logging

app = Flask(__name__)
gsheets = GoogleSheetsService()

app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True  # Для HTTPS

@app.route('/')
def dashboard():
    try:
        participants = gsheets.sheet.get_all_records()
        return render_template('dashboard.html', participants=participants)
    except Exception as e:
        logging.error(f"Dashboard error: {e}")
        return "Error loading data", 500

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        participant_id = request.form.get('participant_id')
        message = request.form.get('message')
        # Здесь должна быть логика отправки сообщения через бота
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Message sending error: {e}")
        return redirect(url_for('dashboard'))

@app.route('/broadcast', methods=['POST'])
def broadcast():
    try:
        message = request.form.get('message')
        # Логика массовой рассылки
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Broadcast error: {e}")
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)