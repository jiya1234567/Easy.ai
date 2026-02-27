from flask import Flask, render_template, request, jsonify
import json
import os
import kernel # We will create this next

app = Flask(__name__)

# Strict Paths
PATHS = {
    "fixed": "./FIXED/profile.json",
    "target": "Target.JASON",
    "variable_img": "./VARIABLE/input_image.jpg",
    "variable_txt": "./VARIABLE/placeholder.txt",
    "dashboard": "DASHBOARD.md"
}

@app.route('/')
def index():
    # Load data for the "Table" view
    with open(PATHS['fixed'], 'r') as f:
        fixed_data = json.load(f)
    with open(PATHS['target'], 'r') as f:
        target_data = json.load(f)
    
    # Check if files exist
    status = {k: os.path.exists(v) for k, v in PATHS.items()}
    
    return render_template('index.html', fixed=fixed_data, target=target_data, status=status)

@app.route('/execute', methods=['POST'])
def execute():
    # Triggers the 90-step audit
    report = kernel.run_audit(PATHS)
    return jsonify({"status": "Success", "report": report})

if __name__ == '__main__':
    app.run(debug=True, port=5000)