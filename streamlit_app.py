import streamlit as st
from snowflake.snowpark.functions import col
import time

# Title for the app
st.title("Smoothie Maker 1000 :cup_with_straw:")
st.write("Place your order below!")

# Connect to Snowflake using your Streamlit connection
cnx = st.connection("snowflake")
session = cnx.session()

# Retrieve fruit options from the fruit_options table
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# Convert the Snowpark DataFrame into a list of fruit names
fruit_options = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# Display fruit options for the user to choose from (multiselect)
ingredients_list = st.multiselect("Choose up to five ingredients:", fruit_options)

# Text input for the customer's name (name_on_order)
name_on_order = st.text_input("Enter your name for the order:")

# Button to submit the order
if st.button("Submit Order"):
    # Validate that at least one ingredient and a name were provided
    if not ingredients_list:
        st.error("Please select at least one ingredient!")
    elif not name_on_order:
        st.error("Please enter your name!")
    else:
        # Create a single string from the list of ingredients (space-separated)
        ingredients_string = " ".join(ingredients_list)
        
        # Build the INSERT statement (using f-string for clarity)
        # This assumes your orders table has columns INGREDIENTS and NAME_ON_ORDER
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """
        st.write("Executing query:")
        st.code(my_insert_stmt)
        
        # Execute the query
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is Ordered!", icon="✅")
