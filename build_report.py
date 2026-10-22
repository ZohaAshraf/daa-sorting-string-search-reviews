import os
import re
from fpdf import FPDF
from PIL import Image

# ====== EDIT THESE ======
NAME = "Zoha Ashraf"          # change if your name is different
ROLL_NO = "24F-3019"      # put your real roll number
# ========================

OUT = "report/DAA_Assignment3_Report.pdf"

SHOTS = [
    ("report/part0_output.png",   "Part 0: Data Preparation output"),
    ("report/task1_1_output.png", "Task 1.1: Heap Sort and Top 10"),
    ("report/task2_1_output.png", "Task 2.1: Counting Sort on Score"),
    ("report/task2_2_output.png", "Task 2.2: Radix Sort (Base-10 vs Base-256)"),
    ("report/task2_3_output.png", "Task 2.3: Bucket Sort on ratio"),
    ("report/task3_1_output.png", "Task 3.1: Naive vs KMP"),
    ("report/task3_2_output.png", "Task 3.2: Rabin-Karp"),
    ("report/task4_1_output.png", "Task 4.1: Gluten Free pipeline"),
]


def clean(t):
    """fpdf core fonts only support latin-1, so swap fancy characters."""
    t = (t.replace("\u2019", "'").replace("\u2018", "'")
          .replace("\u201c", '"').replace("\u201d", '"')
          .replace("\u2013", "-").replace("\u2014", "-")
          .replace("\u2192", "->").replace("\u2026", "..."))
    t = t.replace("**", "").replace("`", "")
    return t.encode("latin-1", "replace").decode("latin-1")


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, "Page %d" % self.page_no(), align="C")


def line(pdf, text, h=6):
    pdf.multi_cell(0, h, clean(text), new_x="LMARGIN", new_y="NEXT")


pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(10, 10, 10)

# ---------- cover page ----------
pdf.add_page()
pdf.ln(50)
pdf.set_font("Helvetica", "B", 18)
line(pdf, "National University of Computer and Emerging Sciences", 10)
pdf.set_font("Helvetica", "B", 16)
line(pdf, "CS2009 - Design and Analysis of Algorithms", 10)
pdf.set_font("Helvetica", "B", 22)
pdf.ln(5)
line(pdf, "Assignment 3", 12)
pdf.set_font("Helvetica", "", 13)
line(pdf, "Sorting and String Searching on Real Data", 8)
line(pdf, "Dataset: Amazon Fine Food Reviews", 8)
pdf.ln(15)
pdf.set_font("Helvetica", "", 14)
line(pdf, "Name: " + NAME, 9)
line(pdf, "Roll No: " + ROLL_NO, 9)
line(pdf, "Session: Fall 2026", 9)
line(pdf, "GitHub: github.com/ZohaAshraf/daa-sorting-string-search-reviews", 9)

# ---------- screenshots ----------
MAX_W, MAX_H = 190, 215
for path, title in SHOTS:
    if not os.path.exists(path):
        print("Skipping (not found):", path)
        continue
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 13)
    line(pdf, title, 8)
    pdf.ln(2)
    w, h = Image.open(path).size
    draw_w = MAX_W
    draw_h = draw_w * h / w
    if draw_h > MAX_H:
        draw_h = MAX_H
        draw_w = draw_h * w / h
    pdf.image(path, x=10, y=pdf.get_y(), w=draw_w, h=draw_h)

# ---------- concept answers from concepts.md ----------
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)
line(pdf, "Conceptual Answers", 10)
pdf.ln(2)

in_code = False
with open("report/concepts.md", encoding="utf-8") as f:
    for raw in f:
        s = raw.rstrip("\n")
        if s.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            pdf.set_font("Courier", "", 9)
            line(pdf, s if s else " ", 5)
            continue
        if not s.strip():
            pdf.ln(2)
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", s)
        if m:
            size = {1: 14, 2: 13, 3: 12}[len(m.group(1))]
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", size)
            line(pdf, m.group(2), 7)
            continue
        pdf.set_font("Helvetica", "", 11)
        if s.lstrip().startswith(("- ", "* ")):
            s = "  - " + s.lstrip()[2:]
        line(pdf, s, 6)

pdf.output(OUT)
print("Saved", OUT)