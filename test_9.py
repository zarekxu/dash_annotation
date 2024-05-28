import os
from flask import Flask, render_template, send_file, redirect, url_for
from google.cloud import storage

app = Flask(__name__)

# Set up the Google Cloud Storage client
client = storage.Client.from_service_account_json('path/to/your/service-account-file.json')
bucket_name = 'your-gcs-bucket-name'
local_folder = 'downloads'

# Ensure the local folder exists
if not os.path.exists(local_folder):
    os.makedirs(local_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download_file():
    file_name = 'file-to-download.txt'  # Specify the file name in the GCS bucket
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    local_file_path = os.path.join(local_folder, file_name)
    blob.download_to_filename(local_file_path)
    
    # Optional: Serve the file to the user or redirect to a success page
    return send_file(local_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)



<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download File</title>
</head>
<body>
    <h1>Download File from GCS</h1>
    <form action="{{ url_for('download_file') }}" method="get">
        <button type="submit">Download File</button>
    </form>
</body>
</html>


