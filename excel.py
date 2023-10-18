import pandas as pd
import openpyxl
import datetime

# data = {
#     'car' : ["A", "B", "C"],
#     'brand' : [1, 2, 3]
# }

# update = ["D", 4]

# excel_file = "test.xlsx"
# myvar = pd.DataFrame(data)
# # newvar = pd.DataFrame(update)

# myvar.loc[len(myvar.index)] = update


# myvar.to_excel(excel_file, index=True)

# # print(myvar)

excel_file = "transaction.xlsx"
data_format = {'Date': []}
myvar = pd.DataFrame(data_format)

for i in cash_transaction:
    myvar.loc[len(myvar.index)] = cash_transaction[i]

myvar.to_excel(excel_file, index="True")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       