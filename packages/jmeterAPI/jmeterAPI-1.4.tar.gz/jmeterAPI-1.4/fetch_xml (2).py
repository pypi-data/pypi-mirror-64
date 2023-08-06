import os
from os.path import join


def fetch_xml_path(dir_path):
    path_here = os.getcwd()
    path_projects = os.path.join(path_here, "jmeter_api")
    file_list = ["include README.md LICENSE", "recursive-include tests *.py"]
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".xml"):
                path_xml = os.path.join(root,file)
                file_list.append(path_xml)
    with open("MANIFEST.in", "w") as file:
        [file.write(f"include {i}\n") for i in file_list]
    return file_list

print(fetch_xml_path(path_projects))
