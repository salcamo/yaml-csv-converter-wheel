from flask import Flask, request, jsonify, send_file, Response
from yaml_csv_converter.converter import yaml_to_csv, csv_to_yaml
import io

app = Flask(__name__)

@app.route('/yaml-to-csv', methods=['POST'])
def convert_yaml_to_csv():
    # API endpoint to convert YAML to CSV.
    try:
        if 'file' in request.files:
            yaml_file = request.files['file'].read().decode('utf-8')
        else:
            yaml_file = request.data.decode('utf-8')

        csv_data = yaml_to_csv(yaml_file)

        if "Invalid YAML" in csv_data:  # Error check from yaml_to_csv()
            return jsonify({"error": csv_data}), 400

        # Return CSV as a downloadable file
        return send_file(io.BytesIO(csv_data.encode()), 
                         download_name='output.csv',  # Changed for Flask 2.x compatibility
                         as_attachment=True, 
                         mimetype='text/csv')

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/csv-to-yaml', methods=['POST'])
def convert_csv_to_yaml():
    # API endpoint to convert CSV to YAML.
    try:
        if 'file' in request.files:
            csv_file = request.files['file'].read().decode('utf-8')
        else:
            csv_file = request.data.decode('utf-8')

        yaml_data = csv_to_yaml(csv_file)

        # Return the YAML output as plain text with the appropriate MIME type
        return Response(yaml_data, mimetype='text/x-yaml')

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
