#coding:utf-8
import os
from excel import ExcelData
from genertation import *
#import data_pb2

def gen_csharp_and_data(file_name):
    excel_data = ExcelData(file_name)
    excel_data.read_from_file()
    excel_data.write_to_binary()
    for sheet in excel_data.sheets:
        gen = GenerateCSharp(sheet)
        gen.gen_code()

def gen_proto_message_and_data(sheet):
    gen_proto = GenerateProto(sheet)
    gen_proto.gen_code()

    gen_text = GenerateProtoText(sheet)
    gen_text.gen_code()

    sheet_name = sheet.sheet_name
    gen_path = '.\\gen_codes\\' + sheet_name.lower()
    arguments = (sheet_name, gen_path, gen_path, gen_path)
    cmd = 'protoc --encode=data.%sInfoList %s.proto<%s.proto.txt>%s.data' % arguments
    os.system(cmd)

def gen_excel_proto(file_name):
    excel_data = ExcelData(file_name)
    excel_data.read_from_file()
    for sheet in excel_data.sheets:
        gen_proto_message_and_data(sheet)

'''
def test_data():
    dInfoList = data_pb2.DataInfoList()
    f = open("./gen_codes/data.bin", "rb")
    dInfoList.ParseFromString(f.read())
    for data_item in dInfoList.dataList:
        print(data_item.ID)
        print(data_item.Some)
        print(data_item.Name)
        print(data_item.Data1)
        print(data_item.Data2)
        print(data_item.Data3)
        print(data_item.Data4)
'''

if __name__ == "__main__":
    gen_excel_proto('Test.xlsx')
