import pandas as pd


# TODO optimize course selction with pandas + regex below are a few tests without regex
# TODO create design patter for Academy emulation
ztm_api = pd.read_csv("ztm.csv").drop(columns="Unnamed: 0")
node_next_js = ztm_api[ztm_api["title"].str.contains(".js")]
javascript_path = ztm_api[ztm_api["title"].str.contains("JavaScript")]
react_path = ztm_api[ztm_api["title"].str.contains("React")]
angular_path = ztm_api[ztm_api["title"].str.contains("Angular")]
web_dev_path = ztm_api[ztm_api["title"].str.contains("Web Developer")]
python_dev_path = ztm_api[ztm_api["title"].str.contains("Python")]
data_sci_path = ztm_api[ztm_api["title"].str.contains("Data Science")]

print(ztm_api["title"])
print(data_sci_path)
