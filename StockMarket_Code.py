import os.path as path
import yfinance as yf
import matplotlib.pyplot as plt

#import datetime as t

FILE_NAME = "portfolio.txt"
Receipts = []

def getCurrentPortfolio():
    file_exists = path.isfile(FILE_NAME)
    
    stocks = {}
    # {"GOOG": 2, "AAPL": 3, "FACEBOOK": 2}
    if file_exists == False:
        balance = 100000
    else:
        port_file = open(FILE_NAME, 'r')
        for line in port_file:
            line_array = line.split()
            if line_array[0] == "balance:":
                balance = float(line_array[1])
            
            if line_array[0] == "stocks:":
                for i in range(1, len(line_array)):
                    stock = line_array[i]
                    
                    stock_data = stock.split(',')
                    ticker = stock_data[0]
                    num_shares = int(stock_data[1])
                    
                    stocks[ticker] = num_shares
        
        port_file.close()
    
    return balance, stocks

def saveCurrentPortfolio(balance, stocks):
    port_file = open(FILE_NAME, 'w+')
    port_file.write("balance: " + str(balance) + '\n')
    port_file.write("stocks: ")
    
    for key in stocks.keys():
        num_shares = stocks[key]
        port_file.write(key + "," + str(num_shares) + " ")
        
        
    
    port_file.close()
    
def buyStock(ticker, num_shares):
    balance, stocks = getCurrentPortfolio()
    stock_wanted = yf.Ticker(ticker)
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    
    receipt = ""
    receipt = str(num_shares) + " shares of " + ticker + " at a price of $" + str(current_price) + " for a total purchase of $" + str(num_shares* current_price)
    Receipts.append(receipt) 
    
    total_cost = current_price * num_shares
    if total_cost > balance:
        print("Sorry you do not have enough money! ")
        money_needed = total_cost - balance 
        print("You need $" + str(money_needed) + " more")
        return balance, stocks

    balance -= total_cost
    if ticker in stocks:
        stocks[ticker] += num_shares
    else:
        stocks[ticker] = num_shares
    
    return balance, stocks

    
def sellStock(ticker, num_shares):
    balance, stocks = getCurrentPortfolio()
    
    if ticker not in stocks:
        print("Sorry you do not have this stock!")
        return balance, stocks
    
    if stocks[ticker] < num_shares:         #stocks[ticker] gets number of stocks
        print("Sorry you do not have that many shares!")
        return balance, stocks
        
    stock_wanted = yf.Ticker(ticker)    #gets YF version of stocks
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    
    total_cost = current_price * num_shares
    stocks[ticker] -= num_shares
    
    balance += total_cost
    return balance, stocks


    


balance, stocks = getCurrentPortfolio()

while True:
    user_input = input("What would you like to do (Buy/Sell/Show/Quit/Search/Receipt) ")
    user_input = user_input.lower()
    if user_input == "quit":
        saveCurrentPortfolio(balance, stocks)
        break
    elif user_input == "buy":
        ticker = input("Enter in what stock you want:")
        num_shares = int(input("Enter in how many shares:"))
        balance, stocks = buyStock(ticker, num_shares)
        saveCurrentPortfolio(balance, stocks)
        
    elif user_input == "sell":
        ticker = input("Enter in what stock you want to sell:")
        num_shares = int(input("Enter in how many shares:"))
        balance, stocks = sellStock(ticker, num_shares)
        saveCurrentPortfolio(balance, stocks)
        
    elif user_input == "show":
        print("Your current balance is $" + str(balance))
        print("Your current stocks: " + str(stocks))
        Total_Portfolio_Value = 0
        for key in stocks.keys():
            stock_wanted = yf.Ticker(key)
            current_price = stock_wanted.history(period = "5d")["Close"][-1]  #5d is 5 day period, close -1 is the closing price 1 day ago
        Total_Portfolio_Value += balance
        print("Your total portfolio value is " + str(Total_Portfolio_Value))
    

       
    elif user_input == "search":
        ticker = input("Enter in what stock you want to search: ")
        stock_wanted = yf.Ticker(ticker)
        #import calendar
	    #my_date = my_date.strftime('%A')
        x_values = []
        y_values = []
        for i in range(0, 5):
            current_price = stock_wanted.history(period="5d")["Close"][i]
            x_values.append(1+i)
            y_values.append(current_price)
        plt.plot(x_values, y_values)
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.title("Last Five Days")
        plt.show()
        
    elif user_input == "receipt":
        print(Receipts)
   
    else:
        print("Choose a valid instruction!")