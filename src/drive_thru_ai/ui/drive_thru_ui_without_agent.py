import streamlit as st
from drive_thru_ai.menu import *


def get_drink_customization(key_prefix=""):
    """Helper function to get drink customization options"""
    drink_type = st.selectbox(
        "Drink Type",
        [dt.value for dt in DrinkType],
        key=f"{key_prefix}drink_type"
    )
    if drink_type == DrinkType.FOUNTAIN.value:
        flavor = st.selectbox(
            "Flavor",
            [ff.value for ff in FountainFlavor],
            key=f"{key_prefix}fountain_flavor"
        )
    else:
        flavor = st.selectbox(
            "Flavor",
            [mf.value for mf in MilkshakeFlavor],
            key=f"{key_prefix}milkshake_flavor"
        )
    return drink_type, flavor


def show_drive_thru_ui():
    st.set_page_config(page_title="Drive-Thru Order Tracker", layout="wide")

    # Initialize session state for order if it doesn't exist
    if 'current_order' not in st.session_state:
        st.session_state.current_order = Order()
    if 'order_status' not in st.session_state:
        st.session_state.order_status = "Waiting for customer..."
    if 'order_history' not in st.session_state:
        st.session_state.order_history = []

    # Title and status
    st.title("Drive-Thru Order Tracker")
    status_col1, status_col2 = st.columns([3, 1])

    with status_col1:
        st.subheader("Current Status")
        st.write(st.session_state.order_status)

    with status_col2:
        if st.button("Start New Order"):
            st.session_state.current_order = Order()
            st.session_state.order_status = "Waiting for customer..."
            st.session_state.order_history = []
            st.rerun()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Current Order")
        if st.session_state.current_order.get_number_of_items() == 0:
            st.write("No items in current order")
        else:
            st.write(st.session_state.current_order.get_order_summary())

            # Show items by type
            items_by_type = st.session_state.current_order.get_items_by_type()
            for item_type, items in items_by_type.items():
                with st.expander(f"{item_type}s ({len(items)})"):
                    for i, item in enumerate(items):
                        st.write(
                            f"- {item.get_name()}: ${item.get_price():.2f}")
                        st.write(f"  {item.get_description()}")
                        if st.button("Remove", key=f"remove_{item_type}_{i}"):
                            st.session_state.current_order.remove_item(i)
                            st.session_state.order_history.append(
                                f"Removed {item.get_name()}: ${item.get_price():.2f}")
                            st.rerun()

    with col2:
        st.subheader("Quick Actions")

        # Burger Customization
        st.subheader("Burger Options")
        burger_price = st.number_input(
            "Base Price", value=5.99, min_value=0.0, step=0.01, key="standalone_burger_price")

        # Ingredient customization in expander
        with st.expander("Customize Ingredients", expanded=False):
            ingredients = {
                "patty": "Patty",
                "cheese": "Cheese",
                "lettuce": "Lettuce",
                "tomato": "Tomato",
                "onion": "Onion",
                "pickles": "Pickles",
                "sauce": "Sauce"
            }

            ingredient_amounts = {}
            for key, label in ingredients.items():
                ingredient_amounts[key] = st.selectbox(
                    label,
                    [amount.value for amount in IngredientAmount],
                    index=2,
                    key=f"standalone_burger_{key}"
                )

        if st.button("Add Customized Burger"):
            burger = Burger(burger_price)
            for ingredient, amount in ingredient_amounts.items():
                burger.set_ingredient(ingredient, IngredientAmount(amount))

            st.session_state.current_order.add_item(burger)
            st.session_state.order_history.append(
                f"Added {burger.get_name()}: ${burger.get_price():.2f}")
            st.rerun()

        st.divider()

        # Add Nuggets
        st.subheader("Nuggets")
        nugget_count = st.selectbox(
            "Nugget Count", Nuggets.PIECE_COUNTS, key="standalone_nuggets")
        if st.button("Add Nuggets"):
            nuggets = Nuggets(nugget_count)
            st.session_state.current_order.add_item(nuggets)
            st.session_state.order_history.append(
                f"Added {nugget_count} Piece Nuggets: ${nuggets.get_price():.2f}")
            st.rerun()

        st.divider()

        # Add Meal
        st.subheader("Value Meals")
        meal_size = st.selectbox(
            "Meal Size", ["Medium", "Large"], key="meal_size")
        meal_type = st.selectbox(
            "Meal Type", ["Burger", "Nuggets"], key="meal_type")

        # Main item customization
        if meal_type == "Burger":
            with st.expander("Customize Burger", expanded=False):
                burger_price = st.number_input(
                    "Burger Base Price", value=5.99, min_value=0.0, step=0.01, key="meal_burger_price")
                ingredients = {
                    "patty": "Patty",
                    "cheese": "Cheese",
                    "lettuce": "Lettuce",
                    "tomato": "Tomato",
                    "onion": "Onion",
                    "pickles": "Pickles",
                    "sauce": "Sauce"
                }
                ingredient_amounts = {}
                for key, label in ingredients.items():
                    ingredient_amounts[key] = st.selectbox(
                        label,
                        [amount.value for amount in IngredientAmount],
                        index=2,
                        key=f"meal_burger_{key}"
                    )
            main_item = Burger(burger_price)
            for ingredient, amount in ingredient_amounts.items():
                main_item.set_ingredient(ingredient, IngredientAmount(amount))
        else:
            nugget_count = st.selectbox(
                "Nugget Count for Meal", Nuggets.PIECE_COUNTS, key="meal_nuggets")
            main_item = Nuggets(nugget_count)

        # Drink customization
        with st.expander("Customize Drink", expanded=False):
            drink_type, flavor = get_drink_customization("meal_")

        if st.button("Add Meal"):
            size = Size.MEDIUM if meal_size == "Medium" else Size.LARGE
            drink = Drink(
                DrinkType(drink_type),
                FountainFlavor(
                    flavor) if drink_type == DrinkType.FOUNTAIN.value else MilkshakeFlavor(flavor),
                size
            )
            fries = Fries(size)

            meal = Meal(main_item, drink, fries)
            st.session_state.current_order.add_item(meal)
            st.session_state.order_history.append(
                f"Added {meal.get_name()}: ${meal.get_price():.2f}")
            st.rerun()

        st.divider()

        # Add Drink
        st.subheader("Drinks")
        drink_type, flavor = get_drink_customization("standalone_")
        size = st.selectbox(
            "Size", [s.value for s in Size], key="standalone_drink_size")

        if st.button("Add Drink"):
            drink = Drink(
                DrinkType(drink_type),
                FountainFlavor(
                    flavor) if drink_type == DrinkType.FOUNTAIN.value else MilkshakeFlavor(flavor),
                Size(size)
            )
            st.session_state.current_order.add_item(drink)
            st.session_state.order_history.append(
                f"Added {size.capitalize()} {flavor}: ${drink.get_price():.2f}")
            st.rerun()

        # Add Fries
        st.subheader("Fries")
        fries_size = st.selectbox(
            "Fries Size", [s.value for s in Size], key="standalone_fries")
        if st.button("Add Fries"):
            fries = Fries(Size(fries_size))
            st.session_state.current_order.add_item(fries)
            st.session_state.order_history.append(
                f"Added {fries_size.capitalize()} Fries: ${fries.get_price():.2f}")
            st.rerun()

    # Order History
    st.subheader("Order History")
    for action in reversed(st.session_state.order_history):
        st.write(action)

    # Total
    st.subheader("Order Total")
    st.write(f"${st.session_state.current_order.get_total_price():.2f}")


if __name__ == "__main__":
    show_drive_thru_ui()
