import re


def remove_newlines(text):
    """
    文字列の先頭と末尾にある改行コードを除外する関数。
    中間の改行コードは残す。
    
    Args:
        text: 文字列
        
    Returns:
        (定義なし): 処理後の文字列
    """
    return re.sub(r"(^\n+)|(\n+$)", "", text)

def replace_and_write(text, replaced_markers, replace_contents, output_file_name):
    """
    テキスト内の特定のマーカーを置換し、結果をファイルに書き込む関数。
    
    Args:
        text: 置換対象の文字列
        replaced_markers: 置換するマーカーのリスト
        replace_contents: 置換する内容のリスト。replaced_markersと同じ長さである必要あり
        output_file_name: 結果を書き込むファイルの名前
    """

    # 置換
    for m,c in zip(replaced_markers, replace_contents):
        text = text.replace(m, c, 1) # mをcで1回だけ置換
    
    # 出力
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(text)