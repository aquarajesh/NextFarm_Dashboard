import streamlit as st
from google.cloud import storage
from google.oauth2 import service_account
import json
import pandas as pd

# Load service account info from Streamlit secrets
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)

# Initialize a client
storage_client = storage.Client(credentials=creds, project=key_dict["project_id"])

# Name of your bucket
bucket_name = 'checktray-ml'  # Corrected bucket name

def count_images_by_day():
    try:
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix='ml/')  # Use prefix to specify directory within the bucket
        day_counts = {}
        for blob in blobs:
            creation_date = blob.time_created
            day = creation_date.strftime('%Y-%m-%d')
            if day not in day_counts:
                day_counts[day] = {'count': 0, 'paths': []}
            day_counts[day]['count'] += 1
            day_counts[day]['paths'].append(blob.name)
        return day_counts
    except Exception as e:
        st.error(f"Error counting images: {e}")
        return None

# Streamlit app
st.title("Image Count by Day in Google Cloud Storage")

if st.button("Count Images"):
    day_counts = count_images_by_day()
    if day_counts:
        # Convert day_counts dictionary to a DataFrame
        data = [{'Date': day, 'Count': info['count'], 'Paths': ', '.join(info['paths'])} for day, info in day_counts.items()]
        df = pd.DataFrame(data)
        df = df.sort_values(by='Date')
        
        st.subheader("Image Counts by Day")
        st.table(df)
        
        total_count = df['Count'].sum()
        st.subheader(f"Total Image Count: {total_count}")
    else:
        st.write("No images found or an error occurred.")
