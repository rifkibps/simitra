from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
import string


def get_name_fields(obj, exclude_pk = False, exclude_fields = None):
    model = obj._meta.concrete_fields
    name_of_pk = obj._meta.pk.name

    headers = []
    for field in model:

        if exclude_pk and field.name == name_of_pk:
                continue

        if exclude_fields and len(exclude_fields) > 0:
            if field.name in exclude_fields:
                continue

        headers.append(field.name)
    
    return headers



def get_verbose_fields(obj, exclude_pk = False, exclude_fields = None):

    model = obj._meta.concrete_fields
    name_of_pk = obj._meta.pk.verbose_name

    headers = []
    for field in model:
        if exclude_fields and len(exclude_fields) > 0:
            if field.name in exclude_fields:
                continue

        headers.append(obj._meta.get_field(field.name).verbose_name)

    if exclude_pk:
        headers.remove(name_of_pk)
    
    return headers


def tablib_to_dict(dataset):

    # Access headers data with imported_data.headers
    # Access content data with imported_data._data

    headers = dataset.headers
    rows_data = dataset._data

    data = []
    for row, rows_values in enumerate(rows_data, 1):
        field_dict = {'row': row}

        for idx, field_value in enumerate(rows_values):
            field_dict[headers[idx]] = field_value

        field_dict['id_sls'] = str(field_dict['kode_prov']) + str(field_dict['kode_kabkot']) + str(field_dict['kode_kecamatan']) + str(field_dict['kode_desa']) + str(field_dict['kode_sls'])
        data.append(field_dict)

    return data



def generate_meta_templates (sheet, head_cell, start_rows, head_text, choices, target_cell, target_idx, def_rows = 10):
    sheet[f'{head_cell}{start_rows}'] = head_text
    sheet[f'{head_cell}{start_rows}'].font = Font(name='Cambria',bold=True, size=11)
    sheet.column_dimensions[head_cell].width = 22


    for idx, dt_status in enumerate(choices): #Generates 99 "ip" address in the Column A;
        sheet[f'{head_cell}{idx+start_rows+1}'].value = dt_status[1]
        sheet[f'{head_cell}{idx+start_rows+1}'].font = Font(name='Cambria', size=11)

    val_data = DataValidation(type="list",formula1=f'=${head_cell}{start_rows+1}:${head_cell}{start_rows+len(choices)}') #You can change =$A:$A with a smaller range like =A1:A9
    val_data.error ='Your entry is not in the list'
    val_data.errorTitle = 'Invalid Entry'
    val_data.prompt = 'Please select from the list'
    val_data.promptTitle = 'List Selection'
    sheet.add_data_validation(val_data)

    for row in range(target_idx,target_idx+def_rows):
        val_data.add(sheet[f"{target_cell}{row}"]) #If you go to the cell B1 you will find a drop down list with all the values from the column A
    return sheet


def generate_meta_templates_multiple_cols (sheet, head_cell, start_rows, head_text, choices, target_cell, target_idx, def_rows = 10):

    cols_lists = list(string.ascii_uppercase)
    next_cols = cols_lists[cols_lists.index(head_cell)+1]
    
    sheet[f'{head_cell}{start_rows}'] = head_text
    sheet[f'{head_cell}{start_rows}'].font = Font(name='Cambria',bold=True, size=11)
    sheet.column_dimensions[head_cell].width = 15
    sheet.column_dimensions[next_cols].width = 22

    sheet.merge_cells(f'{head_cell}{start_rows}:{next_cols}{start_rows}')

    for idx, dt_status in enumerate(choices): #Generates 99 "ip" address in the Column A;
        sheet[f'{head_cell}{idx+start_rows+1}'].value = dt_status[0]
        sheet[f'{head_cell}{idx+start_rows+1}'].font = Font(name='Cambria', size=11)

        sheet[f'{next_cols}{idx+start_rows+1}'].value = dt_status[1]
        sheet[f'{next_cols}{idx+start_rows+1}'].font = Font(name='Cambria', size=11)
    
    val_data = DataValidation(type="list",formula1=f'=${head_cell}{start_rows+1}:${head_cell}{start_rows+len(choices)}') #You can change =$A:$A with a smaller range like =A1:A9
    val_data.error ='Your entry is not in the list'
    val_data.errorTitle = 'Invalid Entry'
    val_data.prompt = 'Please select from the list'
    val_data.promptTitle = 'List Selection'
    sheet.add_data_validation(val_data)

    for row in range(target_idx,target_idx+def_rows):
        val_data.add(sheet[f"{target_cell}{row}"]) #If you go to the cell B1 you will find a drop down list with all the values from the column A
    return sheet

def generate_headers_excel(x):
    
    cols = [string.ascii_uppercase[i] if i < 26 else string.ascii_uppercase[i // 26 - 1] + string.ascii_uppercase[i % 26] for i in range(x)]
    return cols