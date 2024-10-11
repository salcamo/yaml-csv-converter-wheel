# YAML-CSV Converter Library

## Overview

The **YAML-CSV Converter** is a Python library designed to facilitate the conversion between YAML and CSV file formats. This library is useful for data processing tasks where you need to transform structured data from one format to another. It supports both conversion directions: from YAML to CSV and from CSV to YAML.

## Features

- Convert YAML files to CSV format.
- Convert CSV files to YAML format.
- Easy-to-use command-line interface.
- CI/CD pipeline for automated testing, packaging, and deployment.
- Dockerization, making it portable and easily deployable across different environments.

## Project Structure

Here's the structure of the project:

```
yaml_csv_converter/
├── yaml_csv_converter/
│   ├── __init__.py         # Package initialization file
│   ├── converter.py        # Main conversion logic
├── test_converter.py       # Unit tests for the converter
├── app.py                  # Flask application for testing since it comes from the APIfied version
├── Dockerfile              # Docker configuration for containerization
├── input/output files      # Examples for you to try
├── requirements.txt        # Dependencies required for the project
├── setup.py                # Packaging configuration for the library
└── README.md               # Project documentation
```

## Installation

To use the YAML to CSV Converter library, follow these steps:

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installing the Library

1. **Clone the repository**:

   ```bash
   git clone https://github.com/salcamo/yaml-csv-converter-wheel.git
   cd yaml_csv_converter-wheel
   ```

2. **Install the package**:

   You can install the library locally by running:

   ```bash
   pip install .
   ```

   Alternatively, you can also install it in a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install .
   ```

## Usage

The library provides a command-line interface for converting YAML and CSV files. You can use the following commands:

### Convert YAML to CSV

To convert a YAML file to a CSV file, run:

```bash
yaml-csv-converter yaml_to_csv input.yaml > output.csv
```

### Convert CSV to YAML

To convert a CSV file to a YAML file, run:

```bash
yaml-csv-converter csv_to_yaml input.csv > output.yaml
```

### Example Usage

You can also use the converter programmatically by importing it in your Python scripts:

```python
from yaml_csv_converter.converter import yaml_to_csv, csv_to_yaml

# Convert YAML to CSV
yaml_to_csv('data.yaml')

# Convert CSV to YAML
csv_to_yaml('data.csv')
```

## CI/CD Pipeline

The CI/CD pipeline is set up using GitHub Actions to automate testing, packaging, and deployment processes. The pipeline will:

1. **Run tests** using pytest.
2. **Build a wheel file** for the library.
3. **Build a Docker image** containing the library.
4. **Push the Docker image** to Docker Hub.

### CI/CD Configuration

The pipeline configuration is defined in the `.github/workflows/cicd.yml` file. And you can check the last executions in the "Actions" tab.

### Secrets Configuration

Make sure to add your Docker Hub username and password as secrets in your GitHub repository settings. Use the following keys:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password

## Error Handling

The converter functions implement basic error handling using Python's `try-except` blocks. This helps catch and report errors that may occur during file reading, writing, or conversion. 

### Example Error Handling

Here’s an example of how errors are handled in the conversion functions:

```python
def csv_to_yaml(csv_data):
    """Converts CSV data to YAML format."""
    input_stream = io.StringIO(csv_data)
    try:
        ***

    except Exception as e:
        raise ValueError(***{str(e)}")
```

## Scalability and Adaptability

The YAML to CSV Converter is designed to be adaptable for future data sources and volumes. Here are a few strategies to ensure future scalability:

- **Asynchronous Processing**: Implement asynchronous I/O operations to handle larger files without blocking.
- **Batch Processing**: Extend the functionality to process multiple files in parallel.
- **Configuration Management**: Allow users to specify different data formats or input/output paths through configuration files or command-line arguments.

## Performance Considerations

- **Processing Time**: The processing time may vary based on the size of the input files and the complexity of the data structures. For larger files, we can consider profiling the code to identify potential bottlenecks.
- **Resource Utilization**: When deployed in a Docker container, we can monitor resource usage (CPU, memory) to ensure efficient operation.
