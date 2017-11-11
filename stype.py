#coding:utf-8
from enum import Enum

class FieldType(Enum):
    E_None = 0
    E_Int = 1
    E_FLOAT = 2
    E_STRING = 3
    E_ARRAY_SPLIT = 10
    E_Int_ARRAY = 11
    E_FLOAT_ARRAY = 12
    E_STRING_ARRAY = 13

class FieldMgrType(Enum):
    E_Value = 0
    E_Enum = 1
    E_Name = 2
    E_Read_Py = 3
    E_Write_Py = 4
    E_Read_Cs = 5
    E_Type_Proto = 6

class FieldTypeMgr:
    type_list = [
        (FieldType.E_Int.value, FieldType.E_Int,
         "int", "read_int", "write_int", "ReadInt", "int32"),
        (FieldType.E_FLOAT.value, FieldType.E_FLOAT,
         "float", "read_float", "write_float", "ReadFloat", "float"),
        (FieldType.E_STRING.value, FieldType.E_STRING,
         "string", "read_string", "write_string", "ReadString", "string"),
        (FieldType.E_Int_ARRAY.value, FieldType.E_Int_ARRAY,
         "int[]", "read_int_array", "write_int_array", "ReadIntList", "repeated int32"),
        (FieldType.E_FLOAT_ARRAY.value, FieldType.E_FLOAT_ARRAY,
         "float[]", "read_float_array", "write_float_array", "ReadFloatList", "repeated float"),
        (FieldType.E_STRING_ARRAY.value, FieldType.E_STRING_ARRAY,
         "string[]", "read_string_array", "write_string_array", "ReadStringList", "repeated string")
    ]

    @staticmethod
    def get_data_by_type(tp):
        for item in FieldTypeMgr.type_list:
            if tp == item[FieldMgrType.E_Value.value] or tp == item[FieldMgrType.E_Enum.value]:
                return item
        return None

    @staticmethod
    def get_data_item_by_type(tp, fun_type):
        item = FieldTypeMgr.get_data_by_type(tp)
        if item is not None:
            return item[fun_type.value]
        return None

    @staticmethod
    def parse_type_by_name(name):
        for item in FieldTypeMgr.type_list:
            if name.lower() == item[FieldMgrType.E_Name.value]:
                return item[FieldMgrType.E_Enum.value]
        return FieldType.E_None

    @staticmethod
    def parse_name_by_type(tp):
        item = FieldTypeMgr.get_data_by_type(tp)
        if item is None:
            return None
        return item[FieldMgrType.E_Name.value]

    @staticmethod
    def convert_value_by_type(tp, value):
        if tp == FieldType.E_Int or tp == FieldType.E_Int.value:
            return int(value)
        elif tp == FieldType.E_FLOAT or tp == FieldType.E_FLOAT.value:
            return float(value)
        elif tp == FieldType.E_STRING or tp == FieldType.E_STRING.value:
            return str(value)
        elif tp == FieldType.E_Int_ARRAY or tp == FieldType.E_Int_ARRAY.value:
            if isinstance(value, str):
                ret = value.strip('[]')
                if ret != '':
                    ret = ret.split(',')
                    return [int(i) for i in ret]
            else:
                print("strange type:%s" % value)
            return []
        elif tp == FieldType.E_FLOAT_ARRAY or tp == FieldType.E_FLOAT_ARRAY.value:
            if isinstance(value, str):
                ret = value.strip('[]')
                if ret != '':
                    ret = ret.split(',')
                    return [float(i) for i in ret]
            else:
                print("strange type:%s" % value)
            return []
        elif tp == FieldType.E_STRING_ARRAY or tp == FieldType.E_STRING_ARRAY.value:
            if isinstance(value, str):
                ret = value.strip('[]')
                if ret != '':
                    return ret.split(',')
            else:
                print("strange type:%s" % value)
            return []
