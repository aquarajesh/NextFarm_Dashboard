
import streamlit as st
import pandas as pd

def getDictValue(dictObj,strKey):
    if strKey in dictObj.keys():
        return dictObj[strKey]
    return None

def display_farmheader(doc_data):
    st.header(f"**Farm:** {doc_data['farm_name']}")
    with st.popover("More Information"):
         st.markdown(f"**Crop:** {getDictValue(doc_data,'crop')}")
         st.markdown(f"**Crop Active:** {getDictValue(doc_data,'cropActive')}")
         st.markdown(f"**Section Id:** {getDictValue(doc_data,'section_id')}")
         st.markdown(f"**Shipping Address:** {getDictValue(doc_data,'shipping_address')}")   
         st.markdown(f"**RealSite:** {getDictValue(doc_data,'isRealSite')}")  
         st.markdown(f"**Location:** {getDictValue(doc_data,'gps_location')}")


def display_supervisors(doc_data):
    if 'supervisors' in doc_data.keys():
        data = doc_data["supervisors"]
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No Supervisors Data")

def display_feedboys(doc_data):
    if 'feedboys' in doc_data.keys():
        data = doc_data["feedboys"]
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No Feedboys Data")
def display_farmers(doc_data):
    if 'farmers' in doc_data.keys():
        data = doc_data["farmers"]
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No Farmers Data")   

def display_access_numbers(doc_data):
    if 'access_numbers' in doc_data.keys():
        data = doc_data["access_numbers"]
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No Access Numbers Data")

def display_ponds(doc_data):
    ponds_data = doc_data["ponds"]
    st.subheader("Ponds")
    num_columns = 4  # Adjust the number of columns based on your preference
    num_items = len(ponds_data)
    rows_per_column = (num_items + num_columns - 1) // num_columns  # Ceiling division
    # Create columns for grid layout
    columns = st.columns(num_columns)
    for idx, pond in enumerate(ponds_data):
        col_idx = idx // rows_per_column
        with columns[col_idx]:
            container = st.container(border=True)
            with container:
                 st.markdown(f"**Pond Name:** {getDictValue(pond,'pond_name')}")
                 with st.popover("other information"):
                      st.markdown(f"**Pond Id:** {getDictValue(pond,'pond_id')}")
                      st.markdown(f"**RFID:** {getDictValue(pond,'rfid')}")
                      st.markdown(f"**Option Id:** {getDictValue(pond,'optionId')}")
                      st.markdown(f"**Acres:** {getDictValue(pond,'acres')}")
                      st.markdown(f"**Pond Crops:** {getDictValue(pond,'crops')}")
                 with st.popover("Checktrays"):
                    df = pd.DataFrame(pond['checktrays'])
                    st.dataframe(df)
                 with st.popover("Stocking"):
                    if 'stocking' in pond.keys():
                        df = pd.DataFrame(pond['stocking'])
                        st.dataframe(df)
                    else:
                        st.write("No stocking data")

def displayDocument(doc):
    doc_data = doc.to_dict()
    container = st.container(border=True)
    with container:
         display_farmheader(doc_data)
         showMetadata(doc_data)
         with st.expander("Ponds"):
              display_ponds(doc_data)
         with st.expander("Supervisors"):
              display_supervisors(doc_data)
         with st.expander("Farmers"):
              display_farmers(doc_data)
         with st.expander("Feed Boys"):
              display_feedboys(doc_data)
         with st.expander("Access Numbers"):
              display_access_numbers(doc_data)
def showMetadata(doc):
    with st.popover("json:"):
         st.json(doc)

           



         