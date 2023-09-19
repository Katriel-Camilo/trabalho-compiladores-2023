import re

fullHTML = """<html>
<head>
   <title>replit</title>
 </head>
<body>
  <p>Hello world</p>
  <h1 style="font-size:30px;">Olá, Eu sou uma página</h1>
  <div id="teste" style="color:black;">Unipinhal</div>
</body>
</html>"""

#Encontra o conteúdo interno das tags
def getTagsContent(htmlFile):
  currentTag = ''
  tagsContent = []
  state = 0
  for c in htmlFile:
      if state == 1 and c != '>':
          if c == '<':
             raise Exception("Erro sintático: Não é possível inicializar uma tag")
          currentTag = str(currentTag) + str(c)
      if c == '<' :
          state = 1
      if c == '>':
          tagsContent.append(currentTag)
          currentTag = ""
          state = 0
  if state == 1:
     raise Exception("Erro sintático: Finalizador de abertura de tag '>' não encontrado")
  return tagsContent

#Extrai o nome e encontra o nível das tags
def generateTagObjects(tags):
  #Último elemento
  isFirstTag = True
  tagObjects = []
  level = 0
  for tag in tags:
    tagAttrs = tag.split()
    tagName = tagAttrs[0]
    tagObj = {"name" : tagName,
              "attributes" : [],
              "level" : "",
              "childs" : [],
              }
    
    if isFirstTag:
       stack = [tagObj]
       isFirstTag = False

    for tagAttr in tagAttrs:
       if re.match("^[a-zA-Z0-9]+=\"([^\"]*)\"$", tagAttr.strip()):
          tagAttrSplitted = tagAttr.split("=", 1)
          tagAttrLabel = tagAttrSplitted[0]
          tagAttrValue = tagAttrSplitted[1]
          tagObj["attributes"].append({"label" : tagAttrLabel, "value" : tagAttrValue})
  
    if(tagObj["name"] == "/" + stack[-1]["name"]):
      level -= 1
      stack[-1]["level"] = level
      if not isFirstTag:
        stack[-2]["childs"].append(stack[-1])
      tagObjects.append(stack.pop())
    else:
      stack.append(tagObj)
      level += 1
  return tagObjects

tagObjects = generateTagObjects(getTagsContent(fullHTML))

for tagObject in tagObjects:
   print("Nome: " + tagObject["name"])
   print("Atributos: ")
   print(tagObject["attributes"])
   print("Level: " + str(tagObject["level"]))
   for child in tagObject["childs"]:
      print("Child: " + child["name"])
   print("======================")