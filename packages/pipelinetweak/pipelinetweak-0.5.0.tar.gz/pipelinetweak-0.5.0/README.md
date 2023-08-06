[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kmedian/pipelinetweak/master?urlpath=lab)

# pipelinetweak
This package contain additional wrapper classes for the sklearn API.

## Installation
The `pipelinetweak` [git repo](https://github.com/ulf1/sklearn-pipelinetweak) is available as [PyPi package](https://pypi.org/project/pipelinetweak)

```
pip install pipelinetweak
```


## Usage

### Model predictions as transformer (`pipelinetweak.pipe`)
The predictions of `LinearRegression` are used as features for the `DummyRegressor`.

```

from sklearn.pipeline import Pipeline
from pipelinetweak.pipe import PredT
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor

model = Pipeline(steps=[
    ('trans', PredT(LinearRegression())),
    ('pred', DummyRegressor())
])
```

The predicted cluster labels (`KMeans`) are one-hot encoded (`OneHotEncoder`), merged with the scaled raw features (`FeatureUnion` and `StandardScaler`), and piped as regressors to a linear model.

```
from sklearn.pipeline import Pipeline, FeatureUnion
from pipelinetweak.pipe import PredT
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

model = Pipeline(steps=[
    ('trans', FeatureUnion(transformer_list=[
        ('prefit', Pipeline(steps=[
            ('kmeans', PredT(KMeans(n_clusters=7))),
            ('onehot', OneHotEncoder(categories='auto'))         
        ])),
        ('scaler', StandardScaler())
    ])),
    ('pred', LinearRegression(fit_intercept=False))
])
```

The predicted probabilities of a binary classifier are used as features.

```
from pipelinetweak.pipe import ProbT
from sklearn.linear_model import LogisticRegression

trans = ProbT(LogisticRegression(solver='lbfgs', multi_class='multinomial'), drop=False)
trans.fit(X, y)
Z = trans.transform(X)
```


Check the [examples](https://github.com/ulf1/sklearn-pipelinetweak/tree/master/examples) folder for notebooks.


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
Please [open an issue](https://github.com/ulf1/sklearn-pipelinetweak/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/sklearn-pipelinetweak/compare/).
