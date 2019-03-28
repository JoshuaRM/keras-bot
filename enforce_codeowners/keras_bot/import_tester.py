import os
from glob import glob

ignore = ['__future__', 'collections', 'random', 'six', 'cPickle', 'scipy', 'hashlib', 
            'io', 'contextlib', 'unittest', 'types', 'h5py', 'inspect', 'tarfile', 'yaml', 
            'copy', 'marshal', 'requests', 'functools', 'gzip', 're', 'Queue', 'queue', 
            'os', 'pickle', 'importlib', 'mock', 'threading', 'codecs', 'tempfile', 'time', 
            'binascii', 'pydot', 'zipfile', 'json', 'shutil', 'abc', 'sys', 'csv', 'cntk',
            'warnings', 'numpy', 'skimage', 'multiprocessing', 'distutils', 'tensorflow', 
            'theano', 'keras_applications', "keras_preprocessing"]

def check_absolute(file):
    
    with open(file) as f:
        imports = f.read().split("\n")

    errs = []
    lineno=0

    comment = False

    for line in imports:
        lineno+=1
        #Ingore lines withing multi line comments
        if '\"\"\"' in line:
            comment = not comment
        #Empty line or comment line
        if line == "" or comment == True or '#' in line:
            pass
        else:
            split_line = line.split()
            #Import
            if split_line[0] == 'import':
                module_split = split_line[1].split('.')
                #Check if module is an ignored library
                if module_split[0] in ignore:
                    pass 
                else:
                    string = str(file) + " contains an absolute import on line " + str(lineno)
                    errs.append(string)
                    

            #ImportFrom
            elif split_line[0] == 'from' and len(split_line) >= 3:
                #Check if module is an ignored library or line doesnt contain import
                if split_line[1] in ignore or split_line[2] != 'import':
                    pass
                #Check if import is absolute or relative
                elif split_line[1].startswith('.'):
                    pass
                else:
                    module_split = split_line[1].split('.')
                    if module_split[0] in ignore:
                        continue
                    else:
                        string = str(file) + " contains an absolute import on line " + str(lineno)
                        errs.append(string)

    return errs

def check_imports(dirPath):
    ret = {}
    result = [y for x in os.walk(dirPath) for y in glob(os.path.join(x[0], '*.py'))]
    for file in result:
        fileKey = file[11:]
        val = check_absolute(file)
        if val == []:
            pass
        else:
            ret[fileKey]=(val)
    return ret
