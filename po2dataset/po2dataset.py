import os
import sys
import polib
import argparse
import json
import shutil


def create_workdir(output, name, source_code, target_code):
    try:
        path = os.path.join(
            output, "data-{}-{}_{}".format(name, source_code, target_code)
        )
        os.mkdir(path)
        print("Working directory '%s' created successfully" % path)
        return path
    except OSError as error:
        print("Working directory '%s' can not be created" % path)
        sys.exit()


def create_dataset(path, output):
    pofile = polib.pofile(path)
    total_strings = len(pofile)
    print("{} strings to process".format(total_strings))

    f_source = open("{}/source".format(output), "w")
    f_target = open("{}/target".format(output), "w")
    for i, entry in enumerate(pofile.translated_entries(), 1):
        print(entry.msgid, file=f_source)
        print(entry.msgstr, file=f_target)

        process = (i / total_strings) * 100
        print("%{:.0f} completed...".format(process), end="\r")
    f_source.close()
    f_target.close()
    print("\n")
    return total_strings


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


def make_zip(output, format="zip"):
    print("Creating {} file".format(format))
    shutil.make_archive(output, "zip", output)
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
    make_zip(output)

    print("Dataset created successfully!!")


if __name__ == "__main__":
    main()
