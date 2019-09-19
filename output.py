import xlsxwriter
import numpy as np

def output_to_excel(name, max_brightness_mat, delF_mat, two_lib=False, library_1_name=None, library_2_name=None, rpt=False, data=None, labels=None):
    # Initialize workbook based on graph title
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(name))
    worksheet = workbook.add_worksheet()

    # Initialize formatting
    cell_border = workbook.add_format({'border': True})
    cell_bold = workbook.add_format({'bold': True})

    # Label matrix locations
    worksheet.write(0, 0, "Max Brightness", cell_bold)
    worksheet.write(10, 0, "delF/F0", cell_bold)

    # Export matrices to excel
    row = 1
    col = 0
    for i in max_brightness_mat:
        for j in i:
            worksheet.write(row, col, j, cell_border)
            col += 1
        row += 1
        col = 0

    row = 11
    col = 0
    for i in delF_mat:
        for j in i:
            worksheet.write(row, col, j, cell_border)
            col += 1
        row += 1
        col = 0


    if two_lib == False:
        worksheet.conditional_format('A2:L9', {'type': '3_color_scale'})
        worksheet.conditional_format('A12:L19', {'type': '3_color_scale'})
    elif two_lib == True:
        worksheet.write('D1', library_1_name, cell_bold)
        worksheet.write('I1', library_2_name, cell_bold)
        worksheet.conditional_format('A2:F9', {'type': '3_color_scale'})
        worksheet.conditional_format('G2:L9', {'type': '3_color_scale'})
        worksheet.conditional_format('A12:F19', {'type': '3_color_scale'})
        worksheet.conditional_format('G12:L19', {'type': '3_color_scale'})

    if rpt == True:
        worksheet.write('N2', "Average X", cell_bold)
        worksheet.write('N3', "Average Y", cell_bold)
        worksheet.write('N4', "SD X", cell_bold)
        worksheet.write('N5', "SD Y", cell_bold)

        row = 0
        col = 14
        for data, label in zip(data, labels):
            x, y, x_std, y_std = data
            worksheet.write(row, col, label, cell_bold)
            row += 1
            worksheet.write(row, col, x)
            row += 1
            worksheet.write(row, col, y)
            row += 1
            worksheet.write(row, col, x_std)
            row += 1
            worksheet.write(row, col, y_std)
            row = 0
            col += 1


    workbook.close()
