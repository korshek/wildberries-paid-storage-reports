from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import time
import io
import csv
from datetime import datetime, timedelta
from dateutil import parser

app = Flask(__name__)

# Конфигурация API Wildberries
WB_API_BASE_URL = "https://seller-analytics-api.wildberries.ru"

class WildberriesAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
    
    def create_report_task(self, date_from, date_to):
        """Создание задания на генерацию отчета"""
        url = f"{WB_API_BASE_URL}/api/v1/paid_storage"
        params = {
            "dateFrom": date_from,
            "dateTo": date_to
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def check_task_status(self, task_id):
        """Проверка статуса задания"""
        url = f"{WB_API_BASE_URL}/api/v1/paid_storage/tasks/{task_id}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def download_report(self, task_id):
        """Скачивание отчета"""
        url = f"{WB_API_BASE_URL}/api/v1/paid_storage/tasks/{task_id}/download"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_report', methods=['POST'])
def create_report():
    data = request.json
    api_key = data.get('api_key')
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    
    if not all([api_key, date_from, date_to]):
        return jsonify({"error": "Все поля обязательны"}), 400
    
    # Проверяем, что период не превышает 8 дней
    try:
        from_date = parser.parse(date_from)
        to_date = parser.parse(date_to)
        if (to_date - from_date).days > 8:
            return jsonify({"error": "Период не может превышать 8 дней"}), 400
    except:
        return jsonify({"error": "Неверный формат даты"}), 400
    
    wb_api = WildberriesAPI(api_key)
    result = wb_api.create_report_task(date_from, date_to)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route('/api/check_status', methods=['POST'])
def check_status():
    data = request.json
    api_key = data.get('api_key')
    task_id = data.get('task_id')
    
    if not all([api_key, task_id]):
        return jsonify({"error": "Все поля обязательны"}), 400
    
    wb_api = WildberriesAPI(api_key)
    result = wb_api.check_task_status(task_id)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route('/api/download_report', methods=['POST'])
def download_report():
    data = request.json
    api_key = data.get('api_key')
    task_id = data.get('task_id')
    
    if not all([api_key, task_id]):
        return jsonify({"error": "Все поля обязательны"}), 400
    
    wb_api = WildberriesAPI(api_key)
    result = wb_api.download_report(task_id)
    
    if "error" in result:
        return jsonify(result), 400
    
    # Конвертируем в CSV
    if isinstance(result, list) and len(result) > 0:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=result[0].keys())
        writer.writeheader()
        writer.writerows(result)
        
        output.seek(0)
        
        # Создаем имя файла с текущей датой
        filename = f"paid_storage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    return jsonify({"error": "Отчет пуст или неверный формат"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 