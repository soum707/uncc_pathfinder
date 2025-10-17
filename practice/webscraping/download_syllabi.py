import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re

# Base info
base_page = "https://datascience.charlotte.edu/academics/syllabi/"
domain = "https://datascience.charlotte.edu"

# Output folder
output_folder = "syllabi_pdfs"
os.makedirs(output_folder, exist_ok=True)

course_links = []
missing_pdfs = []

# Step 1: Crawl through all paginated pages
page_number = 1
while True:
    page_url = base_page if page_number == 1 else f"{base_page}page/{page_number}/"
    print(f"\n📄 Fetching: {page_url}")
    res = requests.get(page_url)
    if res.status_code != 200:
        print("🔚 No more pages or failed to load.")
        break

    soup = BeautifulSoup(res.text, 'html.parser')
    found_any = False

    for a in soup.find_all("a", href=True):
        text = a.text.strip()
        if text.upper().startswith(("DTSC", "SPOA")):
            full_link = urljoin(domain, a["href"])
            course_links.append((text, full_link))
            print(f"🔗 Found course: {text}")
            found_any = True

    if not found_any:
        break
    page_number += 1

print(f"\n📚 Total course pages found: {len(course_links)}")

# Step 2: Visit each course page and try to find & download the PDF
for course_title, course_link in course_links:
    print(f"\n🔍 Visiting: {course_title} -> {course_link}")
    course_page = requests.get(course_link)
    sub_soup = BeautifulSoup(course_page.text, 'html.parser')

    pdf_found = False
    for a in sub_soup.find_all("a", href=True):
        href = a["href"]
        text = a.text.strip().lower()
        if href.endswith(".pdf") or "syllabus" in href.lower() or "syllabus" in text:
            pdf_link = urljoin(domain, href)
            # Sanitize file name
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", course_title.strip())[:80]
            filename = f"{safe_name}.pdf"
            save_path = os.path.join(output_folder, filename)

            if os.path.exists(save_path):
                print(f"✅ Already downloaded: {filename}")
            else:
                print(f"⬇️  Downloading: {filename}")
                try:
                    pdf_data = requests.get(pdf_link)
                    with open(save_path, "wb") as f:
                        f.write(pdf_data.content)
                    print(f"✅ Saved: {filename}")
                except Exception as e:
                    print(f"❌ Error downloading {pdf_link}: {e}")
            pdf_found = True
            break

    if not pdf_found:
        print(f"❌ No PDF found on: {course_link}")
        missing_pdfs.append(f"{course_title} -> {course_link}")

# Step 3: Report any missing PDFs
if missing_pdfs:
    print("\n🚫 The following course pages had NO downloadable PDF:")
    for m in missing_pdfs:
        print(m)
    with open(os.path.join(output_folder, "missing_pdfs.txt"), "w") as f:
        for m in missing_pdfs:
            f.write(m + "\n")
else:
    print("\n✅ All course pages had PDFs!")


