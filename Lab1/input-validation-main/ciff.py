# import struct


# class CIFF:
#     """
#     Holds data of a CIFF image
#     """

#     def __init__(
#             self,
#             magic_chars="CIFF",
#             header_size_long=0,
#             content_size_long=0,
#             width_long=0,
#             height_long=0,
#             caption_string="",
#             tags_list=None,
#             pixels_list=None
#     ):
#         """
#         Constructor for CIFF images

#         :param magic_chars: the magic "CIFF" characters
#         :param header_size_long: size of the header in bytes (8-byte-long int)
#         :param content_size_long: size of content in bytes 8-byte-long int)
#         :param width_long: width of the image (8-byte-long int)
#         :param height_long: height of the image (8-byte-long int)
#         :param caption_string: caption of the image (string)
#         :param tags_list: list of tags in the image
#         :param pixels_list: list of pixels to display
#         """
#         self._magic = magic_chars
#         self._header_size = header_size_long
#         self._content_size = content_size_long
#         self._width = width_long
#         self._height = height_long
#         self._caption = caption_string
#         if tags_list is None:
#             self._tags = []
#         else:
#             self._tags = tags_list
#         if pixels_list is None:
#             self._pixels = []
#         else:
#             self._pixels = pixels_list
#         self._is_valid = True

#     #
#     # Properties
#     #

#     @property
#     def is_valid(self):
#         """
#         A flag indicating whether the the CIFF image conforms
#         with the specification or not

#         :return: boolean
#         """
#         return self._is_valid

#     @is_valid.setter
#     def is_valid(self, value):
#         self._is_valid = value

#     @property
#     def magic(self):
#         """
#         The parsed magic characters

#         :return: str
#         """
#         return self._magic

#     @magic.setter
#     def magic(self, value):
#         self._magic = value

#     @property
#     def header_size(self):
#         """
#         The parsed header size

#         :return: int
#         """
#         return self._header_size

#     @header_size.setter
#     def header_size(self, value):
#         self._header_size = value

#     @property
#     def content_size(self):
#         """
#         The parsed content size

#         :return: int
#         """
#         return self._content_size

#     @content_size.setter
#     def content_size(self, value):
#         self._content_size = value

#     @property
#     def width(self):
#         """
#         The parsed width of the image

#         :return: int
#         """
#         return self._width

#     @width.setter
#     def width(self, value):
#         self._width = value

#     @property
#     def height(self):
#         """
#         The parsed height of the image

#         :return: int
#         """
#         return self._height

#     @height.setter
#     def height(self, value):
#         self._height = value

#     @property
#     def caption(self):
#         """
#         The parsed image caption

#         :return: str
#         """
#         return self._caption

#     @caption.setter
#     def caption(self, value):
#         self._caption = value

#     @property
#     def tags(self):
#         """
#         The parsed list of tags

#         :return: list of strings
#         """
#         return self._tags

#     @tags.setter
#     def tags(self, value):
#         self._tags = value

#     @property
#     def pixels(self):
#         """
#         The parsed pixels

#         :return: list
#         """
#         return self._pixels

#     @pixels.setter
#     def pixels(self, value):
#         self._pixels = value

#     #
#     # Static methods
#     #

#     @staticmethod
#     def parse_ciff_file(file_path):
#         """
#         Parses a CIFF file and constructs the corresponding object

#         TODO: make sure that malformed input cannot crash the parsing method

#         :param file_path: path the to file to be parsed (string)
#         :return: the parsed CIFF object
#         """
#         new_ciff = CIFF()
#         bytes_read = 0
#         # the following code can throw Exceptions at multiple lines
#         # TODO: surround the parsing code with a try-except block and
#         # TODO: set the is_valid property to False
#         # TODO: if an Exception has been raised
#         try:
#             with open(file_path, "rb") as ciff_file:
#                 # read the magic bytes
#                 magic = ciff_file.read(4)
#                 # read may not return the requested number of bytes
#                 # TODO: magic must contain 4 bytes. If not, raise Exception
#                 if len(magic) != 4:
#                     raise Exception("Magic must contain 4 bytes!")
#                 bytes_read += 4
#                 # decode the bytes as 4 characters
#                 new_ciff.magic = magic.decode('ascii')
#                 # TODO: the magic must be "CIFF". If not, raise Exception
#                 if new_ciff.magic != "CIFF":
#                     raise Exception("Invalid magic characters!")
                
#                 # read the header size
#                 h_size = ciff_file.read(8)
#                 # TODO: h_size must contain 8 bytes. If not, raise Exception
#                 if len(h_size) != 8:
#                     raise Exception("Header size must contain 8 bytes!")
                
#                 bytes_read += 8
#                 # interpret the bytes as an 8-byte-long integer
#                 # unpack returns a list
#                 # HINT: check the "q" format specifier!
#                 # HINT: Does it fit our purposes?
#                 new_ciff.header_size = struct.unpack("q", h_size)[0]
#                 # the header size must be in [38, 2^64 - 1]
#                 # TODO: check the value range. If not in range, raise Exception
#                 if new_ciff.header_size < 38 \
#                         or new_ciff.header_size > 2**64 - 1:
#                     raise Exception("Invalid header size!")

#                 # read the content size
#                 c_size = ciff_file.read(8)
#                 # TODO: c_size must contain 8 bytes. If not, raise Exception
#                 if len(c_size) != 8:
#                     raise Exception("Content size must contain 8 bytes!")
                
#                 bytes_read += 8
#                 # interpret the bytes as an 8-byte-long integer
#                 # HINT: check out the "q" format specifier!
#                 # HINT: Does it fit our purposes?
#                 new_ciff.content_size = struct.unpack("q", c_size)[0]
#                 # the content size must be in [0, 2^64 - 1]
#                 # TODO: check the value range. If not in range, raise Exception
#                 # Question: is this check necessary?
#                 if new_ciff.content_size < 0:
#                     raise Exception("Invalid content size!")

#                 # read the width
#                 width = ciff_file.read(8)
#                 # TODO: check if width contains 8 bytes
#                 if len(width) != 8:
#                     raise Exception("Width must contain 8 bytes!")
                
#                 bytes_read += 8
#                 # interpret the bytes as an 8-byte-long integer
#                 # HINT: check out the "q" format specifier!
#                 # HINT: Does it fit our purposes?
#                 new_ciff.width = struct.unpack("q", width)[0]
#                 # the width must be in [0, 2^64 - 1]
#                 # TODO: check the value range. If not in range, raise Exception
#                 # Question: is this check necessary?
#                 if new_ciff.width < 0:
#                     raise Exception("Invalid width!")

#                 # read the height
#                 height = ciff_file.read(8)
#                 # TODO: check if height contains 8 bytes
#                 if len(height) != 8:
#                     raise Exception("Height must contain 8 bytes!")
                
#                 bytes_read += 8
#                 # interpret the bytes as an 8-byte-long integer
#                 # HINT: check out the "q" format specifier!
#                 # HINT: Does it fit our purposes?
#                 new_ciff.height = struct.unpack("q", height)[0]
#                 # the height must be in [0, 2^64 - 1]
#                 # TODO: check the value range
#                 # Question: is this check necessary?
#                 if new_ciff.height < 0:
#                     raise Exception("Invalid height!")
#                 # TODO: content size must equal width*height*3
#                 if new_ciff.content_size != new_ciff.width * new_ciff.height * 3:
#                     raise Exception("Invalid content size!")

#                 # read the name of the image character by character
#                 caption = ""
#                 c = ciff_file.read(1)
#                 # TODO: check if c contains 1 byte  
#                 if len(c) != 1:
#                     raise Exception("Invalid image")
                
#                 bytes_read += 1
#                 char = c.decode('ascii')
#                 # read until the first '\n' (caption cannot contain '\n')
#                 while char != '\n':
#                     # append read character to caption
#                     caption += char
#                     # read next character
#                     c = ciff_file.read(1)
#                     # TODO: check if c contains 1 byte
#                     if len(c) != 1:
#                         raise Exception("Invalid image")
#                     bytes_read += 1
#                     char = c.decode('ascii')
#                 new_ciff.caption = caption

#                 # read all the tags
#                 tags = list()
#                 # read until the end of the header
#                 tag = ""
#                 while bytes_read != new_ciff.header_size:
#                     c = ciff_file.read(1)
#                     # TODO: check if c contains 1 byte
#                     if len(c) != 1:
#                         raise Exception("Invalid image")
#                     bytes_read += 1
#                     char = c.decode('ascii')
#                     # tags should not contain '\n'
#                     # TODO: char must not be a '\n'
#                     if char == '\n':
#                         raise Exception("Invalid image")
#                     # tags are separated by terminating nulls
#                     tag += char
#                     if char == '\0':
#                         tags.append(tag)
#                         tag = ""
#                     # the very last character in the header must be a '\0'
#                     # TODO: check the last character of the header
#                     if bytes_read == new_ciff.header_size and char != '\0':
#                         raise Exception("Invalid image")
                
#                 # all tags must end with '\0'
#                 # TODO: check the end of each tag for the '\0'
#                 for tag in tags:
#                     if tag[len(tag)-1] != '\0':
#                         raise Exception("Invalid image")

#                 new_ciff.tags = tags
                
#                 # read the pixels
#                 while bytes_read < new_ciff.header_size+new_ciff.content_size:
#                     c = ciff_file.read(3)
#                     # TODO: check if c contains 3 bytes
#                     if len(c) != 3:
#                         raise Exception("Invalid image")
#                     bytes_read += 3
#                     pixel = struct.unpack("BBB", c)
#                     new_ciff.pixels.append(pixel)

#                 # we should have reached the end of the file
#                 # TODO: try to read a byte. If successful, raise Exception
#                 byte = ciff_file.read(1)
#                 if byte != b'':
#                     raise Exception("Invalid image")

#         except Exception as e:
#             new_ciff.is_valid = False
#             print(e)

#         return new_ciff

import ctypes
import os
from ctypes import c_void_p, c_char_p, c_int64, c_bool

# Load the shared library
_lib_path = os.path.join(os.path.dirname(__file__), 'libciff_parser.so')
_ciff_lib = ctypes.CDLL(_lib_path)

# Define function prototypes
_ciff_lib.parse_ciff.argtypes = [c_char_p]
_ciff_lib.parse_ciff.restype = c_void_p

_ciff_lib.get_is_valid.argtypes = [c_void_p]
_ciff_lib.get_is_valid.restype = c_bool

_ciff_lib.get_magic.argtypes = [c_void_p]
_ciff_lib.get_magic.restype = c_char_p

_ciff_lib.get_header_size.argtypes = [c_void_p]
_ciff_lib.get_header_size.restype = c_int64

_ciff_lib.get_content_size.argtypes = [c_void_p]
_ciff_lib.get_content_size.restype = c_int64

_ciff_lib.get_width.argtypes = [c_void_p]
_ciff_lib.get_width.restype = c_int64

_ciff_lib.get_height.argtypes = [c_void_p]
_ciff_lib.get_height.restype = c_int64

_ciff_lib.get_caption.argtypes = [c_void_p]
_ciff_lib.get_caption.restype = c_char_p

_ciff_lib.free_ciff.argtypes = [c_void_p]
_ciff_lib.free_ciff.restype = None


class CIFF:
    """
    Python wrapper for the C++ CIFF parser
    """
    
    def __init__(self):
        """
        Constructor for CIFF Python wrapper
        """
        self._c_ciff = None
        self._is_valid = True
        self._magic = "CIFF"
        self._header_size = 0
        self._content_size = 0
        self._width = 0
        self._height = 0
        self._caption = ""
        self._tags = []
        self._pixels = []
        
    def __del__(self):
        """
        Destructor to free C++ resources
        """
        if self._c_ciff:
            _ciff_lib.free_ciff(self._c_ciff)
            self._c_ciff = None
    
    @property
    def is_valid(self):
        """
        A flag indicating whether the CIFF image conforms
        with the specification or not
        
        :return: boolean
        """
        if self._c_ciff:
            return _ciff_lib.get_is_valid(self._c_ciff)
        return self._is_valid
    
    @property
    def magic(self):
        """
        The parsed magic characters
        
        :return: str
        """
        if self._c_ciff:
            magic_bytes = _ciff_lib.get_magic(self._c_ciff)
            return magic_bytes.decode('ascii') if magic_bytes else self._magic
        return self._magic
    
    @property
    def header_size(self):
        """
        The parsed header size
        
        :return: int
        """
        if self._c_ciff:
            return _ciff_lib.get_header_size(self._c_ciff)
        return self._header_size
    
    @property
    def content_size(self):
        """
        The parsed content size
        
        :return: int
        """
        if self._c_ciff:
            return _ciff_lib.get_content_size(self._c_ciff)
        return self._content_size
    
    @property
    def width(self):
        """
        The parsed width of the image
        
        :return: int
        """
        if self._c_ciff:
            return _ciff_lib.get_width(self._c_ciff)
        return self._width
    
    @property
    def height(self):
        """
        The parsed height of the image
        
        :return: int
        """
        if self._c_ciff:
            return _ciff_lib.get_height(self._c_ciff)
        return self._height
    
    @property
    def caption(self):
        """
        The parsed image caption
        
        :return: str
        """
        if self._c_ciff:
            caption_bytes = _ciff_lib.get_caption(self._c_ciff)
            return caption_bytes.decode('ascii') if caption_bytes else self._caption
        return self._caption
    
    @property
    def tags(self):
        """
        The parsed list of tags
        
        :return: list of strings
        """
        return self._tags
    
    @property
    def pixels(self):
        """
        The parsed pixels
        
        :return: list
        """
        return self._pixels
    
    @staticmethod
    def parse_ciff_file(file_path):
        """
        Parses a CIFF file using the C++ implementation
        
        :param file_path: path to the file to be parsed (string)
        :return: the parsed CIFF object
        """
        ciff = CIFF()
        
        try:
            # Convert file path to bytes for C function
            file_path_bytes = file_path.encode('utf-8')
            
            # Call the C++ parser
            ciff._c_ciff = _ciff_lib.parse_ciff(file_path_bytes)
            
            if not ciff._c_ciff:
                raise Exception("Failed to parse CIFF file")
                
        except Exception as e:
            ciff._is_valid = False
            print(f"Error parsing CIFF file: {e}")
            
        return ciff
