import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump
from sklearn.metrics import mean_squared_error
df = pd.read_csv("E:/generation_facility_data/new_csv/data_augmentation.csv")
# Extract features and target variables
features = df[['numbers', 'Power_Per_unit']]
target = df['Total_emissions']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=40)

X_train = X_train.dropna()
y_train = y_train.dropna()

X_train = X_train.sort_index()
y_train = y_train.sort_index()
df = df[df['Total_emissions'] != 0]

import numpy as np
from sklearn.model_selection import RandomizedSearchCV
n_estimators=[int(x) for x in np.linspace(20,200,10)]
max_features=['auto','sqrt']
max_depth=[10,20,None]
bootstrap=[True,False]
min_samples_split=[2,6,10,12]
min_samples_leaf=[2,4,6]


random_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth,
               'max_features': max_features,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


rf=RandomForestRegressor()
#用随机搜索来优化RandomForestRegressor
rf_random=RandomizedSearchCV(estimator=rf, param_distributions=random_grid,n_iter=10,scoring='neg_mean_absolute_error',cv=3,random_state=40)

rf_random.fit(X_train,y_train)

rf_random.best_params_#The optimal parameters are obtained and the grid search is adjusted on this basis


#获得最优模型
rf_estimator=rf_random.best_estimator_
rf_accuracy = rf_estimator.score(X_test,y_test)
print("Accuracy is :",rf_accuracy)
print(rf_random.best_params_)

from sklearn.model_selection import GridSearchCV
n_estimators=[140,150,160]
min_samples_split=[11,12,13]
min_samples_leaf=[3,4,5]
max_features=['sqrt']
max_depth=[None]
bootstrap=[True]

param_first_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


grid_first_search=GridSearchCV(estimator=rf, param_grid=param_first_grid,
                               scoring='neg_mean_absolute_error',cv=3)

grid_first_search.fit(X_train,y_train)
grid_first_search.best_params_
print('First grid search adjustment')
best_grid_search=grid_first_search.best_estimator_
rf_accuracy = best_grid_search.score(X_test,y_test)
print("Accuracy is :",rf_accuracy)
print(grid_first_search.best_params_)

n_estimators=[110,115,120]
min_samples_split=[1,2]
min_samples_leaf=[2,3,4]
max_features=['sqrt']
max_depth=[None]
bootstrap=[True]

param_final_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


grid_final_search=GridSearchCV(estimator=rf, param_grid=param_final_grid,
                               scoring='neg_mean_absolute_error',cv=3)

grid_final_search.fit(X_train,y_train)
grid_final_search.best_params_
print('Final grid search adjustment')
best_grid_search=grid_final_search.best_estimator_
rf_accuracy = best_grid_search.score(X_test,y_test)
print("Accuracy of the model in the test set is :",rf_accuracy)
print(grid_final_search.best_params_)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 使用训练好的模型对测试集进行预测
y_pred = best_grid_search.predict(X_test)

# 计算均方根误差
rmse = mean_squared_error(y_test, y_pred, squared=False)

# 计算平均绝对误差
mae = mean_absolute_error(y_test, y_pred)

# 计算决定系数
r2 = r2_score(y_test, y_pred)

print("Root mean square error（RMSE）:", rmse)
print("Mean absolute error（MSE）:", mae)
print("Coefficient of determination（R^2 Score）:", r2)

rf_accuracy = best_grid_search.score(X_test,y_test)
print("Accuracy of the model in the test set is :",rf_accuracy)

rf_accuracy = best_grid_search.score(X_train,y_train)
print("Accuracy of the model in the train set is :",rf_accuracy)

dump(best_grid_search, 'trained_model.joblib')
