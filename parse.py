
def parsepdf(file):
    try:
        import PyPDF2
    except ImportError:
        raise ValueError("PyPDF2 is required to read PDF files.")

    text_list = []

    with open(file, "rb") as f:       
        pdf = PyPDF2.PdfReader(f)

        # Iterate over every page
        for page in pdf.pages:
            # Extract the text from the page
            page_text = page.extract_text()
            text_list.append(page_text)

        text = "\n".join(text_list)

        return text
