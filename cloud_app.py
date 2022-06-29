import streamlit as st
import altair as alt
import sqlalchemy
import pymysql
import pandas as pd
import plotly.express as px




# student_conn_string = "mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com/data_academy_02_2022"
# engeto_data_conn = sqlalchemy.create_engine(student_conn_string)
#
# query = """
#     SELECT
#         DATE(a.date_from) AS date,
#         a.value,
#         b.name AS product,
#         c.name AS location
#     FROM czechia_price a
#     LEFT JOIN czechia_price_category b
#         ON a.category_code = b.code
#     LEFT JOIN czechia_region c
#         ON a.region_code = c.code
#     WHERE c.name IS NOT NULL
# """
# df = pd.read_sql(query, engeto_data_conn)
# df.to_csv('price_data.csv', header=True, index=None)


df = pd.read_csv('price_data.csv',index_col=None)
df['date'] = pd.to_datetime(df['date'])
st.write(df)

# product_options_query = """
#     SELECT
#         DISTINCT name
#     FROM czechia_price_category
# """

product_options_list = list(df['product'].unique())
# product_options_df = pd.read_sql(product_options_query, engeto_data_conn)
# product_options_list = product_options_df['name'].to_list()
product_choice = st.sidebar.selectbox('Product', product_options_list)

# region_options_query = """
# SELECT
#     DISTINCT name
# FROM czechia_region
# """

region_options_list = list(df.location.unique())
# region_options_df = pd.read_sql(region_options_query, engeto_data_conn)
# region_options_list = region_options_df['name'].to_list()
region_choice = st.sidebar.multiselect('Location', region_options_list, default=['Hlavní město Praha'])

df = df[(df['product'] == product_choice) & (df['location'].isin(region_choice))]


brush = alt.selection(type='interval', encodings=['x'])
selection = alt.selection_multi(fields=['location'], bind='legend')

base = alt.Chart(df).mark_line().encode(
    x='date',
    y=alt.Y('value', scale=alt.Scale(zero=False)),
    color='location',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection
)

upper = base.encode(
    alt.X('date', scale=alt.Scale(domain=brush)),
).properties(width=700)

lower = base.properties(height=60, width=700).add_selection(brush)


c1, c2, c3 = st.columns((1,5,1))
c2.markdown('# Product prices by regions')

st.altair_chart(upper & lower, use_container_width=True)




    

