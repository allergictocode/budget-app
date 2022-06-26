class Category:
  
    def __init__(self, name):
      self.name = name
      self.ledger = []

    def __str__(self):
      line = f"{self.name:*^30}\n"
      items = ""
      for item in self.ledger:
          description = "{:<23}".format(item["description"])
          amount = "{:>7.2f}".format(item["amount"])
          items += "{}{}\n".format(description[:23], amount[:7])
      total = f"Total: {self.get_balance():.2f}"
      return line + items + total

    def deposit(self, amount, description = ""):
      self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = ""):
      if self.check_funds(amount):
        self.ledger.append({"amount": -amount, "description": description})
        return True
      else:
        return False

    def get_balance(self):
      balance = 0
      for item in self.ledger:
        balance += item["amount"]
      return balance

    def transfer(self, amount, instance_cat):
      if self.check_funds(amount):
        self.withdraw(amount, f"Transfer to {instance_cat.name}")
        instance_cat.deposit(amount, f"Transfer from {self.name}")
        return True
      else:
        return False

    def check_funds(self, amount):
      if amount <= self.get_balance():
        return True
      else:
        return False


def create_spend_chart(categories):
  # spent in each category and category name
  spent = []
  cat_name = []
  for category in categories:
    total = 0
    for item in category.ledger:
      money = item["amount"]
      if money < 0:
        total += abs(money)
    spent.append(round(total, 2))
    cat_name.append(category.name)

  # percentage of spent in each category
  percentage = []
  for n in spent:
    percentage.append(round((n/sum(spent) * 100), 2))
    
  # bar chart
  chart = "Percentage spent by category\n"
  for number in range(100, -10, -10):
    chart += f"{number:>3}| "
    for percent in percentage:
      if percent >= number:
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"

  chart += "    " + "-"*3*len(cat_name) + "-"
  chart += "\n     "

  length = 0
  for name in cat_name:
    if len(name) > length:
      length = len(name)

  for n in range(length):
    for name in cat_name:
      if n < len(name):
        chart += name[n] + "  "
      else:
        chart += "   "
    if length-1 > n:
      chart += "\n     "
    
  return chart