import csv
import pyproj

from sexpdata import loads
from json import dumps

print('...building paths')

source_epsg = 'EPSG:3670' 
target_epsg = 'EPSG:4326'
transformer = pyproj.Transformer.from_crs(source_epsg, target_epsg, always_xy=True)

def translate(x,y):
    return transformer.transform(x, y)

def get_avr(path):

    sum_e = 0
    sum_n = 0
    count = 0

    # Read and process the CSV file
    with open(path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            e_value = float(row["e"])
            n_value = float(row["n"])

            sum_e += e_value
            sum_n += n_value
            count += 1

    # Calculate the average values
    avg_e = round(sum_e / count, 1)
    avg_n = round(sum_n / count, 1)
    return avg_e, avg_n


with open('demo/demo.kicad_pcb', "r") as file:
    data = file.read()

e_avr, n_avr = get_avr('254_piles.csv')

z = loads(data)
nets = {}
for i in z:
    if str(i[0]) == 'segment':
        start = translate(i[1][1]+e_avr, i[1][2]+n_avr)
        end = translate(i[2][1]+e_avr, i[2][2]+n_avr)
        width = i[3][1]
        net = i[5][1]
        if net in nets:
            nets[net]["paths"].append(
                [start, end]
            )
        else:
            nets[net] = {
                "width": width,
                "paths": [[start, end]]
            }


with open("paths.json", 'w') as file:
    # Write some content to the file
    file.write(dumps(nets, indent=2))
print('...done')
