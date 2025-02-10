from random import randint
import sys

def main():
    game = Game()  # Start a new game

    # Main game loop
    while True:
        choice = game.show_menu()  # Open the menu
        continue_game = game.handle_choice(choice)  # Game handling will decide on the input of the choice if 7 then it will not continue

        if not continue_game:  # Typing 7 will end game
            break


def reputation_reader(store):
    """Adjust reputation based on cleanliness."""
    if store.cleanliness > 70 and all(item.stock > 0 for item in store.inventory):
        store.reputation += 5
        print(f"Your reputation is at {store.reputation}. It increased by 5 today.")
    else:
        store.reputation -= 15
        print(f"Your reputation is low at {store.reputation}. It decreased by 15 today.")


def random_event(store):
    random_event_chance = randint(0, 100)  # Chance for a random event

    if 0 <= random_event_chance <= 20:  # 20% chance for a random event
        print("A random event has occurred!")

        # Pick one of several possible events
        random_event_picker = randint(0, 7)  # Range for more events if needed

        if random_event_picker == 0:
            # Event: A surprise sale
            print("A surprise sale boosts your sales for the day!")
            sales_boost = randint(50, 200)  # Boost to sales
            store.sales += sales_boost
            store.budget += sales_boost
            print(f"Sales boosted by ${sales_boost}. Total sales for the day: ${store.sales}")

        elif random_event_picker == 1:
            # Event: Stock shortage
            print("A supplier has failed to deliver, causing a stock shortage!")
            stock_issue = randint(1, len(store.inventory) - 1)
            item_out_of_stock = store.inventory[stock_issue]
            item_out_of_stock.stock = 0  # The item runs out of stock
            print(f"{item_out_of_stock.name} is now out of stock. This will affect your reputation!")
            store.reputation -= 10

        elif random_event_picker == 2:
            # Event: A celebrity visit
            print("The Impractical Jokers visited your store, causing a massive influx of customers!")
            customers_brought = randint(20, 50)
            store.customers += customers_brought
            print(f"Customer count increased by {customers_brought} for the day. Total customers: {store.customers}")

        elif random_event_picker == 3:
            # Event: A store inspection
            print("A surprise inspection by health authorities!")
            cleanliness_penalty = randint(5, 20)
            store.cleanliness -= cleanliness_penalty
            print(f"Cleanliness decreased by {cleanliness_penalty}. Current cleanliness: {store.cleanliness}")

        elif random_event_picker == 4:
            # Event: A promotional campaign
            print("A successful promotional campaign brings in more customers!")
            additional_customers = randint(10, 30)
            store.customers += additional_customers
            print(f"Customers increased by {additional_customers} for the day. Total customers: {store.customers}")

        elif random_event_picker == 5:
            # Event: A sale on a popular item
            print("One of your items is on sale, and customers are flocking to buy it!")
            sale_item = store.inventory[randint(0, len(store.inventory) - 1)]
            sale_quantity = randint(5, 20)
            print(f"Customers are buying {sale_quantity} {sale_item.name}s today!")
            sale_item.stock -= sale_quantity
            earned_money = sale_quantity * sale_item.price
            store.sales += earned_money
            store.budget += earned_money
            print(f"Sales from this sale: ${earned_money}. Updated sales: ${store.sales}")

        elif random_event_picker == 6:
            #Event: Unexpected fire
            print("An unexpected fire broke out in your store, damaging stock and causing temporary closure!")
            fire_damage = randint(100, 300)  # Loss due to fire
            store.budget -= fire_damage
            print(f"You lost ${fire_damage} due to fire damage. Budget decreased to ${store.budget}")
            store.reputation -= 20  # Reputation drop due to the fire
            print("Your reputation decreased by 20 due to the fire.")

        elif random_event_picker == 7:
            # Event: Customer complaint
            print("A customer has filed a formal complaint about your store!")
            complaint_penalty = randint(10, 30)
            store.reputation -= complaint_penalty
            print(f"Your reputation decreased by {complaint_penalty} due to the complaint.")
            lost_customers = randint(5, 15)
            store.customers -= lost_customers
            print(f"You lost {lost_customers} customers due to the complaint. Total customers: {store.customers}")

    else:
        print("No random event occurred today.")


def simulate_day(store):
    """Simulate a day where customers buy items."""
    store.customers = randint(1, 100)  # Random number of customers
    store.sales = 0

    for item in store.inventory:
        customers_buying = randint(0, store.customers)  # Random number of customers buying the item
        money_earned = item.sell(customers_buying)  # Earn money from sales
        store.sales += money_earned
        store.budget += money_earned

        # If stock runs out, reputation decreases
        if item.stock == 0:
            store.reputation -= 10
            print(f"{item.name} is out of stock. Your reputation decreased by 5.")

    reputation_reader(store)
    random_event(store)
    store.days_active += 1
    store.total_sales += store.sales
    store.check_if_game_over()


class Item:
    def __init__(self, name, price, stock):  # Each item will have a name, price, and stock amount
        self.name = name
        self.price = price
        self.stock = stock

    def sell(self, quantity):
        """Sell a specified quantity of this item."""
        if self.stock >= quantity:  # Check that we have stock
            self.stock -= quantity
            return self.price * quantity  # When we sell we will return how much we make
        else:
            return 0  # Not enough stock

    def buy_stock(self, money_open, quantity):
        """Handle the purchase of stock if the player has enough money."""
        total_cost = self.price * quantity
        print(f"It will cost you {total_cost} for {quantity} {self.name}.")  # We need to calc total cost and then we will add to that stock if we have money

        if money_open >= total_cost:
            self.stock += quantity
            money_open -= total_cost
            print(f"You have bought {quantity} of {self.name}. You have {money_open} left.")
        else:
            print(f"You do not have enough to purchase {quantity} {self.name}.")

        return money_open, self.stock


class Store:
    def __init__(self, customers):
        self.cleanliness = 100
        self.reputation = 100
        self.inventory = []
        self.sales = 0
        self.budget = 150
        self.customers = customers
        self.days_active = 0
        self.total_sales = 0

    # Getter for reputation
    @property
    def reputation(self):
        return self._reputation

    # Setter for reputation with limit
    @reputation.setter
    def reputation(self, value):
        # Enforce the reputation limit between 0 and 100
        if value > 100:
            self._reputation = 100
        elif value < 0:
            self._reputation = 0
        else:
            self._reputation = value

    def clean_store(self):  # Reset the store cleaning to 100!
        """Clean the store and reset cleanliness."""
        self.cleanliness = 100
        print("You cleaned the store!")
        return self.cleanliness

    def progress_report(self):  # Our game progress report with quick details
        """Report on store's overall progress."""
        print(f"\nDays Active: {self.days_active}")
        print(f"Total Sales: ${self.total_sales}")
        print(f"Store Reputation: {self.reputation}")
        print(f"Cleanliness: {self.cleanliness}")
        print(f"Remaining Budget: ${self.budget}")

    def check_if_game_over(self):  # We will check if any of our variables for our object violate what consitutes a game over
        if self.cleanliness <= 0:
            sys.exit("The Health Inspector has shut down your store!")
        if self.budget <= 0:
            sys.exit("You are bankrupt and your store is closed!")

        if all(item.stock == 0 for item in self.inventory):
            sys.exit("Your inventory is empty, and customers cannot buy anything! Game over.")

        if self.reputation <= 0:
            sys.exit("Your reputation is ruined! No customers are coming to your store. Game over.")

    def print_status(self):
        """Print the store's status including sales, reputation, and available funds."""
        print(f"\nStore Reputation: {self.reputation}")
        print(f"Store Cleanliness: {self.cleanliness}")
        print(f"Daily Sales: ${self.sales}")
        print(f"Number of Customers: {self.customers}")
        print(f"Available Budget: ${self.budget}\n")

    def add_item(self, item):
        """Add an item to the store's inventory."""
        self.inventory.append(item)

    def buy_items(self, item_name, quantity_to_buy):
        """Buy items and add them to the inventory."""
        item_found = False
        for item in self.inventory:
            if item.name == item_name:
                self.budget, item.stock = item.buy_stock(self.budget, quantity_to_buy)
                item_found = True
                break

        # If the item doesn't exist, add a new item to the inventory
        if not item_found:
            print(f"{item_name} is not in the inventory. Adding a new item to inventory.")
            while True:
                try:
                    price = float(input(f"Enter the price for {item_name}: "))
                except ValueError:
                    print("You must enter a float!")
            new_item = Item(item_name, price, 0)
            self.budget, new_item.stock = new_item.buy_stock(self.budget, quantity_to_buy)
            self.add_item(new_item)


class Game:
    def __init__(self):
        self.store = Store(customers=50)  # Initialize store with a default number of customers
        self.day = 1

        # Initialize the store with some items
        apple = Item("Apple", 1.0, 100)
        banana = Item("Banana", 0.5, 100)
        milk = Item("Milk", 2.5, 100)
        bread = Item("Bread", 1.5, 100)

        self.store.add_item(apple)
        self.store.add_item(banana)
        self.store.add_item(milk)
        self.store.add_item(bread)

    def show_inventory(self):
        for item in self.store.inventory:
            print(f"\n{item.name}: ${item.price} (Stock: {item.stock})")

    def show_menu(self):
        """Display a menu of options for the player."""
        print("\n--- Main Menu ---")
        print("1. Simulate a Day")
        print("2. Buy Items")
        print("3. Clean the Store")
        print("4. View Store Status")
        print("5. Show Inventory")
        print("6. Show Progress")
        print("7. Quit Game")
        choice = input("Choose an option (1-7): ").strip()

        return choice

    def handle_choice(self, choice):
        """Handle the player's choice from the menu."""
        if choice == '1':
            self.start_day()
        elif choice == '2':
            self.buy_items()
        elif choice == '3':
            self.store.clean_store()
        elif choice == '4':
            self.store.print_status()
        elif choice == '5':
            self.show_inventory()
        elif choice == '6':
            self.store.progress_report()
        elif choice == '7':
            print("Exiting the game. Goodbye!")
            self.store.progress_report()
            return False
        else:
            print("Invalid choice. Please try again.")

        return True

    def start_day(self):
        """Simulate the day's activities."""
        print(f"\nDay {self.day} begins!")
        simulate_day(self.store)  # Simulate the store's operations for the day
        self.day += 1
        self.store.cleanliness -= 25

    def buy_items(self):
        """Allow the player to buy items to restock."""
        print("\nAvailable items to restock:")
        self.show_inventory()  # Display available inventory items

        while True:
            try:
                # Ask the player which item they want to buy
                item_name = input("Enter the item you want to buy or type 'quit' to return to the menu: ").strip().capitalize()

                # Check if the user wants to quit and return to the menu
                if item_name.lower() == 'quit':
                    print("Returning to the menu.")
                    break  # Break out of the loop to return to the menu

                # Ask for the quantity of the item they want to buy
                quantity_to_buy = int(input(f"How many {item_name}s would you like to buy? ").strip())

                # Make sure quantity is a valid number (greater than 0)
                if quantity_to_buy <= 0:
                    print("Please enter a quantity greater than 0.")
                    continue

            except ValueError:
                print("Invalid input! Please enter a valid number for the quantity.")
                continue  # Reprompt the user for input if a ValueError occurs

            # If item_name is valid, proceed to the store's buy_items method
            self.store.buy_items(item_name, quantity_to_buy)

            # After completing the transaction, ask if they want to continue buying or quit
            continue_shopping = input("Do you want to buy another item? (y/n): ").strip().lower()
            if continue_shopping != 'y':
                print("Returning to the menu.")
                break  # Exit the loop and return to the menu


if __name__ == "__main__":
    main()
