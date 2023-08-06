from ._ffi import *
from ctypes import *
from wasmtime import ExternType

dll.wasm_extern_as_func.restype = P_wasm_func_t
dll.wasm_extern_as_table.restype = P_wasm_table_t
dll.wasm_extern_as_global.restype = P_wasm_global_t
dll.wasm_extern_as_memory.restype = P_wasm_memory_t
dll.wasm_extern_type.restype = P_wasm_externtype_t


class Extern(object):
    @classmethod
    def __from_ptr__(cls, ptr, owner):
        ty = cls.__new__(cls)
        if not isinstance(ptr, P_wasm_extern_t):
            raise TypeError("wrong pointer type")
        ty.__ptr__ = ptr
        ty.__owner__ = owner
        return ty

    def type(self):
        """
        Returns the type of this `Extern` as an `ExternType`
        """
        val = dll.wasm_extern_type(self.__ptr__)
        return ExternType.__from_ptr__(val, None)

    def func(self):
        """
        Returns this type as a `Func` or `None` if it's not a function
        """
        from wasmtime import Func

        val = dll.wasm_extern_as_func(self.__ptr__)
        if val:
            return Func.__from_ptr__(val, self.__owner__ or self)
        else:
            return None

    def table(self):
        """
        Returns this type as a `Table` or `None` if it's not a table
        """
        from wasmtime import Table

        val = dll.wasm_extern_as_table(self.__ptr__)
        if val:
            return Table.__from_ptr__(val, self.__owner__ or self)
        else:
            return None

    def global_(self):
        """
        Returns this type as a `Global` or `None` if it's not a global
        """
        from wasmtime import Global

        val = dll.wasm_extern_as_global(self.__ptr__)
        if val:
            return Global.__from_ptr__(val, self.__owner__ or self)
        else:
            return None

    def memory(self):
        """
        Returns this type as a `Memory` or `None` if it's not a memory
        """
        from wasmtime import Memory

        val = dll.wasm_extern_as_memory(self.__ptr__)
        if val:
            return Memory.__from_ptr__(val, self.__owner__ or self)
        else:
            return None

    def __call__(self, *params):
        return self.func()(*params)

    def __del__(self):
        if hasattr(self, '__owner__') and self.__owner__ is None:
            dll.wasm_extern_delete(self.__ptr__)
