import streamlit as st
import pandas as pd
def getDictValue(dictObj,strKey):
    if strKey in dictObj.keys():
        return dictObj[strKey]
    return None
def displayDocument(doc):
    doc_data = doc.to_dict()
    tblType = getDictValue(doc_data,'tableType')
    st.markdown(f"**Table Type:** {getDictValue(doc_data,'tableType')} **docId:** {doc.id}")
    st.table(getDictValue(doc_data,'tabledata'))
    #df = pd.DataFrame(getDictValue(doc_data,'tabledata'))
    #st.dataframe(df)
    with st.popover("More Information"):
         st.json(doc_data)
    st.markdown("---")