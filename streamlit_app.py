import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import time

# Set up the title and description
st.title("Smoothie Maker 1000 :cup_with_straw:")
st.write("Place your order below!")

# Connect to Snowflake using the Streamlit connection
cnx = st.connection("snowflake")
session = cnx.session()

# Function to load orders from the table
def load_orders():
    return session.table("smoothies.public.orders")\
                  .select(col("INGREDIENTS"), col("NAME_ON_ORDER"), col("ORDER_FILLED"), col("ORDER_TS"))\
                  .collect()

# Display current orders in the table
st.subheader("Current Orders")
try:
    orders = load_orders()
    st.dataframe(orders)
except Exception as e:
    st.error(f"Error loading orders: {e}")

# Inputs for new order
st.subheader("Create a New Order")
ingredients_input = st.text_input("Enter ingredients (separate with spaces):")
name_on_order = st.text_input("Enter your name:")

# Checkbox for order status
order_filled = st.checkbox("Mark order as filled")

# Button to submit the order
if st.button("Submit Order"):
    if not ingredients_input or not name_on_order:
        st.error("Please provide both ingredients and your name.")
    else:
        # Build the INSERT statement
        # Note: For production, parameterized queries should be used to prevent SQL injection.
        insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_input + """','"""+name_on_order+ """')""" 
        st.write(my_insert_stmt)
        st.stop
        try:
            st.write("Executing query:")
            st.code(insert_stmt)
            session.sql(insert_stmt).collect()
            st.success("Your order has been submitted!")
        except Exception as e:
            st.error(f"Error inserting order: {e}")

# Button to refresh the orders display
if st.button("Refresh Orders"):
    try:
        orders = load_orders()
        st.dataframe(orders)
    except Exception as e:
        st.error(f"Error refreshing orders: {e}")
