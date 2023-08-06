import pipelinetweak.pipe
import sklearn.pipeline
import sklearn.datasets
import sklearn.linear_model
import sklearn.dummy
import numpy as np


def test1():
    # load dataset
    tmp = sklearn.datasets.load_diabetes()
    y = tmp.target
    X = tmp.data

    # Regressor as transformer
    model = sklearn.pipeline.Pipeline(steps=[
        ('trans', pipelinetweak.pipe.PredT(
            sklearn.linear_model.LinearRegression())),
        ('pred', sklearn.dummy.DummyRegressor())
    ])
    # fit and predict
    model.fit(X, y)
    y_pred = model.predict(X)
    # compare
    target = [
        152.13348416, 152.13348416, 152.13348416, 152.13348416, 152.13348416]
    np.testing.assert_allclose(y_pred[:5], target)
