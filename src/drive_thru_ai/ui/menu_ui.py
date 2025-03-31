import streamlit as st
from drive_thru_ai.menu import *#Burger, IngredientAmount, Size, Drink, DrinkType, FountainFlavor, MilkshakeFlavor, Nuggets, Meal, Fries


def show_menu():
    st.set_page_config(page_title="Fast Food Menu", layout="wide")
    st.title("Fast Food Menu")

    # Burgers Section
    st.header("Burgers")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Basic Burger")
        burger = Burger(5.99)
        st.write(f"**Price:** ${burger.get_price():.2f}")
        st.write(f"**Description:** {burger.get_description()}")
        # st.image(burger.get_image(), width=200)

    with col2:
        st.subheader("Double Patty Burger")
        double_burger = Burger(6.99)
        double_burger.set_ingredient("patty", IngredientAmount.DOUBLE)
        st.write(f"**Price:** ${double_burger.get_price():.2f}")
        st.write(f"**Description:** {double_burger.get_description()}")
        # st.image(double_burger.get_image(), width=200)

    with col3:
        st.subheader("Custom Burger")
        custom_burger = Burger(6.99)
        custom_burger.set_ingredient("cheese", IngredientAmount.DOUBLE)
        custom_burger.set_ingredient("lettuce", IngredientAmount.LIGHT)
        custom_burger.set_ingredient("onion", IngredientAmount.NONE)
        st.write(f"**Price:** ${custom_burger.get_price():.2f}")
        st.write(f"**Description:** {custom_burger.get_description()}")
        # st.image(custom_burger.get_image(), width=200)

    # Nuggets Section
    st.header("Chicken Nuggets")
    nuggets_cols = st.columns(len(Nuggets.PIECE_COUNTS))

    for i, count in enumerate(Nuggets.PIECE_COUNTS):
        with nuggets_cols[i]:
            nuggets = Nuggets(count)
            st.subheader(f"{count} Piece Nuggets")
            st.write(f"**Price:** ${nuggets.get_price():.2f}")
            st.write(f"**Description:** {nuggets.get_description()}")
            # st.image(nuggets.get_image(), width=200)

    # Drinks Section
    st.header("Drinks")

    # Fountain Drinks
    st.subheader("Fountain Drinks")
    fountain_cols = st.columns(len(Size))

    for i, size in enumerate(Size):
        with fountain_cols[i]:
            st.write(f"**{size.value.capitalize()}**")
            for flavor in FountainFlavor:
                drink = Drink(DrinkType.FOUNTAIN, flavor, size)
                st.write(f"{flavor.value}: ${drink.get_price():.2f}")

    # Milkshakes
    st.subheader("Milkshakes")
    milkshake_cols = st.columns(len(Size))

    for i, size in enumerate(Size):
        with milkshake_cols[i]:
            st.write(f"**{size.value.capitalize()}**")
            for flavor in MilkshakeFlavor:
                drink = Drink(DrinkType.MILKSHAKE, flavor, size)
                st.write(f"{flavor.value}: ${drink.get_price():.2f}")

    # Fries Section
    st.header("French Fries")
    fries_cols = st.columns(len(Size))

    for i, size in enumerate(Size):
        with fries_cols[i]:
            fries = Fries(size)
            st.subheader(f"{size.value.capitalize()} Fries")
            st.write(f"**Price:** ${fries.get_price():.2f}")
            st.write(f"**Description:** {fries.get_description()}")
            # st.image(fries.get_image(), width=200)

    # Meals Section
    st.header("Value Meals")
    meal_cols = st.columns(2)

    with meal_cols[0]:
        st.subheader("Burger Meal")
        burger_meal = Meal(
            main_item=Burger(5.99),
            drink=Drink(DrinkType.FOUNTAIN, FountainFlavor.COKE, Size.MEDIUM),
            fries=Fries(Size.MEDIUM)
        )
        st.write(f"**Price:** ${burger_meal.get_price():.2f}")
        st.write(f"**Description:** {burger_meal.get_description()}")
        # st.image(burger_meal.get_image(), width=200)

    with meal_cols[1]:
        st.subheader("Nuggets Meal")
        nuggets_meal = Meal(
            main_item=Nuggets(10),
            drink=Drink(DrinkType.FOUNTAIN, FountainFlavor.COKE, Size.MEDIUM),
            fries=Fries(Size.MEDIUM)
        )
        st.write(f"**Price:** ${nuggets_meal.get_price():.2f}")
        st.write(f"**Description:** {nuggets_meal.get_description()}")
        # st.image(nuggets_meal.get_image(), width=200)


if __name__ == "__main__":
    show_menu()
