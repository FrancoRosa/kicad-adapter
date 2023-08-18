from sexpdata import loads, dumps
import json

with open('locations.json', "r") as json_file:
    locations = json.load(json_file)


with open('demo/demo.kicad_pcb', "r") as file:
    data = file.read()

z = loads(data)
for i in z:
    if str(i[0]) == 'footprint':
        for index, j in enumerate(i):

            if str(j[0]) == 'fp_text' and str(j[1]) == 'reference':
                key = j[2]
                i[4][1] = locations[key][0]
                i[4][2] = locations[key][1]

with open("demo.kicad_pcb", "w") as file:
    payload = dumps(z, space_around_lists=True)
    payload = payload.replace(' (', '\n (')
    file.write(payload)
