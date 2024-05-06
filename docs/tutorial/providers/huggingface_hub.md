# Hugging Face Hub

This guide is focuses on the integration of :seedling: **EcoLogits** with the [Hugging Face Hub official python client :octicons-link-external-16:](https://github.com/huggingface/huggingface_hub).

Official links:

* Repository: [:simple-github: huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub)
* Documentation: [:material-file-document: huggingface.co](https://huggingface.co/docs/huggingface_hub/index)


## Installation

To install EcoLogits along with all necessary dependencies for compatibility with the Hugging Face Hub client, please use the `huggingface-hub` extra-dependency option as follows:

```shell
pip install ecologits[huggingface-hub]
```

This installation command ensures that EcoLogits is set up with the specific libraries required to interface seamlessly with Hugging Face Hub's Python client.

## Chat Completions

### Example

Integrating EcoLogits with your applications does not alter the standard outputs from the API responses. Instead, it enriches them by adding the `Impacts` object, which contains detailed environmental impact data.

=== "Sync"

    ```python
    from ecologits import EcoLogits
    from huggingface_hub import InferenceClient
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Tell me a funny joke!"}],
        max_tokens=15
    )
    
    # Get estimated environmental impacts of the inference
    print(response.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    from ecologits import EcoLogits
    from huggingface_hub import AsyncInferenceClient
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = AsyncInferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    
    async def main() -> None:
        response = await client.chat_completion(
            messages=[{"role": "user", "content": "Tell me a funny joke!"}],
            max_tokens=15
        )
        
        # Get estimated environmental impacts of the inference
        print(response.impacts)
    
    
    asyncio.run(main())
    ```


### Streaming example

**In streaming mode, the impacts are calculated incrementally**, which means you don't need to sum the impacts from each data chunk. Instead, the impact information in the last chunk reflects the total cumulative environmental impacts for the entire request.

=== "Sync"

    ```python
    from ecologits import EcoLogits
    from huggingface_hub import InferenceClient
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    stream = client.chat_completion(
        messages=[{"role": "user", "content": "Tell me a funny joke!"}],
        max_tokens=15,
        stream=True
    )
    
    for chunk in stream:
        # Get cumulative estimated environmental impacts of the inference
        print(chunk.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    from ecologits import EcoLogits
    from huggingface_hub import AsyncInferenceClient
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = AsyncInferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    
    async def main() -> None:
        stream = await client.chat_completion(
            messages=[{"role": "user", "content": "Tell me a funny joke!"}],
            max_tokens=15,
            stream=True
        )
        
        async for chunk in stream:
            # Get cumulative estimated environmental impacts of the inference
            print(chunk.impacts)
    
    
    asyncio.run(main())
    ```

