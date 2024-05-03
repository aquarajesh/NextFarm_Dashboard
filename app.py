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
farm_docs = (db.collection("checktraydata").where("ax_django_id", ">", 1).get())

tabAnlyse,tab1, tab2 = st.tabs(["Analyse Tables","NextFarmBubbleTables", "Farms"])
with tabAnlyse:
     farmdocs_docs = (db.collection("crops_test").list_documents())
     farm_ids = []
     for doc in farmdocs_docs:
         farm_ids.append(doc.id)
     option = st.selectbox("select Farm id",farm_ids,index=0,placeholder="Select Farm id...")
     message_path = st.text_input('Enter messages Collection Path:', 'crops_test/'+option+'/croptables')
     st.write('The current messagges from:', message_path)
     restockingPonds = {}
     if message_path:
         msgs_docs = (db.collection(message_path).get())
         for doc in msgs_docs:
             bsd.displayDocument(doc)
             doc_data = doc.to_dict()
             tblType = bsd.getDictValue(doc_data,'tableType')
             tabledata = bsd.getDictValue(doc_data,'tabledata')
             if tblType.lower() == 'stockingtable':
                for row in tabledata:
                    opindid = row["id"]
                    if row["optionId"] == "7":
                       if opindid not in restockingPonds.keys():
                           restockingPonds[opindid] = {
                               "harvested": True
                           }
                    else:
                        if opindid in restockingPonds.keys():
                            restockingPonds[opindid]["restocked"] = True
         if len(restockingPonds.keys()):
             st.write("Restocking Ponds")
             df = pd.DataFrame(restockingPonds)
             st.dataframe(df)
                 
     
# with tab1:
#      farm_docs = (db.collection("checktraydata").where("ax_django_id", ">", 1).get())
#      farm_ids = []  
#      for doc in farm_docs:
#          farm_ids.append(doc.id)
#      option1 = st.selectbox("select Farm id",farm_ids,index=None,placeholder="Select Farm id...")
#      if option1:
#         current_doc = None
#         for doc in farm_docs:
#             if doc.id == option1:
#                current_doc = doc
#                break
#         if current_doc.exists: 
#             data = current_doc.to_dict() 
#             cycle = data["crop"]  
#             cycle = cycle.lower().replace("crop", "cycle")
#             docPath = 'nextfarm_messages/'+option1+'/'+cycle+'/messages/data'
#             message_path = st.text_input('Enter messages Collection Path:', docPath)
#             st.write('The current messagges from:', message_path)
#        #/nextfarm_messages/AQU1304248352/cycle1/messages/data
#             if message_path:
#                msgs_docs = (db.collection(message_path).get())
#                for doc in msgs_docs:
#                    bsd.displayDocument(doc)
with tab2:
     farm_docs = (db.collection("checktraydata").where("ax_django_id", ">", 1).get())
     docids = []  
     for doc in farm_docs:
         docids.append(doc.id)
     option2 = st.selectbox("select Farm id",docids,index=None,placeholder="Select Farm id...")
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



