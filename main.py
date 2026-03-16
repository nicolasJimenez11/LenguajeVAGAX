from antlr4 import InputStream, CommonTokenStream
from grammar.generated.VagaxLexer import VagaxLexer
from grammar.generated.VagaxParser import VagaxParser
from interpreter import VAGAXInterpreter
from librerias.archivos import leer_archivo


def main():
    try:
        nombre_archivo = input("Ingrese el archivo .vagax: ").strip()
        ruta = f"ejemplos/{nombre_archivo}"

        codigo = leer_archivo(ruta)

        input_stream = InputStream(codigo)
        lexer = VagaxLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = VagaxParser(stream)
        tree = parser.program()

        interpreter = VAGAXInterpreter()
        interpreter.visit(tree)

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()