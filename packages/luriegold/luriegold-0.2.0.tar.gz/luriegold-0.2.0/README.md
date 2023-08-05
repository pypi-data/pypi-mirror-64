[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/ulf1/scipy-luriegold/master?urlpath=lab)

# luriegold
Lurie-Goldberg Algorithm to adjust a correlation matrix to be positive semi-definite.

## Installation
The `luriegold` [git repo](http://github.com/ulf1/scipy-luriegold) is available as [PyPi package](https://pypi.org/project/luriegold)

```
pip install luriegold
```


## Usage

```
from luriegold import luriegold
import numpy as np

# A matrix with subjectively set correlations
mat = [[ 1.   , -0.948,  0.099, -0.129],
       [-0.948,  1.   , -0.591,  0.239],
       [ 0.099, -0.591,  1.   ,  0.058],
       [-0.129,  0.239,  0.058,  1.   ]]
mat = np.array(mat)

# Convert to a positive semi-definite matrix
rho, _, _ = luriegold(mat)
print(rho.round(3))
```

Check the [examples](https://github.com/ulf1/scipy-luriegold/tree/master/examples) folder for notebooks.


## Commands
Install a virtual environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

Python commands

* Start virtual env: `source .venv/bin/activate`
* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

## Support
Please [open an issue](https://github.com/ulf1/scipy-luriegold/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/scipy-luriegold/compare/).
