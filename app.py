# app.py
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from scraper import scrape_commercial_hotel
from revenue_forecasting import run_forecasting_pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    data_payload = None

    if request.method == 'POST':
        # CASE A: User submitted a live website link to scrape
        if 'url' in request.form and request.form['url'].strip() != '':
            target_url = request.form['url'].strip()
            print(f"Initiating dynamic data extraction for target path: {target_url}")

            # Fire the advanced Playwright rendering loop
            scraped_df = scrape_commercial_hotel(target_url)
            if scraped_df is not None:
                # Pass the fresh scraped DataFrame straight into Subha's forecasting pipeline
                data_payload = run_forecasting_pipeline(df_input=scraped_df)

        # CASE B: User chose to upload a manual CSV/Excel sheet instead
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                data_payload = run_forecasting_pipeline(file_path=filepath)

    return render_template('index.html', data=data_payload)


if __name__ == '__main__':
    # Bind to 0.0.0.0 and use the port environment variable specified by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)