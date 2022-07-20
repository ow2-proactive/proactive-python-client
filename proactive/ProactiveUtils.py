import re

def convert_palist_to_list(string):
    lst_new = []
    if string.startswith('PA:LIST'):
        str1 = string.replace("(", "")
        str2 = str1.replace(")", "")
        str3 = str2.replace("PA:LIST", "")
        lst_new =  re.split(',', str3)
    return lst_new
