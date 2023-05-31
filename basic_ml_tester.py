from sklearn.linear_model import LinearRegression
import numpy as np

def fit(points):
    points = np.array(points)  # convert list of tuples to numpy array
    print(f"Points shape: {points.shape}")  # print shape of points
    X = points[:, 0].reshape(-1, 1)  # reshape for sklearn
    y = points[:, 1]
    
    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    intercept = model.intercept_

    return slope, intercept
