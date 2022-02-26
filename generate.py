# %% init
import csv
from utils.downloadCSV import downloadCSV
from datetime import datetime

X_OFFSET = 0
Y_OFFSET = 1
INDEX_CUE_NAMES = True
AUTO_DOWNLOAD_URL = "https://docs.google.com/spreadsheets/d/1VwNL2EPMhK5zRUr6NZi1qAGercA4MiS_ut-nJdugD_A/edit?usp=sharing"
AUTO_DOWNLOAD_FILENAME = "Matilda SCS - Sheet1.csv"
SHOW_NAME = "Matilda"

with open("base.scs11.xml") as file:
    baseScs11 = file.read()

# %% load file
autoDownload = input(f"Auto download? [{AUTO_DOWNLOAD_FILENAME}] (y/n): ") == "y"

if autoDownload:
    downloadCSV(AUTO_DOWNLOAD_URL)
    csvFileName = AUTO_DOWNLOAD_FILENAME
else:
    csvFileName = input("Input File (csv): ")

with open("input/" + csvFileName) as file:
    spreadsheet = list(csv.reader(file, quotechar='"'))[Y_OFFSET:]

columns = list(zip(*spreadsheet))[X_OFFSET:]

print("File loaded successfully, generating SCS...")

# %% get mic numbers and scenes
micNumbers = [int(x) for x in columns[0][1:]]
scenes = [
    {
        "index": index,
        "name": column[0],
        "mics": [presentActor.strip() == "" for presentActor in column[1:]],
    }
    for index, column in enumerate(columns[1:])
]

# %% generate data for SCS
cues = []
for scene in scenes:
    cue = {
        "cueId": "Q" + str((scene["index"] + 1)),
        "description": (str(scene["index"] + 1) + ". " if INDEX_CUE_NAMES else "")
        + scene["name"],
        "muteCues": [],
    }
    for i in range(len(micNumbers)):
        cue["muteCues"].append(
            {
                "controlNumber": micNumbers[i] - 1,
                "level": 0 if scene["mics"][i] else 127,
            }
        )
    cues.append(cue)


# %% generate output
output = ""
for cue in cues:
    muteSubCueString = ""
    for muteCue in cue["muteCues"]:
        muteSubCueString += f"""
            <ControlMessage>
                <CMLogicalDev>MIDI</CMLogicalDev>
                <MSMsgType>CC</MSMsgType>
                <MSChannel>2</MSChannel>
                <MSParam1>{muteCue["controlNumber"]}</MSParam1>
                <MSParam2>{muteCue["level"]}</MSParam2>
            </ControlMessage>
"""
    muteSubCueString = f"""
        <Sub>
            <SubType>M</SubType>
            <SubDescription>Mute Actors</SubDescription>
            <DefSubDes>1</DefSubDes>
            {muteSubCueString}
        </Sub>
"""
    output += f"""
    <Cue>
        <CueId>{cue["cueId"]}</CueId>
        <Description>{cue["description"]}</Description>
        {muteSubCueString}
    </Cue>
"""

output = baseScs11.replace("<!-- CUES -->", output)

print("SCS generated successfully")

# %% save output
outputFileName = (
    "output/" + f"{SHOW_NAME} {datetime.now().strftime('%d %b %H%M%S')}.scs11"
)
with open(outputFileName, "w") as file:
    file.write(output)

print(f"SCS saved to {outputFileName}")
