import json
from install import PackageManager

with open('config.json', 'r') as f:
    config = json.load(f)

pm = PackageManager(config["Package"])
pm.run()

from app import app
import argparse

def getArgument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default="8003", help="PORT")
    parser.add_argument('--ip', type=str, default="0.0.0.0", help="IP")
    parser.add_argument('--debug', action="store_true", default=False, help="DEBUG MODE")
    args = parser.parse_args()

    return args

if __name__=="__main__":
    args = getArgument()

    app.run(debug=args.debug, host=args.ip, port=args.port)
