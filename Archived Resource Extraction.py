import pandas as pd

df_old = pd.read_excel("C:/Users/nakul.kumbria/Downloads/New Report (1).xlsx")
df_new = pd.read_excel("C:/Users/nakul.kumbria/Downloads/New Report.xlsx")
merge_cols = ['Project Description', 'Team (OBS)', 'Total (Hours)', 'Cost (USD) *']

df_matched = pd.merge(
    df_new,
    df_old,
    on=merge_cols,
    suffixes=('_anonymized', '_real'),
    how='inner'
)
df_result = df_matched[[
    'Resource Name_anonymized',
    'Resource Name_real',
    'Project Description',
    'Team (OBS)',
    'Total (Hours)',
    'Cost (USD) *'
]]
print(df_result)
df_result.to_excel("C:/Users/nakul.kumbria/Downloads/Matched_Resources.xlsx", index=False)
