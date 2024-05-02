import streamlit as st
import json
from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
import farmdata as fd
import bubble_msg_data as bsd

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="nextaqua-22991")
tabAnlyse,tab1, tab2 = st.tabs(["Analyse Tables","NextFarmBubbleTables", "Farms"])
with tabAnlyse:
     message_path = st.text_input('Enter messages Collection Path:', '/crops_test/BAV1812238444/croptables')
     st.write('The current messagges from:', message_path)
     if message_path:
         msgs_docs = db.collection(message_path).get()
         for doc in msgs_docs:
             bsd.displayDocument(doc)
     
with tab1:
      message_path = st.text_input('Enter messages Collection Path:', 'nextfarm_messages/AQU1304248352/cycle1/messages/data')
      st.write('The current messagges from:', message_path)
       #/nextfarm_messages/AQU1304248352/cycle1/messages/data
      if message_path:
         msgs_docs = db.collection(message_path).get()
         for doc in msgs_docs:
             bsd.displayDocument(doc)
with tab2:          
    if st.button('Show Farms'):
       checktray_docs = db.collection("checktraydata").where("ax_django_id", ">", 1).get()
       for doc in checktray_docs:
	       fd.displayDocument(doc)


    


# doc_ref = db.collection("checktraydata").document("AGV2402246188")
# doc = doc_ref.get()
# fd.displayDocument(doc)
# Add final separator to end of grid



