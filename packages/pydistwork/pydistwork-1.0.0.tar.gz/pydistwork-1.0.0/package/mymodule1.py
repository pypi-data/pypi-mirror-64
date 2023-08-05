# within package/mymodule1.py, for example
import pkgutil


def main():
    data = pkgutil.get_data(__name__, "templates/temp_file")
    print("data:", repr(data))
    text = pkgutil.get_data(__name__, "templates/temp_file").decode()
    print("text:", repr(text))