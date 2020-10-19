import os
import sys


def search_readme(path):
    README_list = []
    dir_list = [path]

# search README.md files
    while dir_list:
        current_work_dir = dir_list[0]
        dir_list.pop(0)
        for filename in os.listdir(current_work_dir):
            absolute_item_path = current_work_dir + "/" + filename
            if os.path.isdir(absolute_item_path):
                dir_list.append(absolute_item_path)
            elif filename == "README.md":
                README_list.append(current_work_dir + "/" + filename)
    return README_list


def get_catalog_info(path):
    catalog = []
    for filename in os.listdir(path):
        if filename == "README.md":
            pass
        elif filename.endswith(".md"):
            catalog.append('[' + filename.strip('.md') + '](' + filename.strip('.md') + '.html)')
        elif os.path.isdir(path+'/'+filename):
            catalog.append('[' + filename + '](' + filename + '/index.html)')
    return catalog


def auto_generate_catalog(path):
    readme_list = search_readme(path)
    for readme_file_path in readme_list:
        catalog = get_catalog_info(readme_file_path.strip("README.md"))
        with open(readme_file_path, 'a+',encoding='utf8') as f:
            f.write("\n\n")
            f.write("以下为由代码自动生成的索引\n\n")
            for item in catalog:
                f.write('* '+ item + '\n')

        print("-------auto append the index for README file: " + readme_file_path+"---------")
