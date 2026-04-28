
import zipfile
import xml.etree.ElementTree as ET
import os

def extract_text(docx_path):
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            texts = tree.findall('.//w:t', namespace)
            return '\n'.join([t.text for t in texts if t.text])
    except Exception as e:
        return str(e)

docx_path = r"C:\Users\ASUS\Desktop\Smartsaha-Doc\SmartSaha_MultiPlateforme.docx"
text = extract_text(docx_path)
with open('extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Extraction complete.")
