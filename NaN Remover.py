import pandas as pd

df_new = pd.read_csv('test.csv')

df_new.to_html('hls10.html')

html = df_new.to_html()

print(html)