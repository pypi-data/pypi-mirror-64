# License: BSD 3 clause
#
# Authors: Roman Yurchak <rth.yurchak@gmail.com>
import os

import pandas as pd

from sklearn.svm import LinearSVC
from sklearn.preprocessing import Normalizer, FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import cross_validate
from sklearn.metrics import f1_score
from sklearn.pipeline import FeatureUnion

from sklearn_extra.feature_weighting import TfigmTransformer

if "CI" in os.environ:
    # make this example run faster in CI
    categories = ["sci.crypt", "comp.graphics", "comp.sys.mac.hardware"]
else:
    categories = None

docs, y = fetch_20newsgroups(return_X_y=True, categories=categories)


vect = CountVectorizer(min_df=5, stop_words="english", ngram_range=(1, 1))
X1 = vect.fit_transform(docs)
X = X1

res = []

from tqdm import tqdm

for n_features in tqdm([100, 200, 500, 1000, 5000, 10000, 1000000]):
    n_features = min(X.shape[1], n_features)
    pipe = make_pipeline(TfigmTransformer(tf_scale="sqrt", n_features=n_features), Normalizer())
    X_tr = pipe.fit_transform(X, y)
    est = LinearSVC()
    scoring = {
        "F1-macro": lambda est, X, y: f1_score(
            y, est.predict(X), average="macro"
        ),
        "balanced_accuracy": "balanced_accuracy",
    }
    scores = cross_validate(est, X_tr, y, scoring=scoring,)
    for key, val in scores.items():
        if not key.endswith("_time"):
            res.append(
                {
                    "metric": "_".join(key.split("_")[1:]),
                    "subset": key.split("_")[0],
                    "preprocessing": n_features,
                    "score": "{:.3f}±{:.3f}".format(val.mean(), val.std()),
                }
            )
scores = (
    pd.DataFrame(res)
    .set_index(["preprocessing", "metric", "subset"])["score"]
    .unstack(-1)
)
scores = scores["test"].unstack(-1).sort_values("F1-macro", ascending=False)
print(scores)
