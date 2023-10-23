
def text_extractor(roi):

    ROIs = []
    with open(roi, "r") as file:
        # file_content = file.read()
        for line in file:
        # Split the input string using spaces and commas as separators
            numbers = [int(value) for part in line.split() for value in part.split(',') if value.isdigit()]
            ROIs.append(numbers)

    return ROIs