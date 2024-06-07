import tkinter as tk
import requests

API_KEY = "5R3OWBXYR8K18YIB"

class Stock:
    def __init__(self, symbol, quantity):
        self.symbol = symbol
        self.quantity = quantity
        self.current_price = None

    def update_price(self):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        try:
            self.current_price = float(data["Global Quote"]["05. price"])
        except KeyError:
            self.current_price = None

class Portfolio:
    def __init__(self):
        self.stocks = []

    def add_stock(self, stock):
        self.stocks.append(stock)

    def remove_stock(self, symbol):
        for i, stock in enumerate(self.stocks):
            if stock.symbol == symbol.upper():
                del self.stocks[i]
                return
        raise ValueError(f"Stock {symbol} not found in portfolio")

    def update_prices(self):
        for stock in self.stocks:
            stock.update_price()

    def get_total_value(self):
        total = 0
        for stock in self.stocks:
            if stock.current_price:
                total += stock.quantity * stock.current_price
        return total

    def display_portfolio(self):
        portfolio_text = "Symbol\tQuantity\tCurrent Price\n"
        for stock in self.stocks:
            if stock.current_price is not None:
                portfolio_text += f"{stock.symbol}\t{stock.quantity}\t{stock.current_price:.2f}\n"
            else:
                portfolio_text += f"{stock.symbol}\t{stock.quantity}\tN/A\n"
        portfolio_text += f"\nTotal Value: {self.get_total_value():.2f}"
        return portfolio_text

def main():
    window = tk.Tk()
    window.title("Stock Portfolio")

    portfolio = Portfolio()

    symbol_label = tk.Label(window, text="Stock Symbol:")
    symbol_label.pack()

    symbol_entry = tk.Entry(window)
    symbol_entry.pack()

    quantity_label = tk.Label(window, text="Quantity:")
    quantity_label.pack()

    quantity_entry = tk.Entry(window)
    quantity_entry.pack()

    def add_stock():
        symbol = symbol_entry.get().upper()
        try:
            quantity = int(quantity_entry.get())
            portfolio.add_stock(Stock(symbol, quantity))
            update_portfolio_text()
            symbol_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            error_label.config(text="")
        except ValueError:
            error_label.config(text="Invalid quantity. Please enter a number.")

    add_stock_button = tk.Button(window, text="Add Stock", command=add_stock)
    add_stock_button.pack()

    def remove_stock():
        symbol = symbol_entry.get().upper()
        try:
            portfolio.remove_stock(symbol)
            update_portfolio_text()
            symbol_entry.delete(0, tk.END)
            error_label.config(text="")
        except ValueError as e:
            error_label.config(text=str(e))

    remove_stock_button = tk.Button(window, text="Remove Stock", command=remove_stock)
    remove_stock_button.pack()

    def update_prices():
        portfolio.update_prices()
        update_portfolio_text()

    update_prices_button = tk.Button(window, text="Update Prices", command=update_prices)
    update_prices_button.pack()

    portfolio_text_area = tk.Text(window, height=10, width=50, state="disabled")
    portfolio_text_area.pack()


    error_label = tk.Label(window, text="")
    error_label.pack()

    def update_portfolio_text():
        portfolio_text_area.config(state="normal")
        portfolio_text_area.delete(1.0, tk.END)
        portfolio_text_area.insert(tk.INSERT, portfolio.display_portfolio())
        portfolio_text_area.config(state="disabled")

    window.mainloop()

if __name__ == "__main__":
    main()
