import threading, webbrowser
from flask import Flask
import hydra

import sys
import os
project_root = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.join(project_root, "..")
sys.path.append(project_root)
from planner.runner import main

app = Flask(__name__, static_folder='.', static_url_path='')

@hydra.main(config_path=os.path.join(project_root, "configs"), config_name="config.yaml")
def run(cfg):
    main(cfg)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    run()
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000') ).start()
    app.run(debug=False)
