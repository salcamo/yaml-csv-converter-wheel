import yaml
import csv
import io
import sys

def flatten_dict(d, parent_key='', sep='_'):
    """Helper function to flatten nested dictionaries."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for index, item in enumerate(v):
                items.extend(flatten_dict({f"{new_key}_{index}": item}, '', sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def yaml_to_csv(yaml_data):
    """Converts YAML data to CSV format."""
    try:
        yaml_obj = yaml.safe_load(yaml_data)

        # Wrap single dictionaries into a list for consistent processing
        if isinstance(yaml_obj, dict):
            yaml_obj = [yaml_obj]

        # Ensure we are processing a list of dictionaries (after flattening if needed)
        if not isinstance(yaml_obj, list) or not all(isinstance(item, dict) for item in yaml_obj):
            raise ValueError("Invalid YAML format. Expected a list of dictionaries or a single dictionary.")

        # Flatten the nested structures before writing to CSV
        flattened_data = [flatten_dict(item) for item in yaml_obj]

        output = io.StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=flattened_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(flattened_data)
        return output.getvalue()

    except Exception as e:
        return str(e)
    
def csv_to_yaml(csv_data):
    """Converts CSV data to YAML format."""
    input_stream = io.StringIO(csv_data)
    try:
        csv_reader = csv.DictReader(input_stream)
        rows = list(csv_reader)

        # Check if rows are empty (no valid data)
        if not rows:
            raise ValueError("CSV data is empty or invalid.")

        # Create YAML output
        yaml_output = yaml.dump(rows, default_flow_style=False, sort_keys=False, allow_unicode=True)
        yaml_output = "---\n"+yaml_output
        # Clean the output: No single quotes for strings
        cleaned_yaml = yaml_output.replace("'", "").strip()

        return cleaned_yaml

    except Exception as e:
        raise ValueError(f"Error converting CSV to YAML: {str(e)}")

def main():
    """Main function to handle command-line arguments for YAML to CSV and CSV to YAML conversions."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  yaml-csv-converter yaml_to_csv input.yaml > output.csv")
        print("  yaml-csv-converter csv_to_yaml input.csv > output.yaml")
        sys.exit(1)

    command = sys.argv[1]
    input_file = sys.argv[2]

    try:
        with open(input_file, 'r') as f:
            input_data = f.read()

        if command == 'yaml_to_csv':
            csv_output = yaml_to_csv(input_data)
            print(csv_output)
        elif command == 'csv_to_yaml':
            yaml_output = csv_to_yaml(input_data)
            print(yaml_output)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()