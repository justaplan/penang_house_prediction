import requests
import os


url_template = "https://www.iproperty.com.my/sale/penang/all-residential/?page={}"
first_page = 1
last_page = 200

# This loop is designed to not download a page again based on page ID.
# That means all pages must be downloaded in one go to prevent missing
# or duplicate entries.
for counter in range(first_page, last_page+1):
    page_out = "iproperty_kl/page_{}.html".format(counter)
    if os.path.exists(page_out):
        continue

    print("Processing page {} ...".format(counter))

    url = url_template.format(counter)
    response = requests.get(url)

    if response.status_code != 200:
        print("FAILED to process page {} ...".format(counter))
        continue

    with open(page_out, "w") as f:
        f.write(response.text)
    print("Done processing and waiting ...".format(counter))
    time.sleep(5)