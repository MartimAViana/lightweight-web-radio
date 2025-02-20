import argparse
import csv
from web_radio import create_radio, start_server
from pathlib import Path

def read_radio_config(csv_path):
    """Read radio configurations from a CSV file"""
    radios = []
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            if not {'name', 'path', 'url_prefix'}.issubset(reader.fieldnames):
                raise ValueError("CSV must have 'name', 'path', and 'url_prefix' columns")
            
            for row in reader:
                # Validate path exists
                path = Path(row['path'])
                if not path.exists():
                    print(f"Warning: Path does not exist: {path}")
                
                radios.append({
                    'name': row['name'].strip(),
                    'folder': str(path),
                    'url_prefix': row['url_prefix'].strip()
                })
    except FileNotFoundError:
        print(f"Error: Could not find CSV file: {csv_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    return radios

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Start web radio servers from CSV configuration')
    parser.add_argument('config', type=str, help='Path to CSV file containing radio configurations')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Read radio configurations
    radios = read_radio_config(args.config)
    if not radios:
        return
    
    if not radios:
        print("No valid radio configurations found in CSV")
        return
    
    # Create each radio
    for radio in radios:
        try:
            create_radio(radio['name'], radio['folder'], radio['url_prefix'])
            print(f"Created radio: {radio['name']} at /{radio['url_prefix']}")
        except Exception as e:
            print(f"Failed to create radio {radio['name']}: {e}")
    
    # Start the Flask server
    print("\nStarting server...")
    start_server()

if __name__ == "__main__":
    main() 