import os


def merge_and_sort_txt_files(folder_name):
    print(f" ----------------- {folder_name.upper()} -----------------")

    # Pfade für Eingabe- und Ausgabedateien festlegen
    input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                f"input_{folder_name}"
                                )
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               f"combined_{folder_name}/combined_"
                               f"{folder_name}.txt"
                               )

    offline_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "offline_domains"
                                  )

    # Erstelle den Ausgabeordner, falls er nicht existiert
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    # Liste aller TXT-Dateien im Ordner erhalten
    txt_files = [file for file in os.listdir(input_folder) if
                 file.endswith(".txt")]

    # Liste aller TXT-Dateien im Ordner erhalten
    txt_files_offline = [file_off for file_off in os.listdir(offline_folder) if
                         (file_off.endswith(".txt") and file_off.startswith(
                                 f"output_{folder_name}"
                                 )
                          )]

    offline_domains = []
    if len(txt_files_offline) != 0:
        for txt_offline in txt_files_offline:
            with open(os.path.join(offline_folder, txt_offline), 'r'
                      ) as off_file:
                lines = off_file.readlines()
                for line in lines:
                    offline_domains.append(line)

        print(f"Loaded {len(offline_domains)} offline domains to be excluded.")

    else:
        print(f"Did not load offline domains to exclude.")

    # Öffne die Ausgabedatei im Schreibmodus
    with open(output_file, 'w') as outfile:
        # Durchlaufe jede TXT-Datei und füge ihre Zeilen zur Ausgabedatei hinzu
        for txt_file in txt_files:
            with open(os.path.join(input_folder, txt_file), 'r') as infile:

                for line in infile.readlines():
                    if line.startswith("#") or line.startswith("!"):
                        continue

                    if line.startswith("www."):
                        outfile.write(line.replace("www.", ""))
                    else:
                        outfile.write(line)

                # outfile.writelines(infile.readlines())

    # Öffne die Ausgabedatei im Lese- und Schreibmodus
    with open(output_file, 'r') as outfile:

        lines_out = [line.lstrip() for line in outfile.readlines()]

        if len(offline_domains) != 0:
            print(f"Before exclusion: "
                  f"{len(lines_out)}."
                  )

            remaining_out = set(lines_out) - set(offline_domains)

            print(f"After exclusion: "
                  f"{len(remaining_out)}."
                  )

        else:
            remaining_out = lines_out

        # Entferne Duplikate und sortiere die Zeilen alphabetisch
        unique_sorted_lines = sorted(list(set(remaining_out)))

    with open(output_file, "w") as fh_r:
        fh_r.writelines(unique_sorted_lines)

    with open(output_file, 'r') as f:
        domains = [line.lstrip() for line in f.readlines()]

        print(f"Die Datei combined_{folder_name}.txt enthält"
              f" {len(domains)} Websites."
              )

    print(f" ----------------------------------------")


if __name__ == "__main__":
    merge_and_sort_txt_files('good')
    merge_and_sort_txt_files('bad')
