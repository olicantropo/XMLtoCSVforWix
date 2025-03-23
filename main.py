import xml.etree.ElementTree as ET
import csv
import re

def clean_html_tags(text):
    """Remove tags HTML e substitui por espaços."""
    return re.sub(r'<[^>]+>', ' ', text).strip() if text else ""

def xml_to_wix_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    opportunities = root.findall(".//Opportunity")
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Wix CSV Headers
        headers = [
            "ID Oportunidade", "Tipo de Transação", "Categoria", "Subcategoria", "Descrição", "Preço", 
            "Área Construída", "Quartos", "Banheiros", "Suítes", "Garagem", "Cidade", "Estado", "País", 
            "Imagem Principal", "Galeria de Imagens"
        ]
        writer.writerow(headers)
        
        for opp in opportunities:
            opportunity_id = opp.find("OpportunityID").text if opp.find("OpportunityID") is not None else ""
            transaction_type = opp.find("TransactionType").text if opp.find("TransactionType") is not None else ""
            transaction_type = "Venda" if transaction_type == "For Sale" else transaction_type
            
            details = opp.find("Details")
            category = details.find("Category").text if details.find("Category") is not None else ""
            subcategory = details.find("Subcategory").text if details.find("Subcategory") is not None else ""
            description = clean_html_tags(details.find("Description").text) if details.find("Description") is not None else ""
            price = details.find("ListPrice").text if details.find("ListPrice") is not None else ""
            living_area = details.find("LivingArea").text if details.find("LivingArea") is not None else ""
            bedrooms = details.find("Bedrooms").text if details.find("Bedrooms") is not None else ""
            bathrooms = details.find("Bathrooms").text if details.find("Bathrooms") is not None else ""
            suites = details.find("Suites").text if details.find("Suites") is not None else ""
            garage = details.find("Garage").text if details.find("Garage") is not None else ""
            
            location = opp.find("Location")
            city = location.find("City").text if location.find("City") is not None else ""
            state = location.find("State").text if location.find("State") is not None else ""
            country = location.find("Country").text if location.find("Country") is not None else ""
            
            medias = opp.find("Medias")
            images = [media.text for media in medias.findall("Media[@type='image']")] if medias is not None else []
            cover_image = images[0] if images else ""
            image_gallery = ",".join(images[1:]) if len(images) > 1 else ""
            
            writer.writerow([
                opportunity_id, transaction_type, category, subcategory, description, price, 
                living_area, bedrooms, bathrooms, suites, garage, city, state, country, 
                cover_image, image_gallery
            ])
    
    print(f"Done: {csv_file}")

xml_to_wix_csv("wallet.xml", "output.csv")
