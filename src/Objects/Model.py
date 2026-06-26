from typing import Any, Generator

from llm_sdk import Small_LLM_Model


class Model(Small_LLM_Model):
    """LLM Class with useful methods"""

    def predict_token(
        self, prompt_message: str, previous_tokens: str = "", skip: int = 0
    ) -> Any:
        """Get the next token from the original prompt + the previously
        generated tokens, as a string."""
        prompt = (
            f"<|im_start|>user\n{prompt_message}<|im_end|>\n"
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{previous_tokens}"
        )

        tensors = self.encode(prompt)
        probabilities = self.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_tokens = sorted(probabilities, reverse=True)
        token = probabilities.index(sorted_tokens[skip])
        return self.decode(token)

    def predict_multiple_tokens(
        self, prompt_message: str, previous_tokens: str = "", skip: int = 0
    ) -> Generator[str]:
        """Returns a generator of the most probable token"""
        prompt = (
            f"<|im_start|>user\n{prompt_message}<|im_end|>\n"
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{previous_tokens}"
        )

        tensors = self.encode(prompt)
        probabilities = self.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_tokens = sorted(probabilities, reverse=True)

        while True:
            yield self.decode(probabilities.index(sorted_tokens[skip]))
            skip += 1
