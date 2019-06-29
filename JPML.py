#MACHINE LEARNING YAY
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
class KNN:
    def __init__(self, X, y):
        
        self.regressor = KNeighborsRegressor(n_neighbors=5, weights='distance')

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=42)

        self.regressor.fit(self.X_train, self.y_train)


        #create regeressor 
    def predict(self, unknown):
        return int(self.regressor.predict(unknown))

    def score(self):
        return self.regressor.score(self.X_test,self.y_test)

        
