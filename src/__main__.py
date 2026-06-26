import sys
import json
from pathlib import Path

from src import (
    Model,
    get_arguments,
    get_functions_definition,
    get_prompts,
    PromptProcessor,
)


def main() -> None:

    # Parsing de argumentos
    try:
        args = get_arguments()
    except Exception as e:
        print(f"Invalid arguments. {e}", file=sys.stderr)
        sys.exit(1)

    # Carga de definiciones de funciones y prompts
    try:
        functions_definition = get_functions_definition(
            args.functions_definition
        )
        prompts = get_prompts(args.input)
    except Exception as e:
        print(f"Error loading input files: {e}", file=sys.stderr)
        sys.exit(1)

    # Carga del modelo LLM
    try:
        llm = Model(model_name=args.model, device=args.device)
    except Exception as e:
        print("Error when loading the model. "
              "Please make sure to provide a correct model name/device. "
              f"Details: {e}", file=sys.stderr)
        sys.exit(1)

    # Procesamiento directo
    processor = PromptProcessor(prompts, functions_definition, llm)
    output = processor.process()

    # Guardado del resultado en formato JSON legible
    try:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(output, output_file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Could not write to the json output. {e}", file=sys.stderr)
        sys.exit(1)

    return None


if __name__ == "__main__":
    main()
