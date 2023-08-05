import os
import stat
import pwd
import grp

class FileInfoMixin:

    @property
    def size(self):
        return os.stat(self.path).st_size
    
    @property
    def inode(self):
        return os.stat(self.path).st_ino
    
    @property
    def mode(self):
        return stat.filemode(os.stat(self.path).st_mode)
    
    @property
    def change_at(self):
        return os.stat(self.path).st_ctime
    
    @property
    def modify_at(self):
        return os.stat(self.path).st_mtime

    @property
    def access_at(self):
        return os.stat(self.path).st_atime
    
    @property
    def uid(self):
        return os.stat(self.path).st_uid
    
    @property
    def gid(self):
        return os.stat(self.path).st_gid
    
    @property
    def dev(self):
        return os.stat(self.path).st_dev
    
    @property
    def links(self):
        return os.stat(self.path).st_nlink

    @property
    def owner_name(self):
        return pwd.getpwuid(self.uid).pw_name
    
    @property
    def owner_directory(self):
        return pwd.getpwuid(self.uid).pw_dir

    @property
    def owner_shell(self):
        return pwd.getpwuid(self.uid).pw_shell

    @property
    def group_name(self):
        return grp.getgrgid(self.gid).gr_name
