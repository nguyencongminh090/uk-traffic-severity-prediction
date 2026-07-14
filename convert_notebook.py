import json

with open("UK_accidents.ipynb", "r") as f:
    nb = json.load(f)

# Add comment block to first code cell
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        cell["source"] = ["# ORIGINAL ENVIRONMENT: Google Colab\n", "# CONVERTED FOR: Local Python 3.13\n\n"] + cell["source"]
        break

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        new_source = []
        for line in cell["source"]:
            if "!pip" in line or "!apt-get" in line or "google.colab" in line or "files.download" in line:
                new_source.append("# " + line)
            else:
                line = line.replace("/content/UK_accidents_balanced.csv", "dataset/UK_accidents_balanced.csv")
                new_source.append(line)
        cell["source"] = new_source

with open("UK_accidents_local.ipynb", "w") as f:
    json.dump(nb, f, indent=1)
