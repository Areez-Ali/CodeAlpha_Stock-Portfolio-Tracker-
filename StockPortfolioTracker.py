import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm

console = Console()

stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 310,
    "AMZN": 135
}

portfolio = {}

console.print(Panel.fit("📊 [bold green]Welcome to Stock Portfolio Tracker[/bold green] 📊", style="cyan"))

table = Table(title="Available Stocks", style="bold white on black")
table.add_column("Symbol", style="yellow", justify="center")
table.add_column("Company", style="cyan", justify="left")
table.add_column("Price (USD)", style="green", justify="right")

company_names = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "GOOGL": "Google",
    "MSFT": "Microsoft",
    "AMZN": "Amazon"
}

for stock, price in stock_prices.items():
    table.add_row(stock, company_names[stock], f"${price}")

console.print(table)
console.print("[italic grey50]Type 'done' when finished adding stocks.[/italic grey50]\n")

while True:
    stock_name = Prompt.ask("🔎 Enter stock symbol").upper()

    if stock_name == "DONE":
        break

    if stock_name not in stock_prices:
        console.print("❌ [red]Stock not found in our list. Try again.[/red]")
        continue
    try:
        qty = IntPrompt.ask(f"📦 Enter quantity of [yellow]{stock_name}[/yellow]")
    except ValueError:
        console.print("⚠️ [orange1]Please enter a valid number.[/orange1]")
        continue

    portfolio[stock_name] = portfolio.get(stock_name, 0) + qty

summary_table = Table(title="📈 Portfolio Summary 📈", style="bold white on black")
summary_table.add_column("Stock", style="yellow", justify="center")
summary_table.add_column("Quantity", justify="center", style="cyan")
summary_table.add_column("Price", justify="right", style="green")
summary_table.add_column("Value", justify="right", style="bold green")

total_value = 0
for stock, qty in portfolio.items():
    price = stock_prices[stock]
    value = qty * price
    total_value += value
    summary_table.add_row(stock, str(qty), f"${price}", f"${value}")

summary_table.add_row("TOTAL", "", "", f"[bold green]${total_value}[/bold green]")

console.print(summary_table)

if Confirm.ask("💾 Do you want to save portfolio to CSV file?"):
    filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Value"])
        for stock, qty in portfolio.items():
            writer.writerow([stock, qty, stock_prices[stock], qty * stock_prices[stock]])
        writer.writerow(["TOTAL", "", "", total_value])
    console.print(f"✅ [bold green]Portfolio saved as {filename}[/bold green]")
else:
    console.print("⚡ [cyan]File not saved. Program ended.[/cyan]")