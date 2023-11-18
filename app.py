from flask import Flask, render_template, request
import os 
from deeplearning import object_detection
import requests
from urllib.parse import quote


app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
# TOKEN = '9f705c754c2fb29a3fc7ef36c8d74469' ## token de consulta para apresentação
TOKEN = '40be640bf60ee817be81169aad1d7616'
BASE_URL = 'https://wdapi2.com.br/consulta/'


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text_list = []
        situacao = ''
        try:
            upload_file = request.files['image_name']
            filename = upload_file.filename
            path_save = os.path.join(UPLOAD_PATH,filename)
            upload_file.save(path_save)
            text_list = object_detection(path_save,filename)
            print(text_list)

            #Criando a URL para a API
            api_url = f'{BASE_URL}{text_list[0]}/{TOKEN}'
            print(api_url)

            # # Fazendo a requisição para a API
            response = requests.get(api_url)

            if response.status_code == 200:
                # Sucesso na requisição, parseando o JSON e pegando o valor de "situacao"
                json_response = response.json()
                situacao = json_response.get('situacao', '')
                print(situacao)
                if situacao == '' or situacao == 'none':
                    situacao = 'Não encontrado no sistema'
                    
                print("Requisição bem-sucedida:", json_response)
            else:
                situacao = 'Não encontrado'
                # Tratar erros na requisição
                print("Erro na requisição:", response.status_code)

        except:
            print("Couldn't save file")

        return render_template('index.html',upload=True,upload_image=filename,text=text_list,no=len(text_list), situacao=situacao)

    return render_template('index.html',upload=False)


if __name__ =="__main__":
    app.run(debug=True)