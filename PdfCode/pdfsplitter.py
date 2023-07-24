import os
import PyPDF2

from langchain.document_loaders import DirectoryLoader, TextLoader

# Specify the directory for the text files
directory_path = "data"

# Expand the user's home directory
directory_path = os.path.expanduser(directory_path)

# Make sure the directory exists
os.makedirs(directory_path, exist_ok=True)

companyname = "schw"

# Open the PDF file
with open(f"../PdfCode/{companyname}-10k.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    pages_text = []

    # Read each page
    for page in reader.pages:
        pages_text.append(page.extract_text())

# Split the document into sections and save each one as a separate file
for i, section in enumerate(pages_text):
    with open(os.path.join(directory_path, f"section_{i}.{companyname}.txt"), "w") as file:
        file.write(section)

# Now, you can use DirectoryLoader
loader = DirectoryLoader(directory_path)

