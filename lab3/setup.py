from distutils.core import setup, Extension

math_ops_module = Extension('_math_ops',
   sources=['math_ops_wrap.c', 'math_ops.c'],
)

setup (name = 'math_ops',
   version = '0.1',
   author = "Nikita Trynus",
   ext_modules = [math_ops_module],
   py_modules = ["math_ops"],
)
