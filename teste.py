from connection import conn

from pandas import read_sql, DataFrame

ins = 'select Producao from tbl_Paradas'
df = DataFrame(read_sql(ins, conn))
arr = []

for i in df.drop_duplicates().values.tolist():
    arr.append(i[0])

print(arr)