from typing import Any, Dict, List

# Importaciones absolutas para evitar bucles circulares con src/__init__.py
from src.parsing.prompts import Prompt
from src.parsing.functions_definition import FunctionDefinition
from src.Objects.Model import Model


class PromptProcessor:
    """Object specialized in prompts processing"""

    def __init__(self,
                 prompts: List[Prompt],
                 functions_definition: List[FunctionDefinition],
                 llm: Model):
        self.__prompts = prompts
        self.__functions_definition = functions_definition
        self.__llm = llm
        self.nb_prompts = len(prompts)

    def process(self) -> List[Any]:
        """Process the list of prompts

        Returns:
            List[Any]: list of outputs for each process
        """
        output = []

        for prompt in self.__prompts:
            prompt_output: Dict[Any, Any] = {}

            # Prompt
            prompt_output['prompt'] = prompt.prompt

            # Name
            fn_name = self.generate_fn_name(prompt)
            prompt_output['name'] = fn_name

            # Parameters
            params = self.generate_parameters(prompt, fn_name)
            prompt_output['parameters'] = params

            output.append(prompt_output)
            print(prompt_output)

        return output

    def get_available_functions(self) -> List[Any]:
        """Returns the list of available functions"""
        available_functions = []
        for function in self.__functions_definition:
            available_functions.append({
                'name': function.name,
                'description': function.description
            })
        return available_functions

    def generate_fn_name(self, prompt: Prompt) -> Any:
        """Given a prompt, returns the most useful function of the
        PromptProcessor's functions to solve the prompt"""
        available_functions = self.get_available_functions()
        function_progress = ''

        while True:
            prompt_message = (
                'Here are the different functions available: '
                f'{available_functions}. To resolve the prompt, "{prompt.prompt}".'
            )

            for generation in self.__llm.predict_multiple_tokens(
                prompt_message=prompt_message,
                previous_tokens=function_progress
            ):
                remaining_functions = []
                for function in available_functions:
                    if function['name'].startswith(function_progress + generation):
                        remaining_functions.append(function)

                if len(remaining_functions) == 1:
                    return remaining_functions[0]['name']
                elif len(remaining_functions) > 1 and generation != '':
                    function_progress = function_progress + generation
                    available_functions = remaining_functions
                    break

    def generate_parameters(self, prompt_message: Prompt,
                            function_name: str) -> Dict[Any, Any]:
        """Given a prompt and the function for this prompt,
        returns the arguments to execute correctly the function."""
        definition = None
        for function_def in self.__functions_definition:
            if function_def.name == function_name:
                definition = function_def
                break

        # Si no encuentra la definición, aborta de forma segura evitando UnboundLocalError
        if not definition:
            return {}

        output: Dict[str, Any] = {}
        for param in definition.parameters:
            previous_gen = ''
            for arg in output.keys():
                previous_gen = previous_gen + arg + '=' + str(output[arg]) + '\n'
            previous_gen = previous_gen + param + '='

            if definition.parameters[param]['type'] == 'string':
                output[param] = self.generate_str_parameter(
                    prompt_message, definition, previous_gen)
            elif definition.parameters[param]['type'] == 'number':
                output[param] = self.generate_int_parameter(
                    prompt_message, definition, previous_gen)
        return output

    def generate_int_parameter(self, prompt_message: Prompt,
                               function: FunctionDefinition,
                               previous_gen: str) -> float:
        """Generate a float parameter, from a given function and its parameters."""
        prompt = (
            f"To solve the prompt {prompt_message}, you will use the following function: "
            f"{function.full_definition}. Provide each parameter. Keep it concise and don't add "
            "custom fields."
        )

        argument_progress = ''
        while True:
            for generation in self.__llm.predict_multiple_tokens(
                prompt_message=prompt,
                previous_tokens=previous_gen + argument_progress
            ):
                if generation == '':
                    try:
                        return float(argument_progress)
                    except ValueError:
                        argument_progress = ''

                regex = '-0123456789.\n'
                stop = False
                for character in generation:
                    if character not in regex:
                        stop = True
                if stop:
                    continue

                if (argument_progress + generation).count('.') >= 2:
                    continue

                if (argument_progress + generation).count('-') >= 2:
                    continue

                if (argument_progress + generation).count('-') == 1 \
                        and (argument_progress + generation)[0] != '-':
                    continue

                argument_progress = argument_progress + generation
                if '\n' in argument_progress:
                    argument_progress = argument_progress.split('\n')[0]
                    if argument_progress is None:
                        continue
                    try:
                        return float(argument_progress)
                    except ValueError:
                        argument_progress = ''
                break

    def generate_str_parameter(self, prompt_message: Prompt,
                               function: FunctionDefinition,
                               previous_gen: str) -> Any:
        """Generate a string parameter, from a given function and its parameters."""
        prompt = (
            f"To solve the prompt {prompt_message}, you will use the following function: "
            f"{function.full_definition}. Provide each parameter. Keep it concise and don't add custom fields."
        )

        argument_progress = ''
        while '\n' not in argument_progress:
            generation = self.__llm.predict_token(
                prompt_message=prompt,
                previous_tokens=previous_gen + argument_progress
            )
            if generation == '':
                return argument_progress

            argument_progress = argument_progress + generation

            if '\n' in argument_progress:
                return argument_progress.split('\n')[0]
        return argument_progress

    def get_prompts(self) -> List[Prompt]:
        """Getter function for the PromptProcessor.__prompts"""
        return self.__prompts
