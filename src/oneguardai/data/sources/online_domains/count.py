import os

current_dir = os.path.dirname(os.path.abspath(__file__))

files = ["output_bad_online_parallel.txt", "output_good_online_parallel.txt"]

for files in files:
    with open(os.path.join(current_dir, files), "r") as infile:
        lines = infile.readlines()
        count1 = len(lines)

        print(f"{files}: {count1} domains.")
