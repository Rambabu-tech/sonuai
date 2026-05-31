from pdfminer.high_level import extract_text

pdf_path = "resume/resume.pdf"
txt_path = "resume/resume.txt"

text = extract_text(pdf_path)

with open(txt_path, "w") as f:
    f.write(text)

print("✅ Clean resume text saved to resume/resume.txt")