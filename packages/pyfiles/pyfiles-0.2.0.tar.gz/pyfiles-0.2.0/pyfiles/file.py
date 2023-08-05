import os
import stat
import subprocess
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

import mixins

class File(mixins.FileInfoMixin):
    def __init__(self, filepath: str):
        self.path = Path(filepath)
        if not self.path.exists():
            raise FileNotFoundError(f"{filepath} doesn't exists")
        if not self.path.is_file():
            raise TypeError(f"{filepath} doesn't a file")
        self.permission = FilePermission(self)
        self.content = FileContent(self.path)
    
    
    def octal_format(self):
        return (
            self.permission.owner.octal_notation(), 
            self.permission.group.octal_notation(), 
            self.permission.others.octal_notation(),
        )
    
    def octal_format_to_string(self):
        return ''.join(str(item) for item in self.octal_format())


class FileContent:
    def __init__(self, path: str):
        self._path = path
    
    def append_to_file(self, content):
        with open(self._path, '+a') as file:
            file.write(content)

    def read_only(self):
        with open(self._path, 'r') as file:
            for line in file.readlines():
                yield line


class FilePermission:
    def __init__(self, file: File):
        self.file = file
        self.owner = _Permission(*file.mode[1:4])
        self.group = _Permission(*file.mode[4:7])
        self.others = _Permission(*file.mode[7:])
    
    def mode(self):
        return f'-{self.owner}{self.group}{self.others}'
   
    def change_permission(self, where_change: str, which_permission: str):
        '''
        where_change: owner, group, others
        which_permission: read, write, execute
        '''
        perm = getattr(self, where_change)
        rwx = getattr(perm, which_permission)
        if rwx == '-':
            if which_permission == 'read':
                setattr(perm, which_permission, 'r' )
            elif which_permission == 'write':
                setattr(perm, which_permission, 'w' )
            elif which_permission == 'execute':
                setattr(perm, which_permission, 'x' )
        else:
            setattr(perm, which_permission, '-' )
        
        output = subprocess.run(['chmod', ''.join(self.file.octal_format_to_string()), self.file.path], capture_output=True)
        if output.stderr:
            print({'error': str(output.stderr)})
            raise OSError(f'Not possible to change file permissions')


class _Permission:
    def __init__(self, read: str, write: str, execute: str):
        self._read = read
        self._write = write
        self._execute = execute
    
    def __repr__(self):
        return f'{self.read}{self.write}{self.execute}'

    @property
    def read(self) -> str:
        return self._read
    
    @read.setter
    def read(self, new_permission) -> None:
        self._read = new_permission

    @property
    def write(self) -> str:
        return self._write
    
    @write.setter
    def write(self, new_permission) -> None:
        self._write = new_permission
    
    @property
    def execute(self) -> str:
        return self._execute
    
    @execute.setter
    def execute(self, new_permission) -> None:
        self._execute = new_permission

    def is_executable(self) -> bool:
        return True if self.execute == 'x' else False
    
    def is_writable(self) -> bool:
        return True if self.write == 'w' else False
    
    def is_readable(self) -> bool:
        return True if self.read == 'r' else False

    def octal_notation(self):
        octal_sum = 0
        if self.is_readable():
            octal_sum += 4
        if self.is_writable():
            octal_sum += 2
        if self.is_executable():
            octal_sum += 1
        return octal_sum


class OctalEnum(Enum):
    READ = 4
    WRITE = 2
    EXECUTE = 1


class PermissionEnum(Enum):
    EXECUTE_ONLY = '--x'
    WRITE_ONLY = '-w-'
    READ_ONLY = 'r--'
    READ_WRITE = 'rw-'
    READ_EXECUTE = 'r-x'
    WRITE_EXECUTE = '-wx'
    FULL_PERMISSION = 'rwx'
    NO_PERMISSION = '---'


@dataclass
class Permissions:
    read: str
    write: str
    execute: str

    def is_executable(self) -> bool:
        return True if self.execute == "x" else False
    
    def is_writable(self) -> bool:
        return True if self.write == "w" else False
    
    def is_readable(self) -> bool:
        return True if self.read == "r" else False


    





class InfoFile:
    def __init__(self, file: File):
        self.info_file = stat(file.path)
    
    @property
    def size(self) -> str:
        return self.info_file.st_size
    
    @property
    def mode(self):
        return self.info_file.st_mode
    
