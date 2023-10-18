from openpyxl import Workbook

book = Workbook()
sheet = book.active
sheet['C4'] = 'Nombres'
sheet['D4'] = 'Cajuelas'
data = ((31, 'Fabian', 3.25),(29, 'Pablo Mora Barrantes', 5.25), (30, 'Ana', 2.25),(31, 'Fabian', 3.25),(29, 'Pablo Mora Barrantes', 5.25),(29, 'Pablo Mora Barrantes', 5.25) ,(29, 'Pablo Mora Barrantes', 5.25))

n=5

for contact in data:
    for num in range(n,n+1):
        print(num)
        sheet[f'C{num}'] = contact[1]
        sheet[f'D{num}'] = contact[2]
        n += 1
            
book.save(f'Registro del dia.xlsx')