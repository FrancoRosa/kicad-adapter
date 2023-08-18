import csv
import uuid
from json import dumps

sch_template = """
(kicad_sch (version 20230121) (generator eeschema)

  (uuid cbbf253c-1d39-4ab0-857a-893ee81d0c6e)

  (paper "User" 1800 899.998)

  (lib_symbols
    (symbol "Connector:TestPoint" (pin_numbers hide) (pin_names (offset 0.762) hide) (in_bom yes) (on_board yes)
      (property "Reference" "TP" (at 0 6.858 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "TestPoint" (at 0 5.08 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (at 5.08 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (at 5.08 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "test point tp" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "test point" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_fp_filters" "Pin* Test*" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "TestPoint_0_1"
        (circle (center 0 3.302) (radius 0.762)
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
      (symbol "TestPoint_1_1"
        (pin passive line (at 0 0 90) (length 2.54)
          (name "1" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )
  )

  {}
  
  (sheet_instances
    (path "/" (page "1"))
  )
)

"""

sym_template = """
(symbol (lib_id "Connector:TestPoint") (at {} {} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced)
    (uuid {})
    (property "Reference" "{}" (at {} {} 0)
      (effects (font (size {} {})) (justify left))
    )
    (property "Value" "TestPoint" (at 128.27 97.028 0)
      (effects (font (size 1 1)) (justify left) hide)
    )
    (property "Footprint" "TestPoint:TestPoint_Pad_D1.0mm" (at 130.81 99.06 0)
      (effects (font (size 1 1)) hide)
    )
    (property "Datasheet" "~" (at 130.81 99.06 0)
      (effects (font (size 1 1)) hide)
    )
    (pin "1" (uuid {}))
    (instances
      (project "demo"
        (path "/c9cd55e0-13a0-48e0-a327-2bac1234e146"
          (reference "{}") (unit 1)
        )
      )
    )
  )

"""

locations = {}


def generate_points(cols, rows, start_x, start_y, gap):
    points = []
    for col in range(cols):
        for row in range(rows):
            points.append([start_x+col*gap,
                           start_y + row*gap])

    return points


def generate_syms(points, template, label, size):
    text = ""
    for (index, point) in enumerate(points):
        x = point[0]
        y = point[1]
        label_x = point[0]+1
        label_y = point[1]+1
        uuid_1 = uuid.uuid4()
        name = f"{label}{index}"
        text = text + template.format(x, y, uuid_1,
                                      name, label_x, label_y, size, size, uuid_1, name)
        locations[name] = [x, y]

    return text


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


def get_points(path):
    points = []
    e_avr, n_avr = get_avr('block_254.csv')

    with open(path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            e_value = float(row["e"])
            n_value = float(row["n"])
            x = round(e_value-e_avr, 1)
            y = round(n_value-n_avr, 1)
            points.append([x, y])

    return points


piles = get_points('block_254.csv')
inverters = get_points('inv_254.csv')

payload = generate_syms(piles, sym_template, "PILE", 0.5) + generate_syms(
    inverters, sym_template, "INV", 1.5)

with open("demo.kicad_sch", "w") as file:
    file.write(sch_template.format(payload))

with open("locations.json", "w") as file:
    file.write(dumps(locations))
