# CLI for Processing .mdoc Files

This script provides a command-line interface (CLI) for parsing and updating `.mdoc` files.

## Usage

### Parse an .mdoc File

To parse an `.mdoc` file and extract its metadata, use the following command:

```bash
python main.py parse <file_path>
```

Replace `<file_path>` with the path to your `.mdoc` file.

### Update the DoseRate in an .mdoc File

To update the `DoseRate` in an `.mdoc` file, use the following command:

```bash
python main.py update <file_path> <new_dose_rate>
```

Replace `<file_path>` with the path to your `.mdoc` file and `<new_dose_rate>` with the new `DoseRate` value.

## Example

```bash
python main.py parse example.mdoc
python main.py update example.mdoc 15.0
```

This will parse the `example.mdoc` file and update its `DoseRate` to `15.0`.
