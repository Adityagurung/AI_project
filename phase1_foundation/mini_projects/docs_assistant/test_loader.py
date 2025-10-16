"""
Quick test of the Document Loader
"""
import sys
from pathlib import Path

# Add to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from document_loader import DocumentLoader

print("="*60)
print("TESTING DOCUMENT LOADER")
print("="*60)

# Initialize loader
loader = DocumentLoader()

# Load all documents
print("\n1. Loading all documents...")
documents = loader.load_all_documents()

print(f"\n✅ Loaded {len(documents)} documents!")

# Show summary
print("\n2. Document Summary:")
summary = loader.get_document_summary(documents)
print(f"   Total documents: {summary['total_documents']}")
print(f"   By type: {summary['by_type']}")
print(f"   Total size: {summary['total_size_mb']} MB")

# Show each document
print("\n3. Document Details:")
for i, doc in enumerate(documents, 1):
    meta = doc['metadata']
    content_preview = doc['content'][:100].replace('\n', ' ')
    print(f"\n   Document {i}:")
    print(f"   Filename: {meta['filename']}")
    print(f"   Type: {meta['type']}")
    print(f"   Size: {meta['size_bytes']} bytes")
    print(f"   Preview: {content_preview}...")

print("\n" + "="*60)
print("✅ Document Loader Test Complete!")
print("="*60)