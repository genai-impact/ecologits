# Mistral AI

??? warning "Deprecation of Mistral AI v0"

    Mistral AI python client with version `<1.0.0` will no longer be supported by EcoLogits. See official [migration guide from v0 to v1 :octicons-link-external-16:](https://github.com/mistralai/client-python/blob/main/MIGRATION.md). 

!!! warning "Lack of transparency"
    
    Some models released by Mistral AI are not open-weights, plus there is no information on the inference infrastructure. Thus, the environmental impacts are estimated with a lower precision.


This guide focuses on the integration of :seedling: **EcoLogits** with the [Mistral AI official python client :octicons-link-external-16:](https://github.com/mistralai/client-python).

Official links:

* Repository: [:simple-github: mistralai/client-python](https://github.com/mistralai/client-python)
* Documentation: [:material-file-document: docs.mistral.ai](https://docs.mistral.ai/getting-started/clients/)


## Installation

To install EcoLogits along with all necessary dependencies for compatibility with the Mistral AI client, please use the `mistralai` extra-dependency option as follows:

```shell
pip install ecologits[mistralai]
```

This installation command ensures that EcoLogits is set up with the specific libraries required to interface seamlessly with Mistral AI's Python client.


## Chat Completions

### Example

Integrating EcoLogits with your applications does not alter the standard outputs from the API responses. Instead, it enriches them by adding the `Impacts` object, which contains detailed environmental impact data.

=== "Sync"

    ``` { .python .annotate }
    from ecologits import EcoLogits
    from mistralai import Mistral
    
    # Initialize EcoLogits
    EcoLogits.init(providers=["mistralai"])
    
    client = Mistral(api_key="<MISTRAL_API_KEY>")

    response = client.chat.complete(# (1)! 
        messages=[
            {"role": "user", "content": "Tell me a funny joke!"}
        ],
        model="mistral-tiny"
    )
    
    # Get estimated environmental impacts of the inference
    print(response.impacts)
    ```
    
    1. Use `client.chat` for Mistral AI v0.

=== "Async"

    ```python
    import asyncio
    from ecologits import EcoLogits
    from mistralai import Mistral
    
    # Initialize EcoLogits
    EcoLogits.init(providers=["mistralai"])
    
    client = Mistral(api_key="<MISTRAL_API_KEY>")
    
    async def main() -> None:
        response = await client.chat.complete_async(# (1)! 
            messages=[
                {"role": "user", "content": "Tell me a funny joke!"}
            ],
            model="mistral-tiny"
        )
        
        # Get estimated environmental impacts of the inference
        print(response.impacts)
    
    
    asyncio.run(main())
    ```
    
    1. Use `client.chat` for Mistral AI v0.


### Streaming example

**In streaming mode, the impacts are calculated incrementally**, which means you don't need to sum the impacts from each data chunk. Instead, the impact information in the last chunk reflects the total cumulative environmental impacts for the entire request.

=== "Sync"

    ```python
    from ecologits import EcoLogits
    from mistralai import Mistral
    
    # Initialize EcoLogits
    EcoLogits.init(providers=["mistralai"])
    
    client = Mistral(api_key="<MISTRAL_API_KEY>")
    
    stream = client.chat.stream(# (1)! 
        messages=[
            {"role": "user", "content": "Tell me a funny joke!"}
        ],
        model="mistral-tiny"
    )
    
    for chunk in stream:
        # Get cumulative estimated environmental impacts of the inference
        print(chunk.data.impacts) # (2)!  
    ```

    1. Use `client.chat_stream` for Mistral AI v0.
    2. Use `chunk.impacts` for Mistral AI v0.

=== "Async"
    
    ```python
    import asyncio
    from ecologits import EcoLogits
    from mistralai import Mistral
    
    # Initialize EcoLogits
    EcoLogits.init(providers=["mistralai"])
    
    client = Mistral(api_key="<MISTRAL_API_KEY>")
    
    async def main() -> None:
        response = await client.chat.stream_async(# (1)! 
            messages=[
                {"role": "user", "content": "Tell me a funny joke!"}
            ],
            model="mistral-tiny"
        )
        
        async for chunk in stream:
            # Get cumulative estimated environmental impacts of the inference
            if hasattr(chunk, "impacts"):
                print(chunk.data.impacts) # (2)!  
    
    
    asyncio.run(main())
    ```

    1. Use `client.chat_stream` for Mistral AI v0.
    2. Use `chunk.impacts` for Mistral AI v0.
    
