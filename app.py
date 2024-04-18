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
tab1, tab2 = st.tabs(["NextFarmBubbleTables", "Farms"])

with tab1:
    if st.button('Show NextFarmTables'):
    #/nextfarm_messages/AQU1304248352/cycle1/messages/data
        msgs_docs = (
         db.collection("nextfarm_messages/AQU1304248352/cycle1/messages/data").stream()
        )
        for doc in msgs_docs:
            bsd.displayDocument(doc)
with tab2:          
    if st.button('Show Farms'):
       checktray_docs = (
            db.collection("checktraydata").where("isRealSite", "==", True).stream()
        )
       for doc in checktray_docs:
	       fd.displayDocument(doc)
    


# doc_ref = db.collection("checktraydata").document("AGV2402246188")
# doc = doc_ref.get()
# fd.displayDocument(doc)
# Add final separator to end of grid



