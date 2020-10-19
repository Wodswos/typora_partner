import os


def search_markdown_files(path):
    sub_dir_list = [path]
    markdown_list = []
    while sub_dir_list:
        current_work_dir = sub_dir_list[0]
        sub_dir_list.pop(0)

        for sub_item in os.listdir(current_work_dir):
            absolute_item_path = current_work_dir + "\\" + sub_item
            if os.path.isdir(absolute_item_path):
                print("Find and add a subdir: " + absolute_item_path)
                sub_dir_list.append(absolute_item_path)
            else:
                if sub_item.endswith(".md"):
                    markdown_list.append(current_work_dir + "\\" + sub_item)
    return markdown_list


def text_replace(path,replace_pairs_dict):
    markdown_file_list = search_markdown_files(path)
    for file in markdown_file_list:
        with open(file, 'r+', encoding='utf8') as f:
            text = f.read()
            print(text)
            for item in replace_pairs_dict:
                text = text.replace(item, replace_pairs_dict[item])
            f.seek(0)
            f.truncate()
            f.write(text)
            print("Complete the replace task of " + file)