from connection import conn

from pandas import read_sql, DataFrame

# ins = 'select Producao from tbl_Paradas'
# df = DataFrame(read_sql(ins, conn))
# arr = []

# for i in df.drop_duplicates().values.tolist():
#     arr.append(i[0])

# print(arr)

sist = 'Britagem Primária'
proc = 'Via Seca'
equip = '2101-FE-001'
dt_inicio = '2021/06/04'
dt_fim = '2021/06/05'
ins = f"select * from tbl_Paradas where Sistema = '{sist}' and Producao = '{proc}' and Equipamento = '{equip}' and DataInicio >= convert(Datetime, '{dt_inicio}') and DataFim <= convert(Datetime, '{dt_fim}')"
df = DataFrame(read_sql(ins, conn))

print(df["Id"].values[0])