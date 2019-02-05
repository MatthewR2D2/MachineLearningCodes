from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn import linear_model
import statsmodels.api as sm
import tkinter as tk

# Example Data for demo purposes
Stock_Market = {
    'Year': [2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2016, 2016, 2016, 2016, 2016, 2016,
             2016, 2016, 2016, 2016, 2016, 2016],
    'Month': [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    'Interest_Rate': [2.75, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.25, 2.25, 2.25, 2, 2, 2, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75,
                      1.75, 1.75, 1.75, 1.75, 1.75],
    'Unemployment_Rate': [5.3, 5.3, 5.3, 5.3, 5.4, 5.6, 5.5, 5.5, 5.5, 5.6, 5.7, 5.9, 6, 5.9, 5.8, 6.1, 6.2, 6.1, 6.1,
                          6.1, 5.9, 6.2, 6.2, 6.1],
    'Stock_Index_Price': [1464, 1394, 1357, 1293, 1256, 1254, 1234, 1195, 1159, 1167, 1130, 1075, 1047, 965, 943, 958,
                          971, 949, 884, 866, 876, 822, 704, 719]
}

# Add data into the dataframe for ease of analysis
df = DataFrame(Stock_Market, columns=['Year', 'Month', 'Interest_Rate', 'Unemployment_Rate', 'Stock_Index_Price'])

# Plot stock prices over time
plt.scatter(df['Month'], df['Stock_Index_Price'], color='blue')
plt.title('Stock Prices for Each Year')
plt.xlabel("Year", fontsize=14)
plt.ylabel("Stock Price", fontsize=14)
plt.grid(True)

plt.savefig("Month_to_Price.png")
plt.show()

# Perform Linear check
# Check if there is a relation between Stock Price (dep) and Interest rate (Indep)
plt.scatter(df['Interest_Rate'], df['Stock_Index_Price'], color='red')
plt.title('Stock Index Price Vs Interest Rate', fontsize=14)
plt.xlabel('Interest Rate', fontsize=14)
plt.ylabel('Stock Index Price', fontsize=14)
plt.grid(True)
# plt.show()
plt.savefig("InterestRate_to_Price.png")
plt.show()

# Check to see if there is a relationship between Stock Price and Unemployment rate

plt.scatter(df['Unemployment_Rate'], df['Stock_Index_Price'], color='green')
plt.title('Stock Index Price Vs Unemployment Rate', fontsize=14)
plt.xlabel('Unemployment Rate', fontsize=14)
plt.ylabel('Stock Index Price', fontsize=14)
plt.grid(True)
# plt.show()
plt.savefig("UnemploymentRate_to_Price.png")
plt.show()

# Now preform the multiple regression
# here we have 2 variables for multiple regression.
# If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.
# Alternatively, you may add additional variables within the brackets
# Define X training data and Y label data,

X = df[['Interest_Rate','Unemployment_Rate']]
Y = df['Stock_Index_Price']

# Training the ML model
# Define a linear regression model
linearModel = linear_model.LinearRegression()
linearModel.fit(X, Y)

# Print out the interception and the coefficients
# The output can be used to build the linear regression model
print("Use these values to build a multiple regression model")
print("Intercept: \n", linearModel.intercept_)
print("Coefficients: \n", linearModel.coef_)

# After training then we can perform new predictions based on the model
# Use these variables to perform a test prediction.
newInterestRate = 2.75
newUnemploymentRate = 5.3

# Preform new prediction of the stock price by using the model
print('Predicted Stock Index Price: \n', linearModel.predict([[newInterestRate, newUnemploymentRate]]))

# now use Statsmodel for analysis and review of the model performance
# This is not ML but pure statistical method/calculation
X = sm.add_constant(X)  # Add the constant (Test data from above)

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

# This displays the comprehensive table with statistical information generated by statsmodels
# This can used to build models and find relationships between variables (independ/depend)
# This can be used to check the ML model results
print_model = model.summary()
print(print_model)

# Build a simple GUI to allow user input
root = tk.Tk()
canvas1 = tk.Canvas(root, width=1200, height=450)
canvas1.pack()

# SKLearn
# Add the intercept to the GUI
interceptResults = ("Intercept:", linearModel.intercept_)
labelIntercept = tk.Label(root, text=interceptResults, justify='center')
canvas1.create_window(260, 220, window=labelIntercept)

# Add the coefficients
coefficientsResult = ("Coefficients: ", linearModel.coef_)
labelCoefficients = tk.Label(root, text=coefficientsResult, justify='center')
canvas1.create_window(260, 240, window=labelCoefficients)

# add statsmodels results to the GUI
# Use the print_model from before here
label_model = tk.Label(root, text=print_model, justify='center', relief='solid', bg='LightSkyBlue1')
canvas1.create_window(800, 220, window=label_model)

# Add in the input boxes for user to input new information for testing/prediction

# New_Interest_Rate label and input box
label1 = tk.Label(root, text='Type Interest Rate: ')
canvas1.create_window(100, 100, window=label1)

entry1 = tk.Entry(root)  # create 1st entry box
canvas1.create_window(270, 100, window=entry1)

# New_Unemployment_Rate label and input box
label2 = tk.Label(root, text=' Type Unemployment Rate: ')
canvas1.create_window(120, 120, window=label2)

entry2 = tk.Entry(root)  # create 2nd entry box
canvas1.create_window(270, 120, window=entry2)


# Method for doing the calculation to make predictions
def values():
    # First input variable
    global New_Interest_Rate
    New_Interest_Rate = float(entry1.get())
    # Second Input value/varialbe
    global New_Unemployment_Rate
    New_Unemployment_Rate = float(entry2.get())

    Prediction_Result = (
        'Predicted Stock Index Price: ', linearModel.predict([[New_Interest_Rate, New_Unemployment_Rate]]))

    label_Prediction = tk.Label(root, text=Prediction_Result, bg='orange')
    canvas1.create_window(260, 280, window=label_Prediction)


# button to call the 'values' command above
button1 = tk.Button(root, text='Predict Stock Index Price', command=values, bg='orange')
canvas1.create_window(270, 150, window=button1)

root.mainloop()