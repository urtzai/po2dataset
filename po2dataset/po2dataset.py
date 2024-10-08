#!/usr/bin/env python3

import os
import sys
import polib
import argparse
import json
import zipfile
import shutil
import requests

DEFAULT_FORMAT = "argosdata"
FORMAT_CHOICES = [DEFAULT_FORMAT, "zip"]

DEFAULT_LICENSE = "CC0"
LICENSE_MAPPING = {
    DEFAULT_LICENSE: "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt",
    "CC-BY": "https://creativecommons.org/licenses/by/4.0/legalcode.txt",
    "CC-BY-SA": "https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt",
}
LICENSE_CHOICES = [key for key, value in LICENSE_MAPPING.items()]


def create_workdir(output, name, source_code, target_code):
    try:
        path = os.path.join(
            output, "data-{}-{}_{}".format(name, source_code, target_code)
        )
        os.mkdir(path)
        print("Working directory '%s' created successfully" % path)
        return path
    except OSError as error:
        print(
            "Working directory '%s' can not be created. This folder already exists!"
            % path
        )
        sys.exit()


def create_dataset(path, output):
    pofile = polib.pofile(path)
    total_strings = len(pofile)
    strings = len(pofile.translated_entries())
    print("{} from {} strings to process".format(strings, total_strings))

    f_source = open("{}/source".format(output), "w")
    f_target = open("{}/target".format(output), "w")
    for i, entry in enumerate(pofile.translated_entries(), 1):
        print(entry.msgid, file=f_source)
        print(entry.msgstr, file=f_target)

        process = (i / strings) * 100
        print("%{:.0f} completed...".format(process), end="\r")
    f_source.close()
    f_target.close()
    print("\n")
    return strings


def create_metadata(output, name, source_code, target_code, ref, total_strings):
    metadata = {
        "name": name,
        "type": "data",
        "from_code": source_code,
        "to_code": target_code,
        "size": total_strings,
        "reference": ref,
    }
    with open("{}/metadata.json".format(output), "w") as f:
        json.dump(metadata, f, indent=2)


def add_license(output, license=DEFAULT_LICENSE):
    print("Adding {} license to the package...".format(license))
    response = requests.get(LICENSE_MAPPING[license])
    if response.status_code == 200:
        with open("{}/LICENSE".format(output), "w") as f:
            f.write(response.text)
    else:
        print("Couldn't retrieve the license due to connection issues")


def make_zip(output, format=DEFAULT_FORMAT):
    print("Creating {} file in {}".format(format, output))
    zip_path = "{}.{}".format(output, format)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        # Direktorioan dauden fitxategi guztiak zip fitxategian sartuko ditugu
        for root, dirs, files in os.walk(output):
            for file in files:
                file_path = os.path.join(root, file)
                # Fitxategia zip fitxategira gehitu
                zipf.write(file_path, os.path.relpath(file_path, output))
    print("Clearing working directory")
    shutil.rmtree(output)


def main():
    parser = argparse.ArgumentParser(description="Create dataset from po file")

    parser.add_argument("path", type=str, help="Absolute po file path")
    parser.add_argument(
        "-n", "--name", type=str, required=True, help="Source language code"
    )
    parser.add_argument(
        "-s", "--source_code", type=str, required=True, help="Source language code"
    )
    parser.add_argument(
        "-t", "--target_code", type=str, required=True, help="Target language code"
    )
    parser.add_argument(
        "-r", "--ref", type=str, required=True, help="Reference of the source data"
    )
    parser.add_argument(
        "-o", "--output", type=str, required=False, help="Output file path"
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=FORMAT_CHOICES,
        required=False,
        help="Extension name of the zip file",
    )

    parser.add_argument(
        "-l",
        "--license",
        type=str,
        choices=LICENSE_CHOICES,
        required=False,
        help="License file to be included in the package (select choice or provide custom file path)",
    )

    args = parser.parse_args()

    output = args.output or ""
    if output and not os.path.exists(output):
        print("{} output directory does not exist!!".format(output))
        sys.exit()

    output = create_workdir(output, args.name, args.source_code, args.target_code)

    total_strings = create_dataset(args.path, output)
    create_metadata(
        output, args.name, args.source_code, args.target_code, args.ref, total_strings
    )

    license = args.license or DEFAULT_LICENSE
    add_license(output, license)

    format = args.format or DEFAULT_FORMAT
    make_zip(output, format)

    print("Dataset created successfully!!")


if __name__ == "__main__":
    main()
