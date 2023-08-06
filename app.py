from flask import Flask, jsonify, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    script_name = request.json.get('script_name')

    try:
        subprocess.check_call(['python', './timing/{}'.format(script_name)])
        return jsonify({"message": "Script run successfully"}), 200
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({"message": "Error while running script"}), 500


if __name__ == "__main__":
    app.run(port=5000)
