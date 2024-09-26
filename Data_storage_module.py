import os
import pickle
import keyboard
from maya import cmds

plugin_path = os.path.join(os.path.dirname(__file__))
# 获取插件路径

data_storage_folder_path = plugin_path + "\\Data"

DATAFILENAME = 'HistoricalDataFile.json'

def Detect_and_create_history_folder():
    """ 创建历史文件夹 判断脚本下有没有历史文件夹，如果没有会自动创建"""
    
    if not os.path.exists(data_storage_folder_path):
        os.makedirs(data_storage_folder_path)
        print('检测到你没有创建数据文件夹，将会自动帮你创建一个数据文件夹')



def Detect_and_create_history_file():
    """ 创建历史文件 判断有没有历史文件，如果没有会自动创建并写入初始数据信息"""

    if not os.path.exists(data_storage_folder_path+'\\'+ DATAFILENAME):
        with open(data_storage_folder_path+'\\'+ DATAFILENAME, 'w') as f:
            f.write(' ')
        print('检测到你没有创建数据文件夹，将会自动帮你创建一个数据文件')
        write_default_attr()


def write_default_attr():
    """ 重新写入文件信息 """

    default_attr = {'role_name':' ',
                    'load_dna_path' : ' ',
                    'fbx_path' : ' ',
                    }
    # 默认属性

    with open(data_storage_folder_path+'\\'+ DATAFILENAME, 'wb')as file:
        pickle.dump(default_attr,file)

def reading_history_file(): # 读取文件信息
    """ 读取文件信息 """

    with open(data_storage_folder_path+'\\'+ DATAFILENAME, 'rb') as file:
        default_attr = pickle.load(file)
    return default_attr

def modify_file_attr(key_var,modify_var):
    """ 修改文件信息 """
    
    reading_history_file()
    default_attr = reading_history_file()

    default_attr[key_var] = modify_var

    with open(data_storage_folder_path+'\\'+ DATAFILENAME, 'wb')as file:
        pickle.dump(default_attr,file)









    
    