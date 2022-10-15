import streamlit as st
import pandas as pd
from PIL import Image
import pickle

## Encoding Function
from sklearn.preprocessing import OneHotEncoder


## Group subarea_name to district of penang
northeast_penang_island = ["Gelugor", "Ayer Itam", "Tanjong Tokong", "Jelutong", "Georgetown", "Tanjung Bungah", "Greenlane", "Batu Ferringhi", 
                           "Pulau Tikus", "Batu Uban", "Bukit Jambul", "Paya Terubong", "Sungai Nibong", "Minden Heights", "Persiaran Gurney",
                           "Bukit Dumbar", "Tasek Gelugor", "Sungai Pinang", "USM", "Scotland"]
southwest_penang_island = ["Bayan Lepas", "Sungai Ara", "Balik Pulau", "Relau", "Bayan Baru", "Batu Maung", "Teluk Kumbar", "Teluk Bahang", "Pulau Betong"]
north_seberang_perai = ["Butterworth", "Bertam", "Kepala Batas", "Sungai Dua", "Air Tawar", "Penaga", "Raja Uda", "Bagan Ajam", "Bagan Lalang", 
                        "Seberang Perai", "Bagan Jesrmal"]
central_seberang_perai = ["Bukit Mertajam", "Alma", "Perai", "Seberang Jaya", "Juru", "Bukit Minyak", "Bukit Tengah", "Prai", "Permatang Pauh", 
                          "Bandar Perda", "Kubang Semang", "Pauh Jaya", "Berapit", "Penanti", "Permatang Tinggi", "Mak Mandin"]
south_seberang_perai = ["Simpang Ampat", "Batu Kawan", "Nibong Tebal", "Valdor", "Sungai Jawi", "Sungai Bakap", "Jawi", "Bukit Tambun"]
others = ["Others"]

## Group distric of penang to island and mainland
pg_island = ["North East Penang Island", "South West Penang Island"]
pg_mainland = ["North Seberang Perai", "Central Seberang Perai", "South Seberang Perai"]

## To create dataframe for prediction
columns_name = ["subarea_name", "category_name", "room_count", "size (sqrt)", "property_type", "price (RM)", "district_penang", "location_penang"]
encode_columns_name = ["subarea_name", "category_name", "property_type", "district_penang", "location_penang"]


## Subarea dropdown
subarea = ['Alma', 'Ayer Itam', 'Balik Pulau', 'Batu Ferringhi', 'Batu Kawan', 'Batu Maung', 'Batu Uban', 'Bayan Baru', 'Bayan Lepas', 'Bertam', 'Bukit Jambul', 'Bukit Mertajam', 'Butterworth', 'Gelugor', 'Georgetown', 'Greenlane', 'Jelutong', 'Kepala Batas', 'Nibong Tebal', 'Paya Terubong', 'Perai', 'Pulau Tikus', 'Relau', 'Seberang Jaya', 'Simpang Ampat', 'Sungai Ara', 'Sungai Nibong', 'Tanjong Tokong', 'Tanjung Bungah', 'Teluk Kumbar']


## Function to group subarea_name to district
def check_subarea_name (x):
    if x in northeast_penang_island:
        return "North East Penang Island"
    elif x in southwest_penang_island:
        return "South West Penang Island"
    elif x in north_seberang_perai:
        return "North Seberang Perai"
    elif x in central_seberang_perai:
        return "Central Seberang Perai"
    elif x in south_seberang_perai:
        return "South Seberang Perai"
    else:
        return "Others"
    
def check_island_mainland (x):
    if x in pg_island:
        return "Island"
    else:
        return "Mainland"

## Function to predict the price
def return_prediction(dataframe):
    ## Read existing pre_abt data
    pre_abt_df = pd.read_csv("pre_abt.csv")

    ## Creating instance of one-hot-encoder
    encoder = OneHotEncoder(categories = "auto", handle_unknown="ignore")

    train_abt_df = encoder.fit_transform(pre_abt_df[["subarea_name", "category_name", "property_type", "district_penang", "location_penang"]])

    ## perform one-hot encoding on 'team' column 
    encoder_df = pd.DataFrame(encoder.transform(dataframe[["subarea_name", "category_name", "property_type", "district_penang", "location_penang"]]).toarray())

    ## merge one-hot encoded columns back with original DataFrame
    abt_df = dataframe.join(encoder_df).drop(["subarea_name", "category_name", "property_type", "district_penang", "location_penang"], axis=1)

    ## Train test split
    y = abt_df["price (RM)"]

    ## Create separate object for input features
    X = abt_df.drop("price (RM)", axis=1)



    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(X)
    return result    
    


## Page Setting
st.set_page_config(page_title="My App")


## Webapp Layout
st.title("Location-Weighted Predictive Modelling of Penang Property Prices?")
st.image(Image.open("./image/penang.jpg"), width=700)
with st.expander("About this app"):
  st.write("This app is used to predict the Penang Housing Price.")


## Form Functionality
st.subheader("Please fill up below information to start predict.")

form = st.form("my_form")


prefer_location = form.selectbox("1. What is your preferred location?",(subarea))
prefer_type = form.selectbox("2. What is your preferred type of house?",(["Apartment / Condominium", "House"]))
property_type = form.selectbox("3. What is your preferred property type?",(["Freehold", "Leasehold"]))
size = form.slider("4. Total of house size (sqrt)?", 500, 3000, 2000)
room_count = form.slider("5. Total of room count?", 2, 10, 7)
house_price = 0
district_penang = check_subarea_name(prefer_location)
location_penang = check_island_mainland(district_penang)


## Data processing
form_return = [prefer_location, prefer_type, room_count, size, property_type,house_price,district_penang,location_penang]
data = [form_return]

predict_df = pd.DataFrame(data, columns=columns_name)

    
if form.form_submit_button("Start Predicting"):
    result = "RM" + str(round(return_prediction(predict_df)[0]))
    st.markdown(f'<h1 style="color:#00a249;font-size:30px;">{result}</h1>', unsafe_allow_html=True)

# form.form_submit_button("Start Predict")
# # st.info(form_return)






