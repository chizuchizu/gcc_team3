from reportlab.pdfgen import canvas
import json
from datetime import datetime

def stringBuilder(data):
    output = "GCC 2024 - Group 3\n\n"
    for platform in data:
        output += platform + " Details\n"
        for detail in data[platform]:
            output += detail + ":  " + str(data[platform][detail]) + '\n'
        output += '\n\n'
    return output

def create_pdf(data, filepath="./page/data.pdf"):
    c = canvas.Canvas(filepath)
    dataString = stringBuilder(data)
    t = c.beginText()
    t.setTextOrigin(100, 750)
    t.textLines(f"""{dataString}""")
    c.drawText(t)
    c.drawString(400, 100, datetime.now().strftime("%d %B, %Y - %H:%M:%S"))
    c.save()

if __name__ == "__main__":
    with open('data.json', 'r') as f:
        data = json.load(f)
        create_pdf(data)


