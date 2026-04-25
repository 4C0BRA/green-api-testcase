import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def index():
    response_text = ""
    id_instance = ""
    token = ""
    chat_id = ""
    message = ""
    urlFile = ""
    fileName =""
    
    if request.method == "POST":
        id_instance = request.form.get("idInstance", "")
        token = request.form.get("apiTokenInstance", "")
        action = request.form.get("action")
        chat_id = request.form.get("number", "")
        message = request.form.get("msg", "")
        urlFile = request.form.get("urlFile","")
        fileName = request.form.get("fileName","")
        
        
        # Проверка на пустые обязательные поля
        if not id_instance or not token:
            response_text = "Ошибка: ID Instance и API Token обязательны"
        else:
            url = ""
            if action == "settings":
                url = f"https://7107.api.greenapi.com/waInstance{id_instance}/getSettings/{token}"
            elif action == "state":
                url = f"https://7107.api.greenapi.com/waInstance{id_instance}/getStateInstance/{token}"
            elif action == "sendMessage":
                url = f"https://7107.api.greenapi.com/waInstance{id_instance}/sendMessage/{token}"
            elif action =="SendFileByUrl":
                url = f"https://7107.api.greenapi.com/waInstance{id_instance}/sendFileByUrl/{token}"

            
            try:
                if action == "sendMessage":
                    if not chat_id:
                        response_text = "Ошибка: Номер телефона не заполнен"
                    else:
                        payload = {
                            "chatId": chat_id + "@c.us",
                            "message": message,
                            "linkPreview": False
                        }
                        headers = {'Content-Type': 'application/json'}
                        
                        api_response = requests.post(url, json=payload, headers=headers)
                        api_response.raise_for_status()  # Raise для статус-кодов 4xx/5xx
                        response_dict = api_response.json()
                        response_text = json.dumps(response_dict, indent=4, ensure_ascii=False)
                elif action =="SendFileByUrl":
                    if not chat_id:
                        response_text = "Ошибка: Номер телефона не заполнен"
                    else:
                        payload = {
                            "chatId": chat_id + "@c.us",
                            "urlFile": urlFile,
                            "fileName": fileName
                        }
                        headers = {'Content-Type': 'application/json'}
                        
                        api_response = requests.post(url, json=payload, headers=headers)
                        api_response.raise_for_status()  # Raise для статус-кодов 4xx/5xx
                        response_dict = api_response.json()
                        response_text = json.dumps(response_dict, indent=4, ensure_ascii=False)

                else:
                    api_response = requests.get(url)
                    api_response.raise_for_status()  # Raise для статус-кодов 4xx/5xx
                    response_dict = api_response.json()
                    response_text = json.dumps(response_dict, indent=4, ensure_ascii=False)
            except requests.exceptions.HTTPError as e:
                response_text = f"HTTP ошибка {e.response.status_code}: {e.response.text}"
            except requests.exceptions.RequestException as e:
                response_text = f"Ошибка сети: {str(e)}"
            except json.JSONDecodeError as e:
                response_text = f"Ошибка парсинга JSON: {str(e)}"
            except Exception as e:
                response_text = f"Неизвестная ошибка: {str(e)}"
    
    return render_template("index.html", response_text=response_text, idInstance=id_instance, apiTokenInstance=token, number=chat_id, msg=message, urlFile=urlFile, fileName=fileName)


if __name__ == "__main__":
    app.run(debug=True)