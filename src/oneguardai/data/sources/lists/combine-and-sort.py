import os

def merge_and_sort_txt_files():
    # Pfade für Eingabe- und Ausgabedateien festlegen
    input_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(input_folder, 'output')
    output_file = os.path.join(output_folder, 'output.txt')

    # Erstelle den Ausgabeordner, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Liste aller TXT-Dateien im Ordner erhalten
    txt_files = [file for file in os.listdir(input_folder) if file.endswith('.txt')]

    # Öffne die Ausgabedatei im Schreibmodus
    with open(output_file, 'w') as outfile:
        # Durchlaufe jede TXT-Datei und füge ihre Zeilen zur Ausgabedatei hinzu
        for txt_file in txt_files:
            if txt_file != 'output.txt':  # Vermeide, die Ausgabedatei selbst zu verarbeiten
                with open(os.path.join(input_folder, txt_file), 'r') as infile:
                    outfile.writelines(infile.readlines())

    # Öffne die Ausgabedatei im Lese- und Schreibmodus
    with open(output_file, 'r+') as outfile:
        # Entferne Duplikate und sortiere die Zeilen alphabetisch
        unique_sorted_lines = sorted(set(outfile.readlines()))
        
        # Position in der Datei auf den Anfang setzen
        outfile.seek(0)
        
        # Schreibe die eindeutigen und sortierten Zeilen zurück in die Datei
        outfile.writelines(unique_sorted_lines)

if __name__ == "__main__":
    merge_and_sort_txt_files()
