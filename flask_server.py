from flask import Flask, request, render_template, Response
import os 
import json
from modules.utils import load_config


PRJ_DIR = os.path.dirname(__file__)
os.chdir(PRJ_DIR)

save_dir = os.path.join(PRJ_DIR, 'data')
os.makedirs(save_dir, exist_ok=True)

app = Flask(__name__)
   
@app.route('/')
def main():
    return 'Test Flask'

@app.route('/upload')
def upload_page():
    return render_template('upload.html')
	
@app.route('/send_data', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        folder_name = request.values['save_folder']
        idx = str(request.values['index']).zfill(7)
        line = request.values['data']
    
        folder_dir = os.path.join(save_dir, folder_name)    
        os.makedirs(folder_dir, exist_ok=True)
        file_path = os.path.join(folder_dir, f'data_{idx}.txt')
        
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(line)
            
        response = {
            # 'request_id':request_id,
            'response': True,
        }
    else :
        response = {
            'response': False
        }

    return Response(
        json.dumps(response),
        mimetype='multipart/form-data')

if __name__ == "__main__":
    PRJ_DIR = os.path.dirname(__file__)
    os.chdir(PRJ_DIR)
    
    # config 
    CONFIG_PATH = os.path.join(PRJ_DIR, 'config/server.yaml')
    args = load_config(CONFIG_PATH)
    
    app.run(host='0.0.0.0', port=args.port, debug=True) # debug: hot-reload 여부