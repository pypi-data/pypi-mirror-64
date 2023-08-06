# missing_values_101703283

_For : **Project-3 (UCS633)**_  
_Submitted by : **Katinder Kaur**_  
_Roll no : **101703283**_  
_Group : **3COE13**_  


missing_values_101703283 is a Python library for dealing with missing values(NaN) in a numeric dataset. This simple package uses column mean to replcae the NaN values.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install missing_values_101703283.

```bash
pip install missing_values_101703283
```

## Usage

### For command prompt:

```
usage: missing_val [-h] InputDataFile

positional arguments:
  InputDataFile  Enter the name of input CSV file with .csv extension

optional arguments:
  -h, --help     show this help message and exit
```

Enter the input csv filename followed by _.csv_ extentsion
```bash
missing_values sample_inputfile.csv
```
after the records with NaN values are removed, the resultant data will be implicitly stored in the same file as input.

#### View help
To view usage __help__, use
```
missing_values -h
```

### For Python IDLE:

```python
>>> from missing_values.missing_values import missing_values_fn
>>> missing_values_fn('inputfile.csv')
Missing values successully replaced with column average.
``` 
## License
[MIT](https://choosealicense.com/licenses/mit/)