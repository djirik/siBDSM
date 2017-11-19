#!/usr/bin/python
import sys, os

#_chunk_Size = int(1.4 * 1000 * 1024)                            # Size of _Chunk_From_File


def split(_File_to_Split, _Dir_To_Wtite_to, _chunk_Size):
    if not os.path.exists(_Dir_To_Wtite_to):                    # if the dir is not exist
        os.mkdir(_Dir_To_Wtite_to)                              # then create it
    else:
        for fname in os.listdir(_Dir_To_Wtite_to):              # if there are files in the directory
            os.remove(os.path.join(_Dir_To_Wtite_to, fname))    # Delete them
    _Number_of_Chunks = 0
    input = open(_File_to_Split, 'rb')                          # open file as binary
    _chunks = []
    while 1:                                                    # start spliting
        _Chunk_From_File = input.read(_chunk_Size)              # read file at the size of the Chunk
        if not _Chunk_From_File: break
        _chunks.append(_Chunk_From_File)

        _Number_of_Chunks = _Number_of_Chunks+1
        _Name_of_The_file = os.path.join(_Dir_To_Wtite_to, ('part%04d' % _Number_of_Chunks)) # Create a file with the current chunk order
        _File_To_Write_to = open(_Name_of_The_file, 'wb')              # Open the file in write binary mode
        _File_To_Write_to.write(_Chunk_From_File)                       # Write to the file
        _File_To_Write_to.close()                                       # close the file 
    input.close()
    assert _Number_of_Chunks <= 9999                                    # join sort fails if 5 digits
    return (_Number_of_Chunks, _chunks)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':                   # if the argumet is not enough          
        print('Usage: split.py file target_dir [_chunk_Size]')  # print the help message 
    else:
        if len(sys.argv) < 3:                                           # if the fucking user didn't specify 3 aurg 
            _Interactive_Mode = 1
            _File_to_Split = input('File to be split? ')            # display the help message 
            _Dir_To_Wtite_to = input('Directory to store part files? ')
        else:                                                           # user is using the program correctly
            _Interactive_Mode = 0
            _File_to_Split, _Dir_To_Wtite_to = sys.argv[1:3]            # 1 = file, 2 = dir
            if len(sys.argv) == 4: _chunk_Size = int(sys.argv[3])       # user specify the chunk size      
        _File_Name, _dir = map(os.path.abspath, [_File_to_Split, _Dir_To_Wtite_to])
        print("Splitting " + str(_File_Name) + " to " + str(_dir) + " by " + str(_chunk_Size))
        try:
            _Num_of_Parts = split(_File_to_Split, _Dir_To_Wtite_to, _chunk_Size)    # Get the number of parts
        except:                                                         # Error Message
            print('Error during split:')
            print(sys.exc_type, sys.exc_value)
        else:                                                           # Everything is ok
            print('Split finished: ' + str(_Num_of_Parts) + ' _Num_of_Parts are in ' + str(_dir))
        if _Interactive_Mode: input('Press Enter key')              # If Interactive, display the final message