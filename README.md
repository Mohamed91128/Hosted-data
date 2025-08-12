# Hs Toolz Server

This is the server component for Hs Toolz, designed to host game files and data that can be accessed by the Hs Toolz client application.

## Server Structure

```
hosted_server/
├── app.py                        # Main Flask application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── games.xlsx                    # Game database Excel file
├── stplugin/                     # Steam plugin files (.lua)
├── depotcache/                   # Depot cache files (.manifest)
├── librarycache_appcache/        # Library cache folders
├── librarycache_userdata_config/ # Library cache JSON files
└── sample_files/                 # Sample files for testing
```

## API Endpoints

- `/` - Server status and available endpoints
- `/gamelist` - Returns the contents of games.xlsx as JSON
- `/download/stplugin/<game_id>` - Download a specific game's .lua file
- `/download/depotcache/<game_id>` - Download a specific game's manifest file
- `/download/librarycache_appcache/<game_id>` - Download a specific game's library cache folder as ZIP
- `/download/librarycache_userdata_config/<game_id>` - Download a specific game's JSON file
- `/download/sample_files/<filename>` - Download a specific sample file
- `/download/folder/<folder_name>` - Download an entire folder as ZIP
- `/verify` - Legacy key verification endpoint

## Local Development

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the server:
   ```
   python app.py
   ```

5. The server will be available at http://localhost:8080

## Deployment

This server is designed to be deployed on Render.com. See the deployment guide in the main project README for step-by-step instructions.

## Notes

- The server automatically creates the necessary directories on startup if they don't exist.
- Place your data files directly in the server folder structure as shown above.
- Simply put your game files in the appropriate folders:
  - `.lua` files in the `stplugin` folder
  - `.manifest` files in the `depotcache` folder
  - Game folders in the `librarycache_appcache` folder
  - `.json` files in the `librarycache_userdata_config` folder
  - Sample files in the `sample_files` folder
  - Your game database Excel file as `games.xlsx` in the root server folder
- The free tier on Render.com has cold starts (15-30 seconds delay) when the server hasn't been accessed for a while.