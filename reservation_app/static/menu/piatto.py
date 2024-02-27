import sys
import csv
import io

from bs4 import BeautifulSoup

css = open('style.css').read()
csv = csv.DictReader(io.open(sys.argv[1], "r", encoding = "utf-8-sig"))

categories = []
rawItems = []
for item in csv:
    rawItems.append(item)
    category = item["item_category"]
    if category not in categories:
        categories.append(category)


list = dict()
for category in categories:
    categoryItems = []
    for item in rawItems:
        itemCategory = item["item_category"]
        if category == itemCategory:
            categoryItems.append(item)
    list[category] = categoryItems


html = "<style>" + css + "</style>"
# html+= "<div class=\"menu-title\">"+ "Speisekarte"  + "</div>"
html += "<div class=\"menu-body\">"

# html+= "<hr class=\"h_line\">"
for category in categories:
    items = list[category]

    html+= "<div class=\"menu-section\"><h2 class=\"menu-section-title\">" + category + "</h2>"

    for item in items:
        description = item["item_description"]
        if item["item_vegan"] == "TRUE":
            description += "(Vegan)"
        if item["item_glutenfree"] == "TRUE":
            description += "(Gluten-Free)"


        html += "<div class=\"menu-item\">"

        html += "<div class=\"menu-item-name\">" + item["item_name"] + "</div>"
        html += "<div class=\"menu-item-price\">€" + item["item_price"] + "</div>"
        html += "<div class=\"menu-item-description\">" + description
        if (item == items[-1]) and (category==categories[-1]):
            html += "<br>"
            html += "<br>"
            html += "<br>"
            html += "<br>"
            html += "<br>"
            html += "<br>"
            html += "<br>"
            html += "<br>"

        html += "</div>"
        html += "</div>"


    html += "</div>"

html += "</div>"


soup = BeautifulSoup(html, "html.parser")

html = soup.prettify()

input_file_path = sys.argv[3]
output_file_path = sys.argv[2]

with open(input_file_path, "r") as input_file:
    content = input_file.read()


new_content = content + html + '{% endblock %}'

with open(output_file_path, "w") as output_file:
    output_file.write(new_content)

