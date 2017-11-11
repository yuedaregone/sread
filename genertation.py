#coding:utf-8
from excel import SheetData
from stype import FieldMgrType, FieldTypeMgr, FieldType
from jinja2 import Template

class GenerateCode:
    tpl_path = './templates/'
    des_path = './gen_codes/'

    def __init__(self, sheet: SheetData):
        self.sheet_data = sheet

    def gen_code(self):
        file_tpl = open(self.tpl_path + self._get_tpl_file_name(), 'r')
        contents = file_tpl.read()

        tpl = Template(contents)
        dic = self._generate_param_list()
        result = tpl.render(dic)

        code_file_name = self.sheet_data.sheet_name.lower() + self._get_gen_file_extension()
        code_file = open(self.des_path + code_file_name, 'w')
        code_file.write(result)

    def _generate_param_list(self):
        return {}

    def _get_read_handle_type(self):
        return FieldMgrType.E_Read_Cs

    def _get_gen_file_extension(self):
        return '.code'

    def _get_tpl_file_name(self):
        return 'csharp.tpl'

class GenerateCSharp(GenerateCode):
    def __init__(self, sheet: SheetData):
        GenerateCode.__init__(self, sheet)

    def _generate_param_list(self):
        sheet_name = self.sheet_data.sheet_name
        sheet_heads = self.sheet_data.sheet_heads
        param_dict = {}
        param_dict['datainfo'] = sheet_name + 'Info'
        param_dict['dataread'] = sheet_name + 'InfoReader'
        param_dict['filename'] = sheet_name.lower() + '.bin'
        member_list = []
        for head in sheet_heads:
            field_data = FieldTypeMgr.get_data_by_type(head.field_type)
            type_name = field_data[FieldMgrType.E_Name.value]
            fun_name = field_data[self._get_read_handle_type().value]
            member_item = (head.field_name, type_name, fun_name)
            member_list.append(member_item)
        param_dict['datamemberlist'] = member_list
        return param_dict

    def _get_read_handle_type(self):
        return FieldMgrType.E_Read_Cs

    def _get_gen_file_extension(self):
        return '.cs'

    def _get_tpl_file_name(self):
        return 'csharp.tpl'

class GenerateProto(GenerateCode):
    def __init__(self, sheet: SheetData):
        GenerateCode.__init__(self, sheet)

    def _generate_param_list(self):
        sheet_name = self.sheet_data.sheet_name
        sheet_heads = self.sheet_data.sheet_heads
        param_dict = {}
        param_dict['datainfo'] = sheet_name + 'Info'
        param_dict['datalist'] = sheet_name + 'InfoList'
        member_list = []
        for head in sheet_heads:
            field_data = FieldTypeMgr.get_data_by_type(head.field_type)
            type_name = field_data[self._get_read_handle_type().value]
            member_item = (type_name, head.field_name)
            member_list.append(member_item)
        param_dict['datamemberlist'] = member_list
        return param_dict

    def _get_read_handle_type(self):
        return FieldMgrType.E_Type_Proto

    def _get_gen_file_extension(self):
        return '.proto'

    def _get_tpl_file_name(self):
        return 'proto.tpl'

class GenerateProtoText(GenerateCode):
    def __init__(self, sheet: SheetData):
        GenerateCode.__init__(self, sheet)

    def __make_cell(self, type_name, value):
        ret_v = None
        if isinstance(value, str):
            ret_v = '"' + value + '"'
        else:
            ret_v = value
        return (type_name, ret_v)

    def _generate_param_list(self):
        row_datas = self.sheet_data.sheet_rows
        sheet_heads = self.sheet_data.sheet_heads
        item_list = []
        for row_data in row_datas:
            item_cells = row_data.cell_list
            field_list = []
            for i in range(0, len(sheet_heads)):
                head = sheet_heads[i]
                if head.field_type.value > FieldType.E_ARRAY_SPLIT.value:
                    for cell in item_cells[i]:
                        field_list.append(self.__make_cell(head.field_name, cell))
                else:
                    field_list.append(self.__make_cell(head.field_name, item_cells[i]))
            item_list.append(field_list)
        param_dict = {}
        param_dict['datalist'] = item_list
        return param_dict

    def _get_gen_file_extension(self):
        return '.proto.txt'

    def _get_tpl_file_name(self):
        return 'proto_text.tpl'
