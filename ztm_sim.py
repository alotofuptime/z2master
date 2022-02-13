import xpath_logic as xp
import pandas as pd


course_directory = xp.main() 
df = pd.DataFrame()
academy_api = df.from_dict(course_directory, orient="columns")

# saved csv to use in jupyter notebooks
academy_api.to_csv("ztm.csv")
# print(academy_api.head())
