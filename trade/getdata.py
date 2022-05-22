import baostock as bs
import pandas as pd

lg = bs.login()

stock_code = "sh.000001"
rs = bs.query_history_k_data_plus(stock_code,
     "date,code,open,high,low,close,preclose,volume,amount,pctChg",
     start_date='2020-02-03', end_date='2021-02-10', frequency="d")

data_list = []
while (rs.error_code == '0') & rs.next():
     # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())

result = pd.DataFrame(data_list, columns=rs.fields)
result.to_csv("%s_data.csv"%stock_code, index=False)