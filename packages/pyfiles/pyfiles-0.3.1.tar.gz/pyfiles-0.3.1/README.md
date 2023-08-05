# pyfiles
management for files with python

## Quickstart
### simple usage:
```
from pyfiles.file import File

file = File('some/file.example')

print(file.path)
-> Path('some/file.example)
```

### permissions:
```
print(file.permission.owner)
-> 'rwx'

print(file.permission.onwer.is_executable)
-> True

print(file.permission.onwer.is_writable)
-> True

print(file.permission.onwer.is_readable)
-> True

file.permission.change_permission('owner', 'execute')
-> grants or revokes execution permission to the owner of the file

file.permission.change_permission('group', 'read')
-> grants or revokes read permission to the file group

file.permission.change_permission('others', 'write')
-> grants or revokes write permission to others

```


### cogrant or revoke permission for read to the file's groupntent:
```
for line in file.content.read_only():
    print(line)
```



