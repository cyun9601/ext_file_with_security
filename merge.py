from flask import Flask, request, render_template, Response
import os 
from pathlib import Path
import json
from tqdm.auto import tqdm
from modules.utils import load_config
import shutil

def merge_txts(data_dir, save_filename, from_ext = 'txt', ext_format = 'csv'):
    file_list = list(Path(data_dir).glob(f'*.{from_ext}'))
    
    line_list = []
    for i in tqdm(range(len(file_list))):
        idx = str(i).zfill(7)
        with open(os.path.join(data_dir, f'data_{idx}.{from_ext}'), 'r', encoding='UTF-8') as f:
            line_list.append(f.readline())       
            
    with open(f'./{save_filename}.{ext_format}', 'w', encoding='UTF-8') as f:
        f.write(''.join(line_list))
        

if __name__ == '__main__':
    
    PRJ_DIR = os.path.dirname(__file__)
    os.chdir(PRJ_DIR)
    
    # config 
    CONFIG_PATH = os.path.join(PRJ_DIR, 'config/merge.yaml')
    args = load_config(CONFIG_PATH)
    
    data_dir = os.path.join(PRJ_DIR, 'data', args.save_folder)

    merge_txts(data_dir, args.save_filename, from_ext = 'txt', ext_format=args.ext_format)

    if args.delete_receive: 
        shutil.rmtree(data_dir)
