import os
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse

def download_media(xml_file, output_folder="downloads"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    opportunities = root.findall(".//Opportunity")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for opp in opportunities:
        opportunity_id = opp.find("OpportunityID").text if opp.find("OpportunityID") is not None else "unknown"
        media_folder = os.path.join(output_folder, opportunity_id)
        
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)
        
        medias = opp.find("Medias")
        if medias is not None:
            for media in medias.findall("Media"):
                media_url = media.text
                if media_url:
                    download_file(media_url, media_folder)

def download_file(url, folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        file_path = os.path.join(folder, filename)
        
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed {url}: {e}")

# Use:
download_media("wallet.xml")
