import os
import stat


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
