from thundergbm import TGBMClassifier as tc
from sklearn.datasets import load_digits

X, y = load_digits(return_X_y=True)
model_path = 'tgbm.model'
clf = tc(n_trees=20, depth=3)


clf.fit(X, y)
print(clf.predict(X))
clf.save_model(model_path)

clf2 = tc()
clf2.load_model(model_path)
print(clf2.predict(X))
