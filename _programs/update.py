import glob
import subprocess
import pandas as pd
from modules import get_modified_time


# 更新の実行
subprocess.run(['python', './_programs/make_posts.py'])
subprocess.run(['python', './_programs/make_index.py'])
subprocess.run(['python', './_programs/make_sort_by_date.py'])
# subprocess.run(['python', './_programs/add_ad_to_posts.py'])
subprocess.run(['python', './_programs/make_sitemap.py'])


# 更新日時の記録
search_words = ["_posts_original_en/20*.html", "_posts_original/20*.html", "_programs/*.py", "_templates/*.html"]

data = []
for w in search_words:
    data += [[f, get_modified_time(f)] for f in glob.glob(w)]

pd.DataFrame(data, columns = ["FileName", "DateTime"]).to_csv("./_programs/last_modified_time.csv")

