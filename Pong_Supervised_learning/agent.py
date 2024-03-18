from sklearn.tree import DecisionTreeClassifier
import pickle

class Agent():
    def __init__(self):
        self.model = DecisionTreeClassifier()
    
    def train(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def save_model(self, path):
        arquivo_modelo_arvore = open(path, 'wb')
        pickle.dump(self.model, arquivo_modelo_arvore)
        arquivo_modelo_arvore.close()
        
    def load_model(self, path):
        arquivo_modelo_arvore = open(path, 'rb')
        self.model = pickle.load(arquivo_modelo_arvore)