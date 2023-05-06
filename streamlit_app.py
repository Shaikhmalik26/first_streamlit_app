import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Dinner")

streamlit.header('Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
#create repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
#Snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall() 
    
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('Please select a fruit to get information')
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
  streamlit.error()
# takes the json version of the response and normalize it
# show the normalize response data as a table on the screen
#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values('add_my_fruit')
            return "Thanks For Adding "+ new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
#Add a button to load a fruit
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function= insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
  

#dont run anything past here while we troubleshoot
streamlit.stop()

streamlit.header("The fruit load list contains:")
