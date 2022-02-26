from xml.etree import ElementTree

# THIS SPLICER IS INDEX BASED - "Q" CUE INDICIES MUST MATCH IN BOTH FILES

with open(input("Splice into file: "), encoding="UTF-8") as file:
    target = ElementTree.parse(file)

with open(input("Splice from file: "), encoding="UTF-8") as file:
    source = ElementTree.parse(file)

sourceElements = {}

for element in source.getroot():
    if element.tag == "Cue":
        sourceElements[element.find("Description").text] = element

newTree = ElementTree.ElementTree()
newTree._setroot(ElementTree.Element(target.getroot().tag))

modified = 0
for element in target.getroot():
    if element.tag == "Cue" and element.find("Description").text in sourceElements:
        newTree.getroot().append(sourceElements[element.find("Description").text])
        modified += 1
    else:
        newTree.getroot().append(element)

print(f"Modified {modified} cue entries.")

with open(input("Save to file: ")+".scs11", "wb") as file:
    file.write(ElementTree.tostring(newTree.getroot(), encoding="UTF-8", method="xml", xml_declaration=True))