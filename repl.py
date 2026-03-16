from antlr4 import InputStream, CommonTokenStream
from grammar.generated.VagaxLexer import VagaxLexer
from grammar.generated.VagaxParser import VagaxParser
from interpreter import VagaxInterpreter


def main():
    print("REPL de VAGAX")
    print("Escribe 'salir' para terminar.\n")

    interpreter = VagaxInterpreter()

    while True:
        try:
            codigo = input("vagax > ").strip()

            if codigo.lower() in ["salir", "exit", "quit"]:
                print("Saliendo de VAGAX...")
                break

            if not codigo:
                continue

            input_stream = InputStream(codigo)
            lexer = VagaxLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = VagaxParser(stream)

            tree = parser.program()

            interpreter.visit(tree)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()