# python piatto.py menu.csv ../../templates/karte.html ../../templates/karte_base.html drinks.csv
import sys
import csv
import io

from bs4 import BeautifulSoup

css = open('style.css').read()
csv1 = csv.DictReader(io.open(sys.argv[1], "r", encoding = "utf-8-sig"))

categories = []
rawItems = []
for item in csv1:
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
html += "<div class=\"wrapper\" style=\"background-color: var(--body_background);box-shadow: none;\">"
html += "<div class=\"form-container\" >"
html += "<div class=\"slide-controls\" style=\"box-shadow: none;\">"
html += "<input type=\"radio\" name=\"slide\" id=\"login\" checked>"
html += "<input type=\"radio\" name=\"slide\" id=\"signup\">"
html += "<label for=\"login\" class=\"slide login\" style=\"font-size: 3vh\">Speise</label>"
html += "<label for=\"signup\" class=\"slide signup\" style=\"font-size: 3vh\">Getränke</label>"
html += "<div class=\"slider-tab\"></div>"
html += "</div>"

html += "<div class=\"form-inner\">"
html += "<form method=\"POST\" action=\"{% url 'create_book'%}\" class=\"login\">"

html += "<div class=\"menu-body\">"

# html+= "<hr class=\"h_line\">"
for category in categories:
    items = list[category]

    html+= "<div class=\"menu-section\"><h2 class=\"menu-section-title\">" + category + "</h2>"

    for item in items:
        description = item["item_description"]
        # if item["item_vegan"] == "TRUE":
        #     description += "(Vegan)"
        # if item["item_glutenfree"] == "TRUE":
        #     description += "(Gluten-Free)"


        html += "<div class=\"menu-item\">"

        html += "<div class=\"menu-item-name\">" + item["item_name"] + "</div>"
        html += "<div class=\"menu-item-price\">" + item["item_price"] + "</div>"
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


csv2 = csv.DictReader(io.open(sys.argv[4], "r", encoding = "utf-8-sig"))

categories = []
rawItems = []
for item in csv2:
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

html +=  "</form>"
html +=  "    <form method=\"POST\" action=\"{% url 'create_book'%}\" class=\"signup\">"

html += "<div class=\"menu-body\">"

# html+= "<hr class=\"h_line\">"
for category in categories:
    items = list[category]

    html+= "<div class=\"menu-section\"><h2 class=\"menu-section-title\">" + category + "</h2>"

    for item in items:
        description = item["item_description"]
        # if item["item_vegan"] == "TRUE":
        #     description += "(Vegan)"
        # if item["item_glutenfree"] == "TRUE":
        #     description += "(Gluten-Free)"


        html += "<div class=\"menu-item\">"
        if item["item_name"]=="":
            html += "<br>"
        html += "<div class=\"menu-item-name\">" + item["item_name"] + "</div>"
        html += "<div class=\"menu-item-price\">" + item["item_price_big"] + "</div>"
        html += "<div class=\"menu-item-price menu-item-price1\">" + item["item_price"] + "</div>"
        if item["item_name"]!="":
            html += "<div class=\"menu-item-description\">" + description
            html += "</div>"
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



html +="</form>"
      
html +=   "</div>"
html += "</div>"

html +="</div>"

html += "<script>"
html += "const loginText = document.querySelector(\".title-text .login\");"
html += "const loginForm = document.querySelector(\"form.login\");"
html += "const loginBtn = document.querySelector(\"label.login\");"
html += "const signupBtn = document.querySelector(\"label.signup\");"
html += "const signupLink = document.querySelector(\"form .signup-link a\");"
html += "signupBtn.onclick = () => {"
html += "  loginForm.style.marginLeft = \"-50%\";"
html += "  loginText.style.marginLeft = \"-50%\";"
html += "};"
html += "loginBtn.onclick = () => {"
html += "  loginForm.style.marginLeft = \"0%\";"
html += "  loginText.style.marginLeft = \"0%\";"
html += "};"
html += "signupLink.onclick = () => {"
html += "  signupBtn.click();"
html += "  return false;"
html += "};"
html += "</script>"


# soup = BeautifulSoup(html, "html.parser")

# html = soup.prettify()

input_file_path = sys.argv[3]
output_file_path = sys.argv[2]

with open(input_file_path, "r") as input_file:
    content = input_file.read()


new_content = content + html + '{% endblock %}'

with open(output_file_path, "w") as output_file:
    output_file.write(new_content)

