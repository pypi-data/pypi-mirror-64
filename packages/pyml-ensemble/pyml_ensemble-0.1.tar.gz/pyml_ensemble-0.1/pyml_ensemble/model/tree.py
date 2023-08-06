from .model import Model
from sklearn.tree import DecisionTreeClassifier

class TreeModel(Model):
    """ TreeModel
        Uses sklearn.tree.DecisionTreeClassifier as a model.
    """
    def __init__(self, criterion='gini', splitter='best',
                max_depth=None, min_samples_split=2, min_samples_leaf=1,
                min_weight_fraction_leaf=0.0, max_features=None,
                random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0,
                min_impurity_split=None, class_weight=None, ccp_alpha=0.0):
        super().__init__()
        self.model = DecisionTreeClassifier(criterion=criterion, splitter=splitter,
                        max_depth=max_depth, min_samples_split=min_samples_split,
                        min_samples_leaf=min_samples_split,
                        min_weight_fraction_leaf=min_weight_fraction_leaf,
                        max_features=max_features,random_state=random_state,
                        max_leaf_nodes=max_leaf_nodes,
                        min_impurity_decrease=min_impurity_decrease,
                        min_impurity_split=min_impurity_split,
                        class_weight=class_weight, ccp_alpha=ccp_alpha)

    def train(self, x, y):
        self.model.fit(x, y)

    def get_prediction(self, x):
        return self.model.predict(x)
