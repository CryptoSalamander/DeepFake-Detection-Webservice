import os
import subprocess

class PackageManager:
    def __init__(self, config):
        self.config = config
    
    def CheckFolder(self, path):
        return os.path.isdir(path)

    def CheckFile(self, path):
        return os.path.isfile(path)

    def Install(self, path, model):
    
        try:
            res = subprocess.check_output(["which wget"], shell=True).decode('utf-8')
        except Exception:
            print("[ERROR] You must Download wget")
            exit(0)

        os.system(f"wget -O {path} {self.config['download url'][model]}")

    def run(self):

        # Check Folder 
        path = self.config["pretrained dir"]
        if not self.CheckFolder(path):
            print(f"{path} is not exist")
            os.makedirs(path)

        # Check pretrained model 
        for model in self.config["model name"]:
            model_path = '/'.join([path, model])
            if not self.CheckFile(model_path):
                print(f"{model} is not exist", end=' ')
                print(f"Install {model}")
                self.Install(model_path, model)
