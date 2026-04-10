import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import easyocr
import fitz
import os
import glob
import json

# Initialize reader
print('Initializing OCR reader...')
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

source_dir = r'C:\Develop\ts\.claude\skills\young-letter-framework\sources'
output_dir = r'C:\Develop\ts\.claude\skills\young-letter-framework\references\research'
os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted(glob.glob(os.path.join(source_dir, '*.pdf')))

def extract_text_from_page(pdf_path, page_num):
    """Extract text from a specific PDF page using EasyOCR"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    
    # Convert to image with good resolution
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    
    # Save to temp file
    temp_path = os.path.join(source_dir, f'temp_page_{page_num}.png')
    pix.save(temp_path)
    
    # OCR
    result = reader.readtext(temp_path, detail=0)
    text = '\n'.join(result)
    
    # Clean up
    os.remove(temp_path)
    doc.close()
    
    return text

# Extract detailed content from each book
book_data = {}

for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    print(f'\n=== Processing: {filename} ===')
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()
    
    # Extract: cover, TOC (usually page 1-3), first several pages
    pages_to_extract = []
    
    # TOC typically at the beginning (pages 1-3)
    for i in range(min(3, total_pages)):
        pages_to_extract.append(('toc', i))
    
    # First 10 content pages
    for i in range(3, min(13, total_pages)):
        pages_to_extract.append(('content', i))
    
    # Last few pages if book is large
    if total_pages > 50:
        for i in range(total_pages - 3, total_pages):
            pages_to_extract.append(('end', i))
    
    extracted = {}
    for page_type, page_num in pages_to_extract:
        text = extract_text_from_page(pdf_path, page_num)
        key = f'{page_type}_{page_num}'
        extracted[key] = text
    
    # Store
    book_data[filename] = {
        'total_pages': total_pages,
        'extracted': extracted
    }
    
    print(f'Extracted {len(extracted)} pages')

# Save to JSON
output_path = os.path.join(output_dir, 'extracted_full.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=2)

print(f'\nSaved to: {output_path}')