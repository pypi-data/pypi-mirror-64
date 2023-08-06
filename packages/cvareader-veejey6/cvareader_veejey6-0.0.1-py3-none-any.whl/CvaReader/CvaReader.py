import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(currentdir))
import shutil
import re


class CvaReader(object):
    def __init__(self):
        pass

    def read_cva(self, path, filename, *args):
        """
        This Function returns the value of given parameters in CVA file (ex: DPB_compliance).
        :param path: path of the cva file
        :param filename: CVA file name
        :param args: Parameters to be searched
        :return: dict
        """
        value = {}
        filename = filename.rstrip('.cva')
        path = path + '\\' + filename if os.path.exists(os.path.join(path, filename)) else path
        for key in args:
            with open(os.path.join(path, filename+'.cva'), encoding='utf-8') as file:
                for line in file:
                    if '[' + key.lower() + ']' in line.lower():
                        l = next(file, '')
                        dictionary = {}
                        try:
                            while l[0] != '[' and l[0] != '\n':
                                dictionary[l.strip().split('=')[0]] = l.strip().split('=')[1]
                                l = next(file, '')
                            value[line.strip()[1:-1]] = dictionary #{l.strip().split('=')[0]: l.strip().split('=')[1]}
                        except IndexError as e:
                            value[line.strip()[1:-1]] = None
                        break
                    elif key.lower() in line.lower() and str(line[0]) != '[':
                        value[line.split('=')[0].strip()] = line.split('=')[1].strip()
                        break

        return value


if __name__ == '__main__':
    cva = CvaReader()
    ret = cva.read_cva(r'C:\Users\cmit\Desktop\SPTest_3.3.27\sp95982', 'sp95982', 'System Information', 'softpaq')
    print(ret.keys())