import re

# 改行コードを除外する関数(冒頭と末尾のみ除外。中間は残す)
def remove_newlines(text):
    return re.sub(r"(^\n+)|(\n+$)", "", text)

def replace_and_write(temp, replaced_markers, replace_contents, output_file_name):
    for m,c in zip(replaced_markers, replace_contents):
        temp = temp.replace(m, c, 1)
    
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(temp)