import requests 
import threading
import os 
from modules.utils import load_config
from tqdm.auto import tqdm

def split_dict(dictionary, n_division):
    result = []

    n_data = len(dictionary)
    n_split_data = int(n_data / n_division)

    partial_result = []
    for i, (k, v) in enumerate(dictionary.items()):
        partial_result.append({k:v})

        if (i + 1) % n_split_data == 0:
            result.append(partial_result)
            partial_result = []
    
    if len(partial_result) != 0 :
        result.append(partial_result)

    return result

def send_api(url, line_dict_list, save_folder):
    for line_dict in tqdm(line_dict_list):
        response = False 
        while True:
            response = requests.post(url, data={'save_folder':save_folder, 'index':list(line_dict.keys())[0], 'data':list(line_dict.values())[0]})
            if response.status_code == 200 : 
                break


if __name__ == '__main__':

    PRJ_DIR = os.path.dirname(__file__)
    os.chdir(PRJ_DIR)

    # config 
    CONFIG_PATH = os.path.join(PRJ_DIR, 'config/send.yaml')
    args = load_config(CONFIG_PATH)

    print(args.send_file)

    with open(args.send_file, encoding='UTF-8') as f: 
        line_list = []
        
        lines = f.readlines()
        
        line_dict = {i:line for i, line in enumerate(lines)}

        split_list = split_dict(line_dict, args.n_thread)

        thread_list = []
        for i in range(args.n_thread):
            thread_list.append(threading.Thread(target=send_api, args = (f'{args.url}/send_data', split_list[i], args.save_folder)))

        for i in range(args.n_thread):
            
            thread_list[i].start()        