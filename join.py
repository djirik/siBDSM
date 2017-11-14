#!/usr/bin/python
import os, sys

_Size_To_Read = 1024
def join(_Src_Dirc, _Dest_file):
    _Output_File = open(_Dest_file, 'wb')
    _List_of_Parts  = os.listdir(_Src_Dirc)
    _List_of_Parts.sort(  )
    for _file in _List_of_Parts:
        _Full_File_Path = os.path.join(_Src_Dirc, _file)
        _Part_of_File  = open(_Full_File_Path, 'rb')
        while 1:
            _Bytes_of_File = _Part_of_File.read(_Size_To_Read)
            if not _Bytes_of_File: break
            _Output_File.write(_Bytes_of_File)
        _Part_of_File.close(  )
    _Output_File.close(  )

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: join.py dir-name file-name')
    else:
        if len(sys.argv) != 3:
            _Interactive_Mode = 1
            _Src_Dirc = input('Directory containing file parts? ')
            _Dest_file  = input('Name of output file? ')
        else:
            _Interactive_Mode = 0
            _Src_Dirc, _Dest_file = sys.argv[1:]
        _From, _To = map(os.path.abspath, [_Src_Dirc, _Dest_file])
        print("Joining " + str(_From) +  " to make " +  str(_To))
        try:
            join(_Src_Dirc, _Dest_file)
        except:
            print('Error occure while joining files:')
            print(sys.exc_type, sys.exc_value)
        else:
           print("Join complete: see " + str(_To))
        if _Interactive_Mode: input('Press Enter key')