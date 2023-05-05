from connection import conn, engine

from pandas import read_sql, DataFrame

# ins = 'select Producao from tbl_Paradas'
# df = DataFrame(read_sql(ins, conn))
# arr = []

# for i in df.drop_duplicates().values.tolist():
#     arr.append(i[0])

# print(arr)

df = DataFrame(read_sql("select CodigoFalha from tbl_Paradas where id = 402", engine.connect()))
print(df["CodigoFalha"][0])