import streamlit as st
import pandas as pd
def getDictValue(dictObj,strKey)->any:
    if strKey in dictObj.keys():
        return dictObj[strKey]
    return None
def displayDocument(doc):
    doc_data = doc.to_dict()
    tblType = getDictValue(doc_data,'tableType')
    st.markdown(f"**Table Type:** {getDictValue(doc_data,'tableType')} **docId:** {doc.id}")
    tabledata = getDictValue(doc_data,'tabledata')
    if tabledata:
       if tblType.lower() == 'croptable':
          newtabledata = tabledata["cropPonds"]
          for row in newtabledata:
              row["startDate"] = tabledata["startDate"]
              row["name"] = tabledata["name"]
          st.table(newtabledata)
       else:
          st.table(tabledata)
    #df = pd.DataFrame(getDictValue(doc_data,'tabledata'))
    #st.dataframe(df)
    with st.popover("More Information"):
         st.json(doc_data)
    st.markdown("---")