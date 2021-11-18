from feature_extractor import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import ExtraTreeClassifier

x,y = batch_extract("E:\GIX\sample_root")
x = np.array(x)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)
extra_tree = ExtraTreeClassifier(random_state=0)
cls = BaggingClassifier(extra_tree, random_state=0).fit(X_train, y_train)
print(cls.score(X_test, y_test))

