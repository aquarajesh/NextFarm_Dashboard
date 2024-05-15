import streamlit as st
import json
from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
import farmdata as fd
import bubble_msg_data as bsd
import utils

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="nextaqua-22991")
farm_docs = (db.collection("checktraydata").where("ax_django_id", ">", 1).get())

tabAnlyse,tab1, tab2 = st.tabs(["Analyse Tables","NextFarmBubbleTables", "Farms"])
with tabAnlyse:
     farm_ids = []
     for doc in farm_docs:
         farm_ids.append(doc.id)
     option = st.selectbox("select Farm id",farm_ids,index=0,placeholder="Select Farm id...")
     tabletypes = utils.tableTypes
     selectedTableType = st.selectbox("select Table id",tabletypes,index=0,placeholder="Select TableType...")
     filter_docs = []
     if option:
        mpath = "nextfarm_data/"+option+"/allcrops/messages/data"
        filter_docs = db.collection(mpath).where("tableType","==",selectedTableType).get()
        st.write('The current messagges from:',mpath)
        st.write(selectedTableType+" count="+str(len(filter_docs)))
        for doc in filter_docs:
            bsd.displayDocument(doc)

        
     
                 
     
with tab1:
     farm_ids = []  
     for doc in farm_docs:
         farm_ids.append(doc.id)
     option1 = st.selectbox("select Farm id",farm_ids,index=None,placeholder="Select Farm id...",key="messagesdata")
     if option1:
        current_doc = None
        for doc in farm_docs:
            if doc.id == option1:
               current_doc = doc
               break
        if current_doc.exists: 
            data = current_doc.to_dict() 
            docPath = 'nextfarm_data/'+option1+'/allcrops/messages/data'
            st.write('The current messagges from:', docPath)
            msgs_docs = (db.collection(docPath).get())
            for doc in msgs_docs:
                bsd.displayDocument(doc)
with tab2:
     docids = []  
     for doc in farm_docs:
         docids.append(doc.id)
     option2 = st.selectbox("select Farm id",docids,index=None,placeholder="Select Farm id...",key="farmsdata")
     if option2:
        farmdoc_path = st.text_input('Enter Farm data Path:', 'checktraydata/'+option2)
        st.write('The Farm Data:', farmdoc_path)
        if farmdoc_path:
           farm_doc = (db.collection('checktraydata').document(option2).get())
           fd.displayDocument(farm_doc)


        
    # if st.button('Show Farms'):
    #    checktray_docs = (db.collection("checktraydata").where("ax_django_id", ">", 1).get())
    #    for doc in checktray_docs:
	#        fd.displayDocument(doc)


    


# doc_ref = db.collection("checktraydata").document("AGV2402246188")
# doc = doc_ref.get()
# fd.displayDocument(doc)
# Add final separator to end of grid



