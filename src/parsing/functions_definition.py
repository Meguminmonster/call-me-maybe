import json
from typing import List, Dict
from pydantic import BaseModel


class FunctionDefinition(BaseModel):
    """Modelo Pydantic para mapear la firma de una función disponible."""
    name: str
    description: str
    parameters: Dict[str, Dict[str, str]]
    returns: Dict[str, str]

    @property
    def full_definition(self) -> str:
        """Genera una representación en texto plano (JSON) de la función.
        Esto es lo que PromptProcessor le inyecta al LLM en el prompt."""
        return json.dumps({
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "returns": self.returns
        }, ensure_ascii=False)


def get_functions_definition(file_path: str) -> List[FunctionDefinition]:
    """Lee el catálogo de funciones y devuelve una lista de FunctionDefinition."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not isinstance(data, list):
        raise ValueError("El archivo de definición de funciones debe ser una lista JSON.")
        
    return [FunctionDefinition(**item) for item in data]
