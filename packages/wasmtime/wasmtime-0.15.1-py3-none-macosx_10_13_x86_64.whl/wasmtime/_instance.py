from ._ffi import *
from ctypes import *
from wasmtime import Module, Extern, Func, Table, Memory, Trap, Global

dll.wasm_instance_new.restype = P_wasm_instance_t


class Instance(object):
    def __init__(self, module, imports):
        """
        Creates a new instance by instantiating the `module` given with the
        `imports` provided.

        The `module` must have type `Module`, and the `imports` must be an
        iterable of external values, either `Extern`, `Func`, `Table`, `Memory`,
        or `Global`.

        Raises an error if instantiation fails (e.g. linking or trap) and
        otherwise initializes the new instance.
        """

        if not isinstance(module, Module):
            raise TypeError("expected a Module")

        import_types = module.imports()
        if len(imports) != len(import_types):
            raise RuntimeError("wrong number of imports provided")
        imports_ffi = (P_wasm_extern_t * len(import_types))()
        for i, ty in enumerate(import_types):
            val = imports[i]
            if isinstance(val, Extern):
                imports_ffi[i] = val.__ptr__
            elif isinstance(val, Func):
                imports_ffi[i] = val.as_extern().__ptr__
            elif isinstance(val, Memory):
                imports_ffi[i] = val.as_extern().__ptr__
            elif isinstance(val, Global):
                imports_ffi[i] = val.as_extern().__ptr__
            elif isinstance(val, Table):
                imports_ffi[i] = val.as_extern().__ptr__
            else:
                raise TypeError("expected an external item as an import")

        trap = P_wasm_trap_t()
        ptr = dll.wasm_instance_new(
            module.store.__ptr__, module.__ptr__, imports_ffi, byref(trap))
        if not ptr:
            if trap:
                raise Trap.__from_ptr__(trap)
            raise RuntimeError("failed to compile instance")
        self.__ptr__ = ptr
        self._module = module

    @classmethod
    def __from_ptr__(cls, ptr, module):
        ty = cls.__new__(cls)
        if not isinstance(ptr, P_wasm_instance_t):
            raise TypeError("wrong pointer type")
        ty.__ptr__ = ptr
        ty._module = module
        return ty

    def exports(self):
        """
        Returns the exports of this module
        """
        externs = ExternTypeList()
        dll.wasm_instance_exports(self.__ptr__, byref(externs.vec))
        ret = []
        for i in range(0, externs.vec.size):
            ret.append(Extern.__from_ptr__(externs.vec.data[i], externs))
        return ret

    def get_export(self, name):
        """
        Gets an export from this module by name, returning `None` if the name
        doesn't exist.
        """
        if not hasattr(self, '_export_map'):
            self._export_map = {}
            exports = self.exports()
            for i, export in enumerate(self._module.exports()):
                self._export_map[export.name()] = exports[i]
        if name in self._export_map:
            return self._export_map[name]
        else:
            return None

    def __del__(self):
        if hasattr(self, '__ptr__'):
            dll.wasm_instance_delete(self.__ptr__)


class ExternTypeList(object):
    def __init__(self):
        self.vec = wasm_extern_vec_t(0, None)

    def __del__(self):
        dll.wasm_extern_vec_delete(byref(self.vec))
