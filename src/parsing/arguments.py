import argparse


def get_arguments() -> argparse.Namespace:
    """Configura y parsea los argumentos pasados por la línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Herramienta CLI de Function Calling para Small LLM."
    )

    parser.add_argument(
        "-f", "--functions-definition",
        required=True,
        help="Ruta al archivo JSON con las definiciones de las funciones."
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Ruta al archivo JSON que contiene los prompts de prueba."
    )

    parser.add_argument(
        "-m", "--model",
        default="small-llm",
        help="Nombre o identificador del modelo LLM a cargar"
    )

    parser.add_argument(
        "-d", "--device",
        default="cpu",
        help="Dispositivo donde correr el modelo."
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Ruta al archivo JSON donde se guardarán los resultados."
    )

    return parser.parse_args()
