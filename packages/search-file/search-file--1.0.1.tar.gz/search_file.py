import sys,os

__all__=["directories","search"]
__email__="3416445406@qq.com"
__author__="七分诚意 qq:3076711200 邮箱:%s"%__email__
__version__="1.0.1"

def dir(path):
    for folder in os.listdir(path):
        yield "{}\{}".format(path,folder)

def directories(path):
    """一个生成器, 列出path下的所有子目录和文件名。
如:
>>> from search_file import directories
>>> list(directories("C:\\"))
['C:\\Users',  #第一层目录
'C:\\Users\\Administrator', #第二层目录
...,
'C:\\Windows',
'C:\\Windows\\System32',
...]
"""
    try:
        for folder in dir(path):
            for sub_directory in directories(folder):
                yield sub_directory
    except OSError:yield path

direc=directories #定义别名
def search(filename,path,minsize=0,maxsize=None):
    """一个生成器,在path中搜索一个文件或文件夹。
如:
>>> from search_file import search
>>> list(search("cmd.exe","C:\\"))
['C:\\Windows\\System32\\cmd.exe',
...]"""
    for file in directories(path):
        if filename in file:
            size=os.path.getsize(file)
            if size>=minsize and (size<=maxsize if maxsize else True):
                yield file

def test():
    "找出(系统)目录中最大的文件。"
    print("搜索中 ...")
    import time
    start_time=time.perf_counter()
    min_size=2**27 # 128MB
    files=[]
    dir=sys.argv[1] if len(sys.argv)>1 else os.environ.get("systemroot")
    for path in directories(dir):
        if os.path.isfile(path):
            size=os.path.getsize(path)
            if size>=min_size:
                print("找到文件:{} ({:.2f}MB)".format(path,size/(2**20)))
                files.append(path)
    largest_file = max(files,key=os.path.getsize)
    print("最大的文件: %s (%fGB)"%(
        largest_file,os.path.getsize(largest_file)/(2**30)))
    print("用时:{:2f}秒".format(time.perf_counter()-start_time))

if __name__=="__main__":test()