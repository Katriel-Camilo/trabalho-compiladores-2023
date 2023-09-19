import re

fullHTML = """<html>
<head>
   <title>replit</title>
 </head>
<body>
  <p>Hello world</p>
  <h1 style="font-size:30px;">Olá, Eu sou uma página </h1>
  <div id="teste" style="color:black;">Unipinhal</div>
</body>
</html>"""

tags = []
currentTag = ""
state = 0

for c in fullHTML:
    if state == 1 and c != '>':
        currentTag = str(currentTag) + str(c)
    if c == '<' :
        state = 1
    if c == '>':
        tags.append(currentTag)
        currentTag = ""
        state = 3

print(tags)