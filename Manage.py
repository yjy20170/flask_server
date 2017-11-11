dic={'yjy':'yinjinyu','st':'shitao','zjy':'zuojinyan','zqb':'zhouqunbo'}
def manage(name):
    if name in dic.keys():
        return dic[name]
    else:
        return 'ERROR'
