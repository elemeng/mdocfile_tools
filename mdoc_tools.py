import re
import argparse
import os
from typing import Dict, Any


def parse_mdoc_file(file_path: str) -> Dict[str, Any]:
    """
    Parse an .mdoc file and extract metadata.

    :param file_path: Path to the .mdoc file
    :return: Dictionary containing parsed metadata
    """
    metadata = {"global": {}}
    current_section = None

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except IOError:
        raise IOError(f"An error occurred while reading the file {file_path}.")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if the line is a section header
        section_match = re.match(r"\[(\w+)\s*=\s*([^\]]+)\]", line)
        if section_match:
            section_type, section_name = section_match.groups()
            if section_type not in metadata:
                metadata[section_type] = {}
            metadata[section_type][section_name] = {}
            current_section = (section_type, section_name)
            continue

        # Check if the line is a key-value pair
        key_value_match = re.match(r"(\w+)\s*=\s*(.*)", line)
        if key_value_match:
            key, value = key_value_match.groups()
            if current_section:
                section_type, section_name = current_section
                metadata[section_type][section_name][key] = value
            else:
                # Global data
                metadata["global"][key] = value

    return metadata


def update_dose_rate(file_path: str, new_dose_rate: float):
    """
    Update the DoseRate and related values in an .mdoc file.

    :param file_path: Path to the .mdoc file
    :param new_dose_rate: New DoseRate value
    """
    metadata = parse_mdoc_file(file_path)

    # Update DoseRate and related values
    for section_type, sections in metadata.items():
        for section_name, data in sections.items():
            if "DoseRate" in data:
                data["DoseRate"] = str(new_dose_rate)
                exposure_time = float(data.get("ExposureTime", 1))
                pixel_spacing = float(data.get("PixelSpacing", 1))
                num_subframes = float(data.get("NumSubFrames", 1))

                # Calculate ExposureDose
                exposure_dose = (new_dose_rate * exposure_time) / (pixel_spacing**2)
                data["ExposureDose"] = str(exposure_dose)

                # Calculate FrameDosesAndNumber
                frame_doses_and_number = exposure_dose / num_subframes
                data["FrameDosesAndNumber"] = (
                    f"{str(frame_doses_and_number)} {int(num_subframes)}"
                )

    # Calculate PriorRecordDose
    for section_type, sections in metadata.items():
        if section_type != "global":
            sorted_sections = sorted(
                sections.items(), key=lambda x: x[1].get("DateTime", "")
            )
            accumulated_dose = 0
            for section_name, data in sorted_sections:
                if "ExposureDose" in data:
                    data["PriorRecordDose"] = str(accumulated_dose)
                    accumulated_dose += float(data["ExposureDose"])

    # Write the updated metadata back to the file
    with open(file_path, "w") as file:
        for section_type, sections in metadata.items():
            if section_type == "global":
                for key, value in sections.items():
                    file.write(f"{key} = {value}\n")
            else:
                for section_name, data in sections.items():
                    file.write("\n")
                    file.write(f"[{section_type} = {section_name}]\n")
                    for key, value in data.items():
                        file.write(f"{key} = {value}\n")
    print(
        f"Updated DoseRate to {new_dose_rate} and Changed ExposureDose, FrameDosesAndNumber and PriorRecordDose accordingly in {file_path}"
    )


def batch_update_dose_rate(directory: str, new_dose_rate: float):
    """
    Batch update the DoseRate for all .mdoc files in a given directory.

    :param directory: Path to the directory containing .mdoc files
    :param new_dose_rate: New DoseRate value
    """
    for filename in os.listdir(directory):
        if filename.endswith(".mdoc"):
            file_path = os.path.join(directory, filename)
            update_dose_rate(file_path, new_dose_rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .mdoc files.")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the parse command
    parse_parser = subparsers.add_parser("parse", help="Parse an .mdoc file")
    parse_parser.add_argument("file_path", type=str, help="Path to the .mdoc file")

    # Subparser for the update command
    update_parser = subparsers.add_parser(
        "update", help="Update the DoseRate in an .mdoc file"
    )
    update_parser.add_argument("file_path", type=str, help="Path to the .mdoc file")
    update_parser.add_argument("new_dose_rate", type=float, help="New DoseRate value")

    # Subparser for the batch update command
    batch_update_parser = subparsers.add_parser(
        "batch_update",
        help="Batch update the DoseRate in all .mdoc files in a directory",
    )
    batch_update_parser.add_argument(
        "directory", type=str, help="Path to the directory containing .mdoc files"
    )
    batch_update_parser.add_argument(
        "new_dose_rate", type=float, help="New DoseRate value"
    )

    args = parser.parse_args()

    if args.command == "parse":
        metadata = parse_mdoc_file(args.file_path)
        print(metadata)
    elif args.command == "update":
        update_dose_rate(args.file_path, args.new_dose_rate)
        print(f"DoseRate updated to {args.new_dose_rate} in {args.file_path}")
    elif args.command == "batch_update":
        batch_update_dose_rate(args.directory, args.new_dose_rate)
        print(
            f"Batch updated DoseRate to {args.new_dose_rate} in all .mdoc files in {args.directory}"
        )
