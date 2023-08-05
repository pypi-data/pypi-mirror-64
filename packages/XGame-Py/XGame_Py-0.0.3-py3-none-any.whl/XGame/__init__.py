import os,subprocess,time,webbrowser
#import definitions as defin
#defintions = defin

from XGame import docs as xdocs
def docs():
    open('docs.html','w').write(xdocs.docs)
    os.startfile('docs.html')
    #os.remove('docs.html')
def FreeStyle(*arg):
    script = ''
    for block in arg:
        script += block
    return script
def tutorialsetup():
    print("hello user! lets get you started on game development!")
    time.sleep(2)
    print("xgame is a powerful python game engine that lets you make games easy and yet rediculously powerful!")
    print("""
as you can see we opened some windows in your browser! (dont worry these links are 100% safe) this is so you can get some guidance in any issues

before you can start developing you will need to download the following..
mingw - this will let you compile and run your programs
SDL - the library to create and run games
discord - join my discord server and get help!(WIP)
the http://lazyfoo.net/SDL_tutorials/lesson01/windows/mingw/index.php link will show you how to setup sdl in mingw once they are downloaded!
  xgame is built on SDL2 do not use anything below this version!

---setup---
1. download the sdl mingw development gz file make sure you installed mingw g++ and c++ files!
MAKE ABSOLUTELY SURE You installed the g++ and c++ check everything that says this
2. once the file is downloaded do XGame.unpack('pathof File')
3. follow the setup tutorial carefully on http://lazyfoo.net/SDL_tutorials/lesson01/windows/mingw/index.php
4. once you get setup you can begin coding!
5. to run your applications use the XGame.game.debug() function example:
6.if the file fails to compile its recommended to do g++ -o myprogram.exe <yourscriptfile> -lmingw32 -lSDL2main -lSDL2 to fix the error
game = XGame.Game(name="main")
@game.code()
def code():
    return "your xgame code"
game.compile() #runs the script
""")
    time.sleep(2)
    webbrowser.open_new('http://lazyfoo.net/SDL_tutorials/lesson01/windows/mingw/index.php')
    webbrowser.open('https://stackoverflow.com/questions/10803918/undefined-reference-to-sdl-main')
    webbrowser.open('https://www.libsdl.org/release/SDL2-devel-2.0.10-mingw.tar.gz')
    webbrowser.open('https://sourceforge.net/projects/mingw/')
preincludings = """
#define SDL_MAIN_HANDLED
#include<SDL2/SDL.h>\n
#include<iostream>\n
#include<stdio.h>\n
using namespace std;
"""
begin = '{'
end = '}'
endl = 'endl'
def Log(*strings,endline=True):
    el = 'cout'
    for word in strings:
        el += f' << "{word}"'
    if endline:
        el += ' << endl;'
    else:
        el += ';'
    return el
def Main(code='',args=''):
    print('main point created')
    return f"""
int main({args}){begin}
{code}
{end}
"""
def mclass(name='UntitledClass',init=True,member=[],pre=[],type="private",preinitvals=[]):
    args = ''
    args2 = ''
    args3 = ''
    x = 0
    for i in pre:
        x += 1
        if x == len(member):
            if len(preinitvals) > 0:
                args3 += i.split('=')[0] + '=' + preinitvals[x -1 ]
            else:
                if len(preinitvals) > 0:
                    args3 += i.split('=')[0] + '=' + preinitvals[x -1 ]
                else:
                    args3 += i.split('=')[0]
            break
        else:
            args3 += i.split('=')[0] + ','
    x = 0
    for i in pre:
        x += 1
        if x == len(member):
            args2 += i.split(' ')[0]
            break
        else:
            args2 += i.split(' ')[0] + ','
    x = 0
    for i in member:
        x += 1
        if x == len(member):
            args += i
            break
        else:
            args += i + ','
    pred = ''
    for i in pre:
        pred += i + '\n'
    s = ''
    if member != []:
        for i in member:
            s += f'this->{i}={i}' + ';\n'
    #print(s)
    #print('---')
    #print(args)
    
    if not init:
        return f'''
class {name}{begin}

{end};
'''
    else:
        return f'''
class {name}{begin}
{type}:
{pred}
{name}({args2});

{end};
{name}::{name}({args3}){begin}
{s}


{end};
'''
class game:
    def __init__(self,name,includes=[],compiletest=False):
        self.name = name
        self.includes = includes
        v = []
        self.libs = ''
        for i in self.includes:
            if '<' or '>' in i:
                v.append(f'\n#include {i}')
            else:
                v.append(f'\n#include "{i}"')
        
        self.includes = v
        self.config = {}
        self.file = None
        if not compiletest:
            if os.path.isfile(name + '.cpp'):
                print(f'rewritting game.... in dir {os.path.realpath(name)}.cpp')
                self.file = open(name + '.cpp','w+')
                self.file.write(preincludings)
                for i in self.includes:
                    self.file.write(i)
            else:
                print(f'starting new game project in {os.path.realpath(name)}.cpp')
                self.file = open(name + '.cpp','w+')
                self.file.write(preincludings)
                for i in self.includes:
                    self.file.write(i)
        else:
            if os.path.isfile(name + '.cpp'):
                print(f'rewritting game.... in dir {os.path.realpath(name)}.cpp')
                self.file = open(name + '.cpp','w+')
                self.file.write('#include<iostream>\nusing namespace std;')
                for i in self.includes:
                    self.file.write(i)
            else:
                print(f'starting new game project in {os.path.realpath(name)}.cpp')
                self.file = open(name + '.cpp','w+')
                self.file.write('#include<iostream>\nusing namespace std;')
                for i in self.includes:
                    self.file.write(i)
        
    def run(config):
        config = config()
        name = config["name"]
        scale = config["scale"]
        flags = config["flags"]
    def showformat(self,code):
        print(code)
    def close(self):
        self.file.close()
        exec('del(self)')
    def reload(self):
        self.file.close()
        cache = open(self.name + '.cpp').read()
        self.file = open(self.name + '.cpp','w+')
        for c in cache:
            self.file.write(c)
    def compile(self):
        #self.file.close()
        print(f'{self} was compiled')
        if 'int main' in self.file.read():
            pass
        else:
            print("""make sure you have a main point:
                    @game.code
                    def code():
                        return XGame.Main()""")
        
    def code(self,code):
        code = code()
        print(f"writing {code}")
        self.file.write(code)
    def debug(self,command="cmd.exe",output="default",launch=True):
        if output == "default":
            output = f'xgame_{self.name}'
        self.close()
##        if 'int main(' not in self.file:
##            Warning("""main point not defined! please create one by doing:
##                    @game.code
##                    def code():
##                        return XGame.Main()""")
            
        print('please make sure you have minGW c++ compiler installed on the machine')
        self.file.close()
        #subprocess.Popen([f"{command}",f"c++ {self.name}.cpp"])
        try:
            
            os.system(f"g++ -o {output}.exe {self.name}.cpp -lmingw32 -lSDL2main -lSDL2")
            os.system("echo compilation completed succesfully you may now close the window")
            if launch == True:
                os.startfile(output + '.exe')
        except Exception as e:
            os.system(f"echo compilation failed! please make sure everything is setup correctly error: {e}")
	
        
        cache = open(self.name + '.cpp').read()
        self.file = open(self.name + '.cpp','w+')
        for c in cache:
            self.file.write(c)
        self.close()
        print(f'if script doesnt run do: g++ -o {output}.exe {self.name}.cpp -lmingw32 -lSDL2main -lSDL2')
        
