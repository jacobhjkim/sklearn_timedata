print(__doc__)

import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import *
from sklearn.neural_network import *
from sklearn.neighbors import *
from sklearn.svm import *
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.tree import *
from sklearn.ensemble import *
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn import preprocessing


file = open('result.csv', 'w')

ALGORITHM_NAMES = ["kNN", "Radius Neighbors", "SVM", "Decision Tree",
         "Random Forest", "Neural Net", "AdaBoost",
        ]

scores = ['accuracy', 'precision', 'recall']

classifiers = [
    KNeighborsClassifier(),
    SVC(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    MLPClassifier(),
    AdaBoostClassifier(),
]

regressors = [
    KNeighborsRegressor(),
    SVR(),
    DecisionTreeRegressor(),
    RandomForestRegressor(),
    MLPRegressor(),
    AdaBoostRegressor(),
]

# Parameters used for parameter fields below
k_range = list(range(1, 10))
leaf_range = list(range(25, 35))
degree_range = list(range(2, 5))
n_range = list(range(1, 10))
m_range = list(range(1, 3))
hidden_layer_size_range = list(range(80, 150))

classifiers_list = [DecisionTreeClassifier(random_state=3, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=4, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=5, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=6, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=7, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=8, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=9, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=10, max_features="auto", class_weight="auto", max_depth=None),
                    DecisionTreeClassifier(random_state=11, max_features="auto", class_weight="auto", max_depth=None),
                    MLPClassifier(hidden_layer_sizes=100),
                    MLPClassifier(hidden_layer_sizes=110),
                    MLPClassifier(hidden_layer_sizes=120),
                    MLPClassifier(hidden_layer_sizes=130),
                    MLPClassifier(hidden_layer_sizes=140),
                    MLPClassifier(hidden_layer_sizes=150),
                    MLPClassifier(hidden_layer_sizes=160),
                    MLPClassifier(hidden_layer_sizes=170),
                    MLPClassifier(hidden_layer_sizes=180),
                    MLPClassifier(hidden_layer_sizes=190),
                    ]

regressors_list = [DecisionTreeRegressor(random_state=3, max_features="auto", max_depth=None),
                   DecisionTreeRegressor(random_state=4, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=5, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=6, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=7, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=8, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=9, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=10, max_features="auto",max_depth=None),
                   DecisionTreeRegressor(random_state=11, max_features="auto",max_depth=None),
                   MLPRegressor(hidden_layer_sizes=100),
                   MLPRegressor(hidden_layer_sizes=110),
                   MLPRegressor(hidden_layer_sizes=120),
                   MLPRegressor(hidden_layer_sizes=130),
                   MLPRegressor(hidden_layer_sizes=140),
                   MLPRegressor(hidden_layer_sizes=150),
                   MLPRegressor(hidden_layer_sizes=160),
                   MLPRegressor(hidden_layer_sizes=170),
                   MLPRegressor(hidden_layer_sizes=180),
                   MLPRegressor(hidden_layer_sizes=190),
                   ]
n_estimator_range = list(range(50, 200))

tuned_parameters_classifiers = [
    # knn classifier
    {'n_neighbors': k_range, 'weights': ['uniform', 'distance'],
     'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'leaf_size': leaf_range},

    # SVM classifier
    {'kernel': ['rbf', 'linear', 'poly', 'sigmoid'], 'gamma': [1e-3, 1e-4], 'C': [1, 20, 100, 1000],
     'degree': degree_range},

    # Decision Tree Classifier
    {'max_depth': n_range, 'max_features': ['auto', 'sqrt', 'log2']},

    # Random Forest Classifier
    {'max_depth': n_range, 'n_estimators': n_estimator_range, 'max_features': ['auto', 'sqrt', 'log2', 'None']},

    # Neural Net, MLPClassifier
    {'hidden_layer_sizes': hidden_layer_size_range, 'activation': ['identity', 'logistic', 'tanh', 'relu'],
    'solver': ['lbfgs', 'sgd', 'adam'], 'learning_rate': ['constant', 'invscaling', 'adaptive']},

    # AdaBoostClassifier
    {'base_estimator': classifiers_list, 'n_estimators': n_estimator_range},
]

tuned_parameters_regressors = [
    # knn regression
    {'n_neighbors': k_range, 'weights': ['uniform', 'distance'],
     'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'leaf_size': leaf_range},

    # SVR classifier
    {'kernel': ['rbf', 'linear', 'poly', 'sigmoid', 'precomputed'], 'gamma': [1e-3, 1e-4], 'C': [1, 20, 100, 1000],
     'degree': degree_range},

    # Decision Tree Regressor
    {'max_depth': n_range, 'max_features': ['auto', 'sqrt', 'log2', 'None']},

    # Random Forest Regressor
    {'max_depth': n_range, 'n_estimators': n_estimator_range, 'max_features': ['auto', 'sqrt', 'log2', 'None']},

    # Neural Net, MLPRegressor
    {'hidden_layer_sizes': hidden_layer_size_range, 'activation': ['identity', 'logistic', 'tanh', 'relu'],
     'solver': ['lbfgs', 'sgd', 'adam'], 'learning_rate': ['constant', 'invscaling', 'adaptive']},

    # AdaBoostRegressor
    {'base_estimator': regressors_list, 'n_estimators': n_estimator_range}
]

# Create random dataset
X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                           random_state=1, n_clusters_per_class=1)

rng = np.random.RandomState(2)
X += 2 * rng.uniform(size=X.shape)
linearly_separable = (X, y)

classification_datasets_names = ['make_moons', 'make_circles', 'linearly_separable', 'iris', 'digits', 'wine']
classification_datasets = [make_moons(n_samples=10000, noise=0.3, random_state=1),
                           make_circles(n_samples=10000, noise=0.2, factor=0.5, random_state=1),
                           linearly_separable,
                           load_iris(return_X_y = True),
                           load_digits(return_X_y = True),
                           load_wine(return_X_y = True)
                           ]
regression_datasets_names = ['make_regression', 'make_sparse_uncorrelated', 'california_housing', 'boston_housing',
                             'diabetes', 'linnerud']
regression_datasets = [make_regression(n_samples=10000, n_features=100),
                       make_sparse_uncorrelated(n_samples=10000),
                       fetch_california_housing(),
                       load_boston(),
                       load_diabetes(),
                       load_linnerud()
                       ]

# iterate over datasets
dataset_num = 0
for ds_cnt, ds in enumerate(classification_datasets):
    name = classification_datasets_names[dataset_num]
    dataset_num  += 1
    print("Working on " + name + "dataset")
    # preprocess dataset, split into training and test part
    X, y = ds
    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4, random_state=420)
    X_train = preprocessing.scale(X_train)
    
    i = 0
    # iterate over classifiers
    for clf in classifiers:
        try:
            print("Working on ",  str(clf))
            grid = GridSearchCV(clf, tuned_parameters_classifiers[i], cv=3, n_jobs=-1)
            grid.fit(X_train, y_train)

            # CSV writer
            param_list = grid.cv_results_['params']
            fieldnames = list(param_list[0].keys())
            fieldnames.append('mean_fit_time')
            fieldnames.insert(0, 'algorithm_name')
            fieldnames.insert(1, 'dataset_name')
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Save params & mean fit time and compare
            mean_fit_time = grid.cv_results_['mean_fit_time']
            for param, time in zip(param_list, mean_fit_time):
                param['mean_fit_time'] = time
                param['algorithm_name'] = ALGORITHM_NAMES[i]
                param['dataset_name'] = name
                writer.writerow(param)

        except Exception as e: 
            pass
            # print(e)
        i += 1

file.close()
