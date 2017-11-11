#coding:utf-8
import os
import xlrd
from binarybuff import BinaryBuff
from stype import FieldType, FieldTypeMgr, FieldMgrType

class SheetBinaryBuff(BinaryBuff):
    def write_data_by_type(self, tp, value):
        fun_name = FieldTypeMgr.get_data_item_by_type(tp, FieldMgrType.E_Write_Py)
        att_fun = getattr(self, fun_name)
        att_fun(value)

    def read_data_by_type(self, tp):
        fun_name = FieldTypeMgr.get_data_item_by_type(tp, FieldMgrType.E_Read_Py)
        att_fun = getattr(self, fun_name)
        return att_fun()

binary_buff = SheetBinaryBuff(10*1024*1024)

class SheetCellHead:
    def __init__(self):
        self.col_index = 0
        self.field_name = ''
        self.field_type = FieldType.E_None

    def set_data(self, colx, f_name, f_type):
        self.col_index = colx
        self.field_name = f_name
        self.field_type = f_type

    def serialize(self, bin_buff: BinaryBuff):
        bin_buff.write_unsign_short(self.field_type.value)
        bin_buff.write_string(self.field_name)

    def deserialize(self, bin_buff: BinaryBuff):
        self.field_type = bin_buff.read_unsign_short()
        self.field_name = bin_buff.read_string()

class SheetRowData:
    def __init__(self, sheet_head):
        self.cell_list = []
        self.sheet_head = sheet_head

    def parse_row(self, cells):
        cell_len = len(cells)
        for head in self.sheet_head:
            if head.col_index < cell_len:
                cell_value = self.parse_cell(head.field_type, cells[head.col_index])
                self.cell_list.append(cell_value)
            else:
                self.cell_list.append(None)

    def parse_cell(self, tp, cell: xlrd.sheet.Cell):
        return FieldTypeMgr.convert_value_by_type(tp, cell.value)

    def serialize(self, bin_buff: SheetBinaryBuff):
        ncol = len(self.sheet_head)
        #bin_buff.write_unsign_short(ncol)
        for i in range(0, ncol):
            head = self.sheet_head[i]
            bin_buff.write_data_by_type(head.field_type, self.cell_list[i])

    def deserialize(self, bin_buff: SheetBinaryBuff):
        ncol = len(self.sheet_head) #bin_buff.read_unsign_short()
        for i in range(0, ncol):
            head = self.sheet_head[i]
            self.cell_list.append(bin_buff.read_data_by_type(head.field_type))


class SheetData:
    def __init__(self):
        self.sheet_name = ''
        self.sheet_heads = []
        self.sheet_rows = []

    def get_heads(self):
        return self.sheet_heads

    def get_col_num(self):
        return len(self.sheet_heads)

    def get_row_num(self):
        return len(self.sheet_rows)

    def parse(self, sheet: xlrd.sheet.Sheet):
        self.sheet_name = sheet.name
        self.parse_head(sheet)
        self.parse_rows(sheet)

    def parse_head(self, sheet: xlrd.sheet.Sheet):
        field_name = sheet.row(0)
        field_type = sheet.row(1)
        for i in range(0, len(field_name)):
            fname = field_name[i].value
            tname = i < len(field_type) and field_type[i].value or ''
            if tname == 'null' or fname == '':
                continue
            ftype = FieldTypeMgr.parse_type_by_name(tname)
            if ftype == FieldType.E_None:
                continue

            cell_head = SheetCellHead()
            cell_head.set_data(i, fname, ftype)
            self.sheet_heads.append(cell_head)

    def parse_rows(self, sheet: xlrd.sheet.Sheet):
        for i in range(3, sheet.nrows):
            row_data = SheetRowData(self.sheet_heads)
            row_data.parse_row(sheet.row(i))
            self.sheet_rows.append(row_data)

    def serialize(self, bin_buff: BinaryBuff):
        bin_buff.reset_write()
        bin_buff.write_string_nolen(b'ydg')
        offset = bin_buff.get_write_offset()
        bin_buff.write_int(0) #seize a int
        bin_buff.write_unsign_short(len(self.sheet_heads))
        for head in self.sheet_heads:
            head.serialize(bin_buff)
        bin_buff.write_insert_int(offset, bin_buff.get_write_offset())
        bin_buff.write_unsign_short(len(self.sheet_rows))
        for row in self.sheet_rows:
            row.serialize(bin_buff)

    def deserialize(self, bin_buff: BinaryBuff):
        bin_buff.reset_read()
        start_str = bin_buff.read_string_nolen(3)
        if start_str != b'ydg':
            return
        bin_buff.read_int()
        head_len = bin_buff.read_unsign_short()
        for i in range(0, head_len):
            head = SheetCellHead()
            head.deserialize(bin_buff)
            self.sheet_heads.append(head)
        nrow = bin_buff.read_unsign_short()
        for i in range(0, nrow):
            row = SheetRowData(self.sheet_heads)
            row.deserialize(bin_buff)
            self.sheet_rows.append(row)


    def out_put(self):
        head_names = ''
        for head_name in self.sheet_heads:
            head_names = head_names + head_name.field_name + "\t"
        head_types = ''
        for head_type in self.sheet_heads:
            head_types = head_types + str(head_type.field_type) + "\t"
        print(head_names)
        print(head_types)
        for sheet_row in self.sheet_rows:
            row_str = ''
            for cell_item in sheet_row.cell_list:
                row_str = row_str + str(cell_item) + "\t"
            print(row_str)
            print("\n")

class ExcelData:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.sheets = []

    def get_file_name(self):
        (_, fname) = os.path.split(self.excel_path)
        (name, _) = os.path.splitext(fname)
        return name

    def read_from_file(self):
        xlsx = None
        try:
            xlsx = xlrd.open_workbook(self.excel_path)
        except IOError:
            xlsx = None
        if xlsx is None:
            print("Not found xlsx:" + self.excel_path)
            return
        sheet_names = xlsx.sheet_names()
        for name in sheet_names:
            sheet = xlsx.sheet_by_name(name)
            sheet_data = SheetData()
            sheet_data.parse(sheet)
            self.sheets.append(sheet_data)

    def write_to_binary(self):
        for sheet in self.sheets:
            binary_buff.reset_write()
            sheet.serialize(binary_buff)
            binary_buff.write_to_file('./data/' + sheet.sheet_name.lower() + '.bin')

    def out_put(self):
        for sheet in self.sheets:
            print(sheet.sheet_name)
            sheet.out_put()
            print("\n\n\n")

if __name__ == "__main__":
    #'''
    xlsx1 = xlrd.open_workbook('Test.xlsx')
    sheet1 = xlsx1.sheet_by_index(0)

    read_sheet = SheetData()
    read_sheet.parse(sheet1)
    read_sheet.serialize(binary_buff)
    read_sheet.out_put()

    read_sheet = SheetData()
    read_sheet.deserialize(binary_buff)
    read_sheet.out_put()
    #'''
