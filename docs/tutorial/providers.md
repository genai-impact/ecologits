# Supported providers

## List of all providers

| Provider name       | Extra for installation | Guide                                                                                            | 
|---------------------|------------------------|--------------------------------------------------------------------------------------------------| 
| Anthropic           | `anthropic`            | [Guide for Anthropic :octicons-link-16:](providers/anthropic.md)                                 |
| Cohere              | `cohere`               | [Guide for Cohere :octicons-link-16:](providers/cohere.md)                                       |
| Google Gemini       | `google-generativeai`  | [Guide for Google Gemini :octicons-link-16:](providers/google.md)                                |
| Hugging Face Hub    | `huggingface-hub`      | [Guide for Hugging Face Hub :octicons-link-16:](providers/huggingface_hub.md)                    |
| LiteLLM             | `litellm`              | [Guide for LiteLLM :octicons-link-16:](providers/litellm.md)                                     |
| Mistral AI `>1.0.0` | `mistralai`            | [Guide for Mistral AI v0 (soon deprecated) :octicons-link-16:](providers/mistralai_v0.md)                                |
| Mistral AI `<=1.0.0`| `mistralai`            | [Guide for Mistral AI v1 :octicons-link-16:](providers/mistralai_v1.md)                                |
| OpenAI              | `openai`               | [Guide for OpenAI :octicons-link-16:](providers/openai.md)                                       |
| Azure OpenAI        | `openai`               | [Guide for Azure OpenAI :octicons-link-16:](providers/openai.md#compatibility-with-azure-openai) |


## Chat Completions

| Provider        |            Completions             |       Completions (stream)        |        Completions (async)        |   Completions (async + stream)    |
|-----------------|:----------------------------------:|:---------------------------------:|:---------------------------------:|:---------------------------------:|
| Anthropic       | :material-checkbox-marked-circle:  |  :material-check-circle-outline:  | :material-checkbox-marked-circle: |  :material-check-circle-outline:  |
| Cohere          | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |
| Google Gemini   | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |
| HuggingFace Hub | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |
| LiteLLM         | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |
| Mistral AI      | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |
| OpenAI          | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |
| Azure OpenAI    | :material-checkbox-marked-circle:  | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: | :material-checkbox-marked-circle: |

Partial support for Anthropic streams, see full documentation: [Anthropic provider](providers/anthropic.md).
