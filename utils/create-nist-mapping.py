import pyexcel
import pprint

# Open the ODS file
data = pyexcel.get_array(file_name='stig.ods')

srgid_to_iacontrol = dict()

# Iterate over rows and print values of columns B, F, and G
for row in data[1:]:
    nist_controls = row[0]
    srg_ids = row[2]

    # Split the comma-separated values and strip extra whitespace
    for srg_id in [value.strip() for value in srg_ids.split(',')]:
        if srg_id not in srgid_to_iacontrol:
            srgid_to_iacontrol[srg_id] = set()
        [srgid_to_iacontrol[srg_id].add(value.strip()) for value in nist_controls.split(',')]


# Convert from set to a comma-separated string
for srg in srgid_to_iacontrol:
    srgid_to_iacontrol[srg] = ','.join(sorted(srgid_to_iacontrol[srg]))

pprint.pprint(srgid_to_iacontrol)