import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz
import os
import glob
import json

source_dir = r'C:\Develop\ts\.claude\skills\young-letter-framework\sources'
pdf_files = sorted(glob.glob(os.path.join(source_dir, '*.pdf')))

for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    print(f"=== {filename} ===")
    
    try:
        doc = fitz.open(pdf_path)
        print(f"Pages: {len(doc)}")
        
        # Get info from first page
        page = doc[0]
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])
        print(f"Blocks: {len(blocks)}")
        
        if blocks:
            # Sample first few blocks
            for i, block in enumerate(blocks[:3]):
                block_type = block.get("type")
                print(f"Block {i}: type={block_type}")
                if block_type == 0:  # text block
                    lines = block.get("lines", [])
                    for j, line in enumerate(lines[:2]):
                        spans = line.get("spans", [])
                        for span in spans:
                            text = span.get("text", "")
                            if text.strip():
                                print(f"  Text: {text[:100]}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()