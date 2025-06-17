# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customise your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """
)

# option = st.selectbox(
#   "What is your favourite fruit?",
#    ("Banana", "Strawberry", "Peaches"),
#)

# st.write('Your favorite fruit is: ', option)


cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width= True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.datafreame(pd_df)
st.stop()

name_on_smoothie = st.text_input("Name on Smoothie: ")
st.write("The name on Smoothie will be: " + name_on_smoothie)

ingredients_list  = st.multiselect(
    "Choose upto 5 ingredients", 
    my_dataframe,
    max_selections=5
)

ingredients_string=''
if ingredients_list: 
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name_on_smoothie + """' , '""" + ingredients_string + """')"""
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_smoothie + '!', icon="✅")


ingredients_string=''
if ingredients_list: 
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

      
