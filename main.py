import json
import csv
import math
import matplotlib.pyplot as plt

with open("dendrite-labels.json", "r") as input_file:
    data = json.load(input_file)

# Create list to store labels for each image
labels = [[] for _ in range(len(data))]
# Loop through each image
for i in range(len(data)):
    # Parse image index
    image_url = data[i]["Labeled Data"]
    start = image_url.find("data-") + 5
    image_index = int(image_url[start : image_url.find(".", start)]) - 1
    # Loop through labels for current image
    for label in data[i]["Label"]["objects"]:
        if label["value"] == "dendrite":
            labels[image_index].append(("dendrite", label["line"]))
        if label["value"] == "neuron":
            labels[image_index].append(("neuron", label["bbox"]))

total_dendrite_count = 0
total_neuron_count = 0
all_dendrite_lengths = []
average_dendrite_lengths = []
# Output CSV file of the dendrite properties for each image
# Dendrite properties include quantity, average length, and lengths
with open("dendrite-properties.csv", "w", encoding = "UTF8") as properties_file:
    writer = csv.writer(properties_file)
    header = ["Image #", "# of Neuron Labels", "# of Dendrite Labels", "Average Dendrite Length (in pixels)", "Dendrite Lengths (in pixels)"]
    writer.writerow(header)
    # Loop through each image's labels
    for image_index in range(len(labels)):
        dendrite_count = 0
        dendrite_lengths = []
        for label in labels[image_index]:
            (label_type, label_value) = label
            if label_type == "dendrite":
                dendrite_count += 1
                dendrite_length = 0 
                # Find sum of distances between each pair of points
                for i in range(1, len(label_value)):
                    dendrite_length += round(math.sqrt((label_value[i]["y"] - label_value[i - 1]["y"]) ** 2 + (label_value[i]["x"] - label_value[i - 1]["x"]) ** 2))
                dendrite_lengths.append(dendrite_length)
        # Calculate dendrite properties
        neuron_count = len(labels[image_index]) - dendrite_count
        average_dendrite_length = round(sum(dendrite_lengths) / len(dendrite_lengths), 3)
        writer.writerow([image_index + 1, neuron_count, dendrite_count, average_dendrite_length, dendrite_lengths])
        total_dendrite_count += dendrite_count
        total_neuron_count += neuron_count
        all_dendrite_lengths.extend(dendrite_lengths)
        average_dendrite_lengths.append(average_dendrite_length)

# Output CSV file summarizing data
with open("dendrite-overview.txt", "w") as overview_file:
    overview_file.write(f"Dendrite Data Overview:\n")
    overview_file.write(f"Total # of Images: {len(labels)}\n")
    total_labels_count = total_dendrite_count + total_neuron_count
    overview_file.write(f"Total # of Labels: {(total_labels_count)}\n")
    overview_file.write(f"Total # of Neuron Labels: {total_neuron_count}\n")
    overview_file.write(f"Total # of Dendrite Labels: {total_dendrite_count}\n")
    overview_file.write(f"Average # of Neuron Labels Per Image: {round(total_neuron_count / len(labels), 3)}\n")
    overview_file.write(f"Average # of Dendrite Labels Per Image: {round(total_dendrite_count / len(labels), 3)}\n")
    overview_file.write(f"Overall Average Dendrite Length (in pixels) {round(sum(all_dendrite_lengths) / len(all_dendrite_lengths), 3)}\n")

# Plot average dendrite length for each image
image_numbers = list(range(1, len(labels) + 1))
plt.bar(image_numbers, average_dendrite_lengths)
plt.title("Average Dendrite Length Per Image")
plt.xlabel("Image #")
plt.ylabel("Average Dendrite Length (in pixels)")
plt.show()