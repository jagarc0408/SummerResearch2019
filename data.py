import xlrd 

def get_data(fileName):  
    loc = (fileName) 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    
    unit_id = []
    for i in range(sheet.nrows): 
        unit_id.append((sheet.cell_value(i, 0))) 
    unit_id.pop(0)
    
    aggression = []
    for i in range(sheet.nrows): 
        aggression.append((sheet.cell_value(i, 14))) 
    aggression.pop(0)
    
    bullying = []
    for i in range(sheet.nrows): 
        bullying.append((sheet.cell_value(i, 15))) 
    bullying.pop(0)
    
    '''
    
    comments = []
    for i in range(16, 216):
        
        comments.append((sheet.cell_value(j, i))) 
        
    '''
    return unit_id, aggression, bullying

data = get_data('labeled_0plus_to_10__full.xlsx')

#print(data)
