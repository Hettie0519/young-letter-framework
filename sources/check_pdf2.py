import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pypdf import PdfReader
import os
import glob

source_dir = r'C:\Develop\ts\.claude\skills\young-letter-framework\sources'
pdf_files = sorted(glob.glob(os.path.join(source_dir, '*.pdf')))

# Check first PDF in detail
pdf_path = pdf_files[3]  # 怎样解脱我的困惑
filename = os.path.basename(pdf_path)
print(f"=== {filename} ===")

reader = PdfReader(pdf_path)
print(f"Pages: {len(reader.pages)}")
print(f"Metadata: {reader.metadata}")
print(f"Trailer: {reader.trailer}")

# Check attachments
if hasattr(reader, 'attachments'):
    print(f"Attachments: {reader.attachments}")

# Check for embedded files
try:
    for name in reader.embedded_file_names:
        print(f"Embedded file: {name}")
except Exception as e:
    print(f"No embedded files: {e}")

# Try to get the document info
print(f"\nDocument info:")
print(f"Title: {reader.metadata.get('/Title')}")
print(f"Author: {reader.metadata.get('/Author')}")
print(f"Subject: {reader.metadata.get('/Subject')}")
print(f"Creator: {reader.metadata.get('/Creator')}")
print(f"Producer: {reader.metadata.get('/Producer')}")