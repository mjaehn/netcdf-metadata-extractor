# NetCDF Metadata Extractor

## Overview

The NetCDF Metadata Extractor is a Python script that extracts metadata information from NetCDF files, focusing on specific variables. It outputs the metadata in CSV format, sorted by variable name.

## Requirements

- Python 3.x
- Required Python packages: `xarray`

## Usage

### Running the Script

Run the script using the following command:

```bash

python netcdf_metadata_extractor.py [file_path or folder_path] [--output_file OUTPUT_FILE]

    [file_path or folder_path]: Path to the NetCDF file or folder containing multiple NetCDF files. It can be a relative or absolute path.
    --output_file OUTPUT_FILE (optional): Specify the output CSV file name. Default is output_metadata.csv.
```

Example Usage

```bash

python netcdf_metadata_extractor.py /path/to/netcdf/files --output_file extracted_metadata.csv

```
or for a single file:

```bash

python netcdf_metadata_extractor.py /path/to/netcdf/file.nc

```

### Output

The script generates a CSV file containing the following columns:
```
    Variable: The variable name within the NetCDF file.
    File Name: The name of the NetCDF file.
    Time Step: Output frequency step.
    Standard Name: The standard name attribute of the variable.
    Long Name: The long name attribute of the variable.
    Units: The units attribute of the variable. If not available, it is set to "-".
```

The output CSV file is sorted by the variable name.

## Notes

The script excludes certain variables (e.g., dimensions, coordinates) specified in the code.
If a variable has already been processed for a file, it is skipped to avoid duplicates.

## License

This project is licensed under the MIT License.
