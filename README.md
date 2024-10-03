# PO2Dataset

Python tool to extract sentences from po files and create language datasets for NLP machine learning and neural machine translation.

This command line tool is intended to create dataset packages suitable for [Argos Train](https://github.com/argosopentech/argos-train).

## How to install

### Manual installation

Create a virtual environment using [virtualenv](https://virtualenv.pypa.io/en/latest/index.html)

```bash
git clone https://github.com/urtzai/po2dataset.git
virtualenv po2dataset
cd po2dataset
source ./bin/activate
```

## Quick start guide

### Create Argos Train suitable dataset

```python
python po2dataset/po2dataset.py <path_to_po_file> --name <project_name> --source_code <source_lang_code> --target_code <target_lang_code> --ref "Some reference information of the project"
```

Where:

- `name`: The name of the project
- `source_code`: Source language code ([ISO 639](https://en.wikipedia.org/wiki/ISO_639))
- `target_code`: Target language code ([ISO 639](https://en.wikipedia.org/wiki/ISO_639))
- `ref`: Some reference information of the project

## Support

Should you experience any issues do not hesistate to post an issue or contribute in this project pulling requests.
