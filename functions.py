import sys

def print_hello_world():
    print("Hello World")


def print_name(name: str):
    print(name)


def execute(fn_name: str, *args):
    method_to_call = getattr(sys.modules[__name__], fn_name)
    if not args:
        print(f"Invoking functions.{method_to_call.__name__}()")
        return method_to_call()
    else:
        print(f"Invoking functions.{method_to_call.__name__}() with args - {args}")
        return method_to_call(args[0])
