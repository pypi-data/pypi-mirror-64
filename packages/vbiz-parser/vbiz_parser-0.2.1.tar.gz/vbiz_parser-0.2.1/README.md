### Dependencies

This package uses [pdfminer.six](https://pypi.org/project/pdfminer.six/) package for parsing pdf file

pip install pdfminer.six

### Usage

Change dir to folder which contains .pdf files downloaded from https://bocaodientu.dkkd.gov.vn/

Run command

```
vbiz_parser
vbiz_parser -i /path/to/file.pdf -o file.csv
vbiz_parser -i /path/to/file.pdf -u https://linktoupload.com
```

### Publish package

```
python setup.py sdist bdist_wheel
twine upload dist/*
```

### Install package

Locally
```
pip install .
```

PiPy
```
pip install vbiz_parser
```
