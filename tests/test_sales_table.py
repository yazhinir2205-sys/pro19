import os
import sys
from bs4 import BeautifulSoup


FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "starter",
    "index.html"
)

TOTAL_MARKS = 50
score = 0


def award(marks, message):
    global score
    score += marks
    print(f"PASS +{marks}: {message}")


def fail(message):
    print(f"FAIL  0: {message}")


# =========================================================
# Load file
# =========================================================

if not os.path.exists(FILE):
    print("ERROR: starter/index.html not found.")
    sys.exit(1)

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

style = soup.find("style")
css = style.get_text(" ", strip=True) if style else ""


# =========================================================
# 1. HTML DOCUMENT STRUCTURE - 5 MARKS
# =========================================================

print("\n[1] HTML DOCUMENT STRUCTURE")

if soup.find("html"):
    award(1, "<html> exists")
else:
    fail("<html> is missing")

if soup.find("head"):
    award(1, "<head> exists")
else:
    fail("<head> is missing")

if soup.find("body"):
    award(1, "<body> exists")
else:
    fail("<body> is missing")

title = soup.find("title")

if title and title.get_text(strip=True) == "Sales table as a figure":
    award(2, "Correct page title")
else:
    fail("Incorrect page title")


# =========================================================
# 2. FIGURE AND CAPTION - 8 MARKS
# =========================================================

print("\n[2] FIGURE AND CAPTION")

figure = soup.find("figure")

if figure:
    award(3, "<figure> exists")
else:
    fail("<figure> is missing")

figcaption = soup.find("figcaption")

if figcaption:
    award(2, "<figcaption> exists")
else:
    fail("<figcaption> is missing")

if (
    figcaption
    and figcaption.get_text(" ", strip=True)
    == "Total Sales by Book"
):
    award(3, "Correct figure caption")
else:
    fail("Caption should be 'Total Sales by Book'")


# =========================================================
# 3. TABLE STRUCTURE - 7 MARKS
# =========================================================

print("\n[3] TABLE STRUCTURE")

table = soup.find("table")

if table:
    award(2, "<table> exists")
else:
    fail("<table> is missing")

thead = soup.find("thead")
tbody = soup.find("tbody")
tfoot = soup.find("tfoot")

if thead:
    award(1, "<thead> exists")
else:
    fail("<thead> is missing")

if tbody:
    award(1, "<tbody> exists")
else:
    fail("<tbody> is missing")

if tfoot:
    award(1, "<tfoot> exists")
else:
    fail("<tfoot> is missing")

headers = []

if thead:
    headers = [
        th.get_text(" ", strip=True)
        for th in thead.find_all("th")
    ]

expected_headers = [
    "Book",
    "Year Published",
    "Sales"
]

if headers == expected_headers:
    award(2, "Correct table headings")
else:
    fail(f"Expected headings: {expected_headers}")


# =========================================================
# 4. SALES DATA - 10 MARKS
# =========================================================

print("\n[4] SALES DATA")

expected_data = [
    ("PHP and MySQL", "2014", "$372,381"),
    ("JavaScript and jQuery", "2015", "$305,447"),
    ("Java Programming", "2011", "$392,444"),
    ("Java Servlets and JSP", "2014", "$328,992"),
    ("ASP.NET with Visual Basic", "2011", "$351,200"),
    ("ASP.NET with C#", "2011", "$404,332"),
]

body_rows = tbody.find_all("tr") if tbody else []

actual_data = []

for row in body_rows:
    cells = row.find_all("td")

    if len(cells) == 3:
        actual_data.append(
            tuple(
                cell.get_text(" ", strip=True)
                for cell in cells
            )
        )

if len(body_rows) == 6:
    award(2, "Exactly six employee/book rows")
else:
    fail("There must be exactly six book rows")

matched = 0

for expected in expected_data:
    if expected in actual_data:
        matched += 1

if matched == 6:
    award(8, "All six book records are correct")
elif matched > 0:
    marks = round((matched / 6) * 8)
    award(marks, f"{matched}/6 book records are correct")
else:
    fail("Book data is incorrect")


# =========================================================
# 5. CSS - 10 MARKS
# =========================================================

print("\n[5] CSS")

css_checks = [
    ("border: 1px solid black", 2,
     "Figure/table border is defined"),

    ("width: 450px", 1,
     "Figure width is 450px"),

    ("padding: 15px", 1,
     "Figure padding is 15px"),

    ("font-weight: bold", 1,
     "Bold formatting is defined"),

    ("text-align: center", 1,
     "Centered text is defined"),

    ("border-collapse: collapse", 1,
     "Table border-collapse is defined"),

    ("background-color: aqua", 1,
     "Aqua header/footer is defined"),

    ("background-color: silver", 1,
     "Silver alternating rows are defined"),

    ("margin: 10px auto", 1,
     "Table is centered with margin"),
]

for keyword, marks, message in css_checks:
    if keyword in css:
        award(marks, message)
    else:
        fail(f"Missing CSS: {keyword}")


# =========================================================
# 6. ALIGNMENT AND ALTERNATING ROWS - 7 MARKS
# =========================================================

print("\n[6] ALIGNMENT")

if "text-align: right" in css:
    award(2, "Right alignment is defined")
else:
    fail("Right alignment is missing")

if "th:first-child" in css and "td:first-child" in css:
    award(2, "First column alignment rule exists")
else:
    fail("First column alignment rule is missing")

if "nth-child(2)" in css:
    award(1, "Second-column alignment rule exists")
else:
    fail("Second-column alignment rule is missing")

if "nth-child(2n)" in css:
    award(2, "Alternating tbody rows are styled")
else:
    fail("Alternating row selector is missing")


# =========================================================
# 7. FOOTER AND TOTAL - 3 MARKS
# =========================================================

print("\n[7] FOOTER")

if tfoot:
    footer_text = tfoot.get_text(" ", strip=True)

    if "Total Sales" in footer_text:
        award(1, "Footer contains Total Sales")
    else:
        fail("Footer label is incorrect")

    if "$2,154,786" in footer_text:
        award(2, "Correct total sales")
    else:
        fail("Total sales should be $2,154,786")


# =========================================================
# FINAL SCORE
# =========================================================

score = min(score, TOTAL_MARKS)

print("\n" + "=" * 60)
print("SALES TABLE AS A FIGURE - FINAL GRADE")
print("=" * 60)
print(f"SCORE: {score}/{TOTAL_MARKS}")

if score == TOTAL_MARKS:
    print("STATUS: PASS")
else:
    print("STATUS: REVIEW REQUIRED")

print("=" * 60)

sys.exit(0)
