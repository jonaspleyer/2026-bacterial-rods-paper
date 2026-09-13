import re
import argparse
import zipfile


def extract_input(line):
    m = re.search(r"\\input\{([^}]+)\}", line.strip())
    return m.group(1) if m else None


def extract_graphics(line):
    m = re.search(r"\\includegraphics\[([^}]+)\]\{([^}]+)\}", line.strip())
    return m.group(2) if m else None


def combine_tex_files():
    # Read main file
    full_text = []

    with open("main.tex", "r") as f:
        lines = f.readlines()

        # Find all input commands
        for line in lines:
            if "\\input" in line:
                fname = extract_input(line)
                fname = f"{fname}.tex"
                # Import everything from that file
                with open(fname, "r") as f2:
                    full_text.extend(f2.readlines())
            else:
                full_text.append(line)

    with open("main-combined.tex", "w") as f:
        f.writelines(full_text)


def zip_graphics():
    zipf = zipfile.ZipFile("archive.zip", "a", compression=zipfile.ZIP_DEFLATED)
    with open("main-combined.tex", "r") as f:
        for line in f.readlines():
            if "includegraphics" in line and line[0] != "%":
                fname = extract_graphics(line)
                if fname is not None:
                    zipf.write(fname)
    zipf.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    pyargs = parser.parse_args()

    if pyargs.command == "combine":
        combine_tex_files()

    if pyargs.command == "zip_graphics":
        zip_graphics()
