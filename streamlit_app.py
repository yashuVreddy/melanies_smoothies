# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
    """
    Choose the fruit you want in your custom Smoothie!!
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write("""Choose the fruits you want in your custom smoothie""")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("Fruit_Name"),col('Search_On'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list =st.multiselect('Choose up to 5 ingredients:',my_dataframe)

if ingredients_list:
    #st.write(ingredients_list);
    # st.text(ingredients_list)

    ingredients_string ='';
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen +'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '"""+ name_on_order+ """')"""

    st.write(my_insert_stmt)

    
    time_to_insert = st.button('Sumbit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        #my_variable = 'Your Smoothie is ordered! %S',name_on_order
        st.success('Your Smoothie is ordered!',icon="✅")


