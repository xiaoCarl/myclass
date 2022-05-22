# 下载0600000数据

./getdata 0600000

code：后面接的是所要查询的股票代码（文末会给出A股大部分股票代码）
start：后面接的是数据起始日期（比如，2019年2月3号就是对应21090203）
end：后面接的是数据截止日期（注意这个时间要比start对应时间大，这两个不能弄反）
fields：对应的就是你要下载的数据类型，就是下图对应的项

TCLOSE 收盘价
HIGH 最高价
LOW 最低价
TOPEN 开盘价
LCLOSE 前收盘价
CHG 涨跌额
PCHG 涨跌幅
TURNOVER   换手率
VOTURNOVER 成交量 
VATURNOVER 成交金额
TCAP  总市值
MCAP  流通市值



# 下载数据
pip3 install baostack

python3 getdata.py


# 简单的量化测试(https://github.com/Ckend/pythondict-quant.git)
python3 cash.py


