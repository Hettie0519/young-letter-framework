import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import easyocr
import fitz
import os
import glob
import json

# Initialize reader with Chinese and English
print('Initializing OCR reader...')
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

source_dir = r'C:\Develop\ts\.claude\skills\young-letter-framework\sources'
output_dir = r'C:\Develop\ts\.claude\skills\young-letter-framework\references\research'
os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted(glob.glob(os.path.join(source_dir, '*.pdf')))

def extract_text_from_pdf(pdf_path, max_pages=10):
    """Extract text from PDF using EasyOCR"""
    doc = fitz.open(pdf_path)
    pages_text = []
    
    # Extract first max_pages for overview
    for page_num in range(min(max_pages, len(doc))):
        page = doc[page_num]
        
        # Convert to image with good resolution
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        # Save to temp file
        temp_path = os.path.join(source_dir, f'temp_page_{page_num}.png')
        pix.save(temp_path)
        
        # OCR
        result = reader.readtext(temp_path, detail=0)
        text = '\n'.join(result)
        pages_text.append(text)
        
        # Clean up temp file
        os.remove(temp_path)
    
    doc.close()
    return pages_text

# Process each PDF
all_content = {}

for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    print(f'\n=== Processing: {filename} ===')
    
    # Extract text
    pages_text = extract_text_from_pdf(pdf_path)
    
    # Get page count
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    doc.close()
    
    print(f'Total pages: {page_count}')
    print(f'Extracted preview: {len(pages_text)} pages')
    print(f'First page content (first 500 chars): {pages_text[0][:500] if pages_text else "N/A"}')
    
    # Store result
    all_content[filename] = {
        'total_pages': page_count,
        'extracted_pages': len(pages_text),
        'pages': pages_text
    }

# Save to JSON
output_path = os.path.join(output_dir, 'extracted_content.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_content, f, ensure_ascii=False, indent=2)

print(f'\nSaved to: {output_path}')