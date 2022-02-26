import yaml

with open(input("Input File: ")) as file:
    cues = yaml.load(file, Loader=yaml.FullLoader)

output = []

for i, cue in enumerate(cues):
    keys = list(cue.keys())
    values = list(cue.values())
    keys.insert(1, "progchange")
    values.insert(1, i+1)
    output.append(dict(zip(keys, values)))

with open(input("Write to: ")+".yml", "w") as file:
    file.write(yaml.dump(output, sort_keys=False).replace("\n-", "\n\n-"))