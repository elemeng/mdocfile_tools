# CLI for Processing .mdoc Files

This script provides a command-line interface (CLI) for parsing and updating `.mdoc` files.

## Usage

### Parse an .mdoc File

To parse an `.mdoc` file and extract its metadata, use the following command:

```bash
python mdoc_tools.py parse <file_path>
```

Replace `<file_path>` with the path to your `.mdoc` file.

### Update the DoseRate in an .mdoc File

To update the `DoseRate` in an `.mdoc` file, use the following command:

```bash
python mdoc_tools.py update <file_path> <new_dose_rate>
```

Replace `<file_path>` with the path to your `.mdoc` file and `<new_dose_rate>` with the new `DoseRate` value.

### Batch Update the DoseRate in All .mdoc Files in a Directory

To batch update the `DoseRate` in all `.mdoc` files in a given directory, use the following command:

```bash
python mdoc_tools.py batch_update <directory> <new_dose_rate>
```

Replace `<directory>` with the path to the directory containing your `.mdoc` files and `<new_dose_rate>` with the new `DoseRate` value.

## Example

```bash
python mdoc_tools.py parse example.mdoc
python mdoc_tools.py update example.mdoc 15.0
python mdoc_tools.py batch_update /path/to/mdoc/files 15.0
```

This will parse the `example.mdoc` file, update its `DoseRate` to `15.0`, and batch update the `DoseRate` to `15.0` in all `.mdoc` files in the specified directory.
