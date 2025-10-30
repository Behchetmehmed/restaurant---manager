from project.waiters_app import RestaurantManagement
restaurant = RestaurantManagement()
all_actions = {
    1: restaurant.register_waiter,
    2: restaurant.list_waiters,
    3: restaurant.unregister_waiter,
    4: restaurant.create_table,
    5: restaurant.assign_waiter_to_a_table,
    6: restaurant.list_free_tables,
    7: restaurant.list_active_tables,
    8: restaurant.show_menu,
    9: restaurant.get_product_by_code,
    10: restaurant.take_order,
    11: restaurant.show_table_orders,
    12: restaurant.remove_item_from_order,
    13: restaurant.close_table_bill,
    14: restaurant.daily_summary,
    15: exit
}


def show_menu():
    menu = [
        "\n",
        "1. Register waiter",
        "2. List waiters",
        "3. Unregister waiter",
        "4. Create Table",
        "5. Assign waiter to a table",
        "6. List free tables",
        "7. List active tables",
        "8. Show menu",
        "9. Get product by code",
        "10. Take order",
        "11. Show table orders",
        "12. Remove item from order",
        "13. Close table bill",
        "14. Daily summary",
        "15. Exit"
    ]
    print('\n'.join(menu))

    try:
        choice = int(input("\nPlease enter a choice (1–15): "))
    except ValueError:
        return None  # Invalid input

    return choice


while True:
    user_choice = show_menu()  # Store the user's choice
    if user_choice is None:
        print("Invalid input! Please enter a number.")
        continue

    if user_choice in all_actions:
        all_actions[user_choice]()  # Call the selected function
    else:
        print("Invalid choice! Please enter a number between 1 and 15.")