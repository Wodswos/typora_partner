import os
import json
import pypandoc
import paramiko


# 递归搜索、索引文件夹
def recursive_lookup_markdown(source_dir):
    dir_queue = [source_dir]
    markdown_list = []
    while dir_queue:
        current_work_dir = dir_queue[0]
        f = open(current_work_dir + "/README.md", "a+", encoding='utf8')
        f.write("\n\n")
        f.write("以下为由代码自动生成的索引\n\n")

        for filename in os.listdir(current_work_dir):
            item = current_work_dir + '/' + filename
            if os.path.isdir(item):
                dir_queue.append(item)
                f.write("- ["+filename+"]("+filename+"/index.html)\n")
            elif filename.endswith("README.md"):
                markdown_list.append(item)
            elif filename.endswith(".md"):
                markdown_list.append(item)
                f.write("- ["+filename.rstrip('.md')+"]("+filename.rstrip('.md')+".html)\n")
            else:
                f.write("- ["+filename+"]("+filename+")\n")
        f.close()
        dir_queue.pop(0)
    return markdown_list


def reformat(markdown_list, config):
    for item in markdown_list:
        with open(item, 'r+', encoding='utf8') as f:
            text = f.read()
            if "text_replace_pair" in config:
                text_replace_dict = config["text_replace_pair"]
                for key in text_replace_dict.keys():
                    text = text.replace(key, text_replace_dict[key])

            if "mathjax_url" in config:
                text = config['mathjax_url'] + '\n' + text

            if "yaml_info" in config:
                yaml_info_dict = config['yaml_info']
                yaml_info_string = "---\n"
                for key in yaml_info_dict.keys():
                    yaml_info_string = yaml_info_string + key + ": " + yaml_info_dict[key] + "\n"
                yaml_info_string = yaml_info_string + "---\n"
                text = yaml_info_string + text

            f.seek(0)
            f.truncate()
            f.write(text)
    print("Reformat markdown files successfully!")


def convert(markdown_list, config):
    pandoc_args = config['pandocParameter']
    for item in markdown_list:
        output = pypandoc.convert_file(item, 'html', extra_args=pandoc_args, encoding='utf8')
        if item.endswith('README.md'):
            with open(item.rstrip('README.md')+"index.html", 'w+', encoding='utf8') as f:
                f.write(output)
        else:
            with open(item.rstrip('.md')+".html",'w+', encoding='utf8') as f:
                f.write(output)
    print("Convert markdown files to html files successfully!")


def upload_recursion(base_local_dir, cloudServer):
    # config中的source文件夹会覆盖给出的云端路径
    tran = paramiko.Transport((cloudServer['host'], 22))
    tran.connect(username=cloudServer['username'], password=cloudServer['password'])
    sftp_client = paramiko.SFTPClient.from_transport(tran)

    def dfs(local_dir, remote_dir):
        for filename in os.listdir(local_dir):
            local_path = local_dir + '/' + filename
            remote_path = remote_dir + '/' + filename
            if os.path.isdir(local_path):
                try:
                    sftp_client.stat(remote_path)
                except IOError:
                    sftp_client.mkdir(remote_path)
                dfs(local_path, remote_path)
            elif os.path.isfile(local_path):
                sftp_client.put(local_path, remote_path)
        print("Uploaded " + local_dir + " to the cloud successfully")

    base_remote_dir = cloudServer['htmlPath']
    try:
        sftp_client.stat(base_remote_dir)
    except IOError:
        sftp_client.mkdir(base_remote_dir)

    dfs(base_local_dir, base_remote_dir)


# 获取参数
with open('config.json') as f:
    config = json.load(f)

# 处理流程
all_markdown = recursive_lookup_markdown(config["sourcePath"])
print("Indexing the path successfully!")

reformat(all_markdown, config)
convert(all_markdown, config)

if "cloudServer" in config:
    print("Upload processing may take a long time, please be patient....")
    upload_recursion(config["sourcePath"],config['cloudServer'])
    print("Uploaded all files to Cloud successfully!")

print("--------------Completed!----------------")