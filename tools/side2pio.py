import sys
import os.path
import re
import configparser

rx_dict = {
    'compiler': re.compile(r'^(?:>compiler)=(?P<compiler>\S+).*\n'),
    'memtype':  re.compile(r'^(?:>memtype)=(?P<memtype>\S+).*\n'),
    'optimize': re.compile(r'^(?:>optimize)=(?P<optimize>\S+).*\n'),
    'flag':     re.compile(r'^(?:>)(?P<flag>-\S+).*\n'),   
    'board':    re.compile(r'^(?:>BOARD):*(?P<board>\S+).*\n')
}

def parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def process(config, filename):
    board = []
    build_flags = []
    build_unflags = []
    with open(filename) as sidefile:
        line = sidefile.readline()
        while line:
            key, match = parse_line(line)       
            line = sidefile.readline()
            if key == 'compiler':
                None
            if key == 'board':
                board = [match.group(key)]
            if key == 'optimize':
                build_flags += [match.group(key)]
            if key == 'memtype':
                build_flags += ["-m" + match.group(key)]

    if not "-Os" in build_flags:
        build_unflags += ["-Os"]

    envname = 'env:' + os.path.splitext(os.path.basename(filename))[0]
    config[envname] = {}
    env = config[envname]
    env['platform'] = 'propeller'
    if board:
        env['board'] = ''.join(board).lower()
    if build_flags:
        env['build_flags'] = '\n'+'\n'.join(build_flags)
    if build_unflags:
        env['build_unflags'] = '\n'+'\n'.join(build_unflags)

def main():
    argnum = len(sys.argv)
    if argnum > 1:
        flist = sys.argv[1:]
        fext = [os.path.splitext(x)[1] for x in flist]
        if not all(item in ['.side'] for item in fext):
            print('Error: only SimpleIDE files are allowed')
            exit(1)
        else:
            config = configparser.ConfigParser()
            for filename in flist:
                process(config, filename)
                print('Log: processed', filename)
            with open('platformio.ini', 'w') as piofile:
                config.write(piofile)
            print('Log: done')
            exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    # execute only if run as a script
    main()