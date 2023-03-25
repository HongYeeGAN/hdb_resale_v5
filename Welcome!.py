import streamlit as st
import plotly.express as px
import pandas as pd
import base64
import time


########################################################################################################################

# https://www.google.com/search?q=Introducing+multipage+apps!+streamlit&rlz=1C1SQJL_enSG972SG972&oq=Introducing+multipage+apps!++streamlit&aqs=chrome..69i57j69i60l2.3585j0j15&sourceid=chrome&ie=UTF-8#fpstate=ive&vld=cid:76e79db5,vid:YClmpnpszq8



#######################################################################################################################################

st.set_page_config(layout="wide", page_title="Welcome")

# https://soundcloud.com/ashamaluevmusic/imagination
# https://github.com/streamlit/streamlit/issues/2446
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true" loop="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

col1, mid, col2, mid, col3 = st.columns([1,1.5,20,1,13])
with col1:
    st.image('logo.png', width = 50)
with col2:
    original_title = '<h1 style ="font-weight: bold;position: relative; bottom: 10px;color:#0066cc; font-size: 28px;">FlatFinder</h1>'
    st.markdown(original_title, unsafe_allow_html=True)
with col3:
    autoplay_audio("Imagination.mp3")


st.markdown(
    """
    <div style='background-color: #0066cc; padding: 30px'>
        <h2 style='color: white;'>Welcome to FlatFinder!</h2>
        <p style='color: white;'>Plan your next home in 4 simple steps</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='padding: 8px'>
        <h3 style='color: white;color: #808080;text-align: left;'>Observe how the home prices in each town changes over the years</h3>
    </div>
    """,
    unsafe_allow_html=True
)



######################################################################################################

map4 = pd.read_csv("map4.csv")

figure = px.scatter(map4, x='Price/sqm (S$)', y='Distance from city center in km', animation_frame="year",
                    size='scale',
                    color='Price/sqm (S$)', range_x = [1500, 7500],
                    title='Click on the bubble to select town<br>'
                          'Color represent price per square meter    •      '
                          'Size represent transaction count',
                    log_x=False, size_max=55, text='town', opacity = 0.7,
                    color_continuous_scale='YlGnBu',
                    hover_data={
                                    'town': True,
                                    'year': True,
                                    'Distance from city center in km': False,
                                    'transaction_count': True,
                                    'scale': False},
                        labels={'year': 'Year','town': 'Town ',
                                'transaction_count': 'Number of transactions'}


                    )

figure.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
figure.update_traces(textposition='bottom center', textfont_size=10, textfont_color = '#808080')
figure.update_layout(width=800, height=900, title_font_color='#808080',
                    title_x=0, plot_bgcolor="white",
                    paper_bgcolor="white", clickmode='event+select',
                    xaxis=dict(showgrid=True, gridcolor="lightgrey"),
                    yaxis=dict(showgrid=True, gridcolor="lightgrey"))

def update_color(trace, points, selector):
    c = list(trace.marker.color)
    for i in points.point_inds:
        c[i] = '#FF69B4'  # Set selected point color to pink
    trace.marker.color = c

figure.data[0].on_selection(update_color)

col1, col2, col3 = st.columns([0.5,10,0.5])
with col1:
    st.write(" ")
with col2:
    st.plotly_chart(figure, use_container_width=True)

with col3:
    st.write(" ")

####################################################################################################3

observation = """
The plot above shows housing prices of different towns in Singapore based on their distance from the city center, with higher prices indicated by darker colors and fewer transactions by smaller bubbles.

Generally, homes located closer to the city center are priced higher but have fewer transactions, while those situated further away are cheaper with more transactions.

Over time, HDB resale prices in Singapore have increased, although there was a drop in housing prices starting from 2013. The pandemic in 2020 caused an increase in demand for housing, leading to further price appreciation. Some towns, like Bishan, Ang Mo Kio, Toa Payoh, and Tampines, have experienced steady price increase, while others, like Punggol and Sengkang, have seen more significant acceleration recently due to new amenities.

Housing prices in Singapore have generally increased over time, with some fluctuations and variations across different towns, driven by factors such as population growth, urban development, and government policies.
"""
def typewriter(text):
    t = st.empty()
    for i in range(len(text)):
        t.write(text[:i+1])
        time.sleep(0.05)
        if i == len(text) - 1:
            time.sleep(1) # wait for 1 second after the text is fully displayed

# Define a button with custom CSS style
button_style = """
    <style>
    div.stButton > button:first-child {
        background-color: #B7C9E2;
        color: #31333F;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)
# Define a button
button = st.button("Click me after interacting with the plot animation!")

# If the button is clicked, display some text
if button:
    typewriter(observation)

########################################################################################################################




