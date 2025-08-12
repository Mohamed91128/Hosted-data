import os
import json
import pandas as pd
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import zipfile
import io
import time

app = Flask(__name__)

# Configuration
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Use the same folder as the server for data
DATA_FOLDER = APP_ROOT
GAMES_EXCEL = os.path.join(DATA_FOLDER, 'games.xlsx')

# Ensure data directories exist
os.makedirs(os.path.join(DATA_FOLDER, 'stplugin'), exist_ok=True)
os.makedirs(os.path.join(DATA_FOLDER, 'depotcache'), exist_ok=True)
os.makedirs(os.path.join(DATA_FOLDER, 'librarycache_appcache'), exist_ok=True)
os.makedirs(os.path.join(DATA_FOLDER, 'librarycache_userdata_config'), exist_ok=True)
os.makedirs(os.path.join(DATA_FOLDER, 'sample_files'), exist_ok=True)

# Simulate cold start delay for testing (remove in production)
@app.before_request
def simulate_cold_start():
    # Uncomment to test cold start behavior
    # time.sleep(2)  # Simulate 2-second cold start
    pass

# Health check endpoint
@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'message': 'Hs Toolz Server is running',
        'endpoints': [
            '/gamelist',
            '/download/stplugin/<game_id>',
            '/download/depotcache/<game_id>',
            '/download/librarycache_appcache/<game_id>',
            '/download/librarycache_userdata_config/<game_id>',
            '/download/sample_files/<filename>',
            '/download/folder/<folder_name>'
        ]
    })

# Game list endpoint
@app.route('/gamelist')
def get_game_list():
    try:
        # Read Excel file
        df = pd.read_excel(GAMES_EXCEL)
        # Convert to JSON
        games_json = df.to_dict(orient='records')
        return jsonify(games_json)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download stplugin file
@app.route('/download/stplugin/<game_id>')
def download_stplugin(game_id):
    file_path = os.path.join(DATA_FOLDER, 'stplugin', f"{game_id}.lua")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': f'No stplugin file found for game {game_id}'}), 404

# Download depotcache file
@app.route('/download/depotcache/<game_id>')
def download_depotcache(game_id):
    # Look for any file starting with game_id in the depotcache folder
    depotcache_dir = os.path.join(DATA_FOLDER, 'depotcache')
    for filename in os.listdir(depotcache_dir):
        if filename.startswith(f"{game_id}_") and filename.endswith('.manifest'):
            file_path = os.path.join(depotcache_dir, filename)
            return send_file(file_path, as_attachment=True)
    
    return jsonify({'error': f'No depotcache file found for game {game_id}'}), 404

# Download librarycache_appcache folder
@app.route('/download/librarycache_appcache/<game_id>')
def download_librarycache_appcache(game_id):
    folder_path = os.path.join(DATA_FOLDER, 'librarycache_appcache', game_id)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Create a zip file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, folder_path)
                    zf.write(file_path, arc_name)
        
        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{game_id}_librarycache_appcache.zip"
        )
    else:
        return jsonify({'error': f'No librarycache_appcache folder found for game {game_id}'}), 404

# Download librarycache_userdata_config file
@app.route('/download/librarycache_userdata_config/<game_id>')
def download_librarycache_userdata(game_id):
    file_path = os.path.join(DATA_FOLDER, 'librarycache_userdata_config', f"{game_id}.json")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': f'No librarycache_userdata_config file found for game {game_id}'}), 404

# Download sample file
@app.route('/download/sample_files/<filename>')
def download_sample_file(filename):
    file_path = os.path.join(DATA_FOLDER, 'sample_files', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': f'Sample file {filename} not found'}), 404

# Download entire folder as zip
@app.route('/download/folder/<folder_name>')
def download_folder(folder_name):
    valid_folders = ['stplugin', 'depotcache', 'librarycache_appcache', 'librarycache_userdata_config', 'sample_files']
    
    if folder_name not in valid_folders:
        return jsonify({'error': f'Invalid folder name. Must be one of: {valid_folders}'}), 400
    
    folder_path = os.path.join(DATA_FOLDER, folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return jsonify({'error': f'Folder {folder_name} not found'}), 404
    
    # Create a zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, folder_path)
                zf.write(file_path, arc_name)
    
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{folder_name}.zip"
    )

# Verify key endpoint (for backward compatibility)
@app.route('/verify')
def verify_key():
    key = request.args.get('key', '')
    # Simple verification logic - in a real app, you'd check against a database
    if key and len(key) >= 5:  # Accept any key with 5+ characters
        return jsonify({'status': 'success', 'message': 'Key verified successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid key'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))