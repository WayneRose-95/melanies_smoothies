# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]
cnx = st.connection("snowflake")
session = cnx.session() 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write('Choose the fruits you want in your custom Smoothie!')

# fruit_option = st.selectbox(
#     'What is your favourite fruit?', 
#     ('Banana', 'Strawberries', 'Peaches')
# )

name_on_order = st.text_input('Name')

# st.write('Your favourite fruit is:', fruit_option)
# Create a dataframe selecting from the fruit_options table 
# Returning only the fruit name column from the fruit_options table. 

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Using the .multiselect method to select multiple options.
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response)
# 5 ingredients are shown, but no code to enforce the limit 
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    # Printing out the contents of the ingredients_list for debugging.
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    # for each fruit chosen 
    ingredients_string = ' '
    for fruit_chosen in ingredients_list:
        # Concatentate each element of the list to a new string. 
        ingredients_string += fruit_chosen + ' '
    # Write this string to the console. 
    st.write(ingredients_string)


    # Inserting the data into the database. 
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    # st.write(my_insert_stmt)
    # st.stop() 
    
    # Showing the output to the console for debugging
    # st.write(my_insert_stmt)

    # Defining a variable to create a button to submit the order
    time_to_insert = st.button('Submit Order')
    # If this button is selected, then submit the order to the database. 
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success(f'Your smoothie is ordered, {name_on_order}!', icon="✅" )
