# LiteLLM

!!! warning "Lack of transparency"

    Depending on the provider, the level of transparency varies. Thus, the environmental impacts can be estimated with a low precision.

This guide focuses on the integration of :seedling: **EcoLogits** with the [LiteLLM official Python client :octicons-link-external-16:](https://github.com/BerriAI/litellm).

Official links:

* Repository: [:simple-github: BerriAI/litellm](https://github.com/BerriAI/litellm)
* Documentation: [:material-file-document: litellm.vercel.app](https://docs.litellm.ai/docs/)


## Installation

To install EcoLogits along with all necessary dependencies for compatibility with LiteLLM, please use the `litellm` extra-dependency option as follows:

```shell
pip install ecologits[litellm]
```

This installation command ensures that EcoLogits is set up with the specific libraries required to interface seamlessly with LiteLLM's Python client.


## Chat Completions

### Example

Integrating EcoLogits with your applications does not alter the standard outputs from the API responses. Instead, it enriches them by adding the `Impacts` object, which contains detailed environmental impact data. **Make sure you have the api key of the provider used in an .env file.** Make sure you call the litellm generation function as "litellm.completion" and not just "completion".

=== "Sync"

    ```python
    from ecologits import EcoLogits
    import litellm
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    response = litellm.completion(
        model="gpt-4o-2024-05-13",
        messages=[{ "content": "Hello, how are you?","role": "user"}]
    )
    
    # Get estimated environmental impacts of the inference
    print(response.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    import litellm
    from ecologits import EcoLogits
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    async def main() -> None:
        response = await litellm.acompletion(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Tell me a funny joke!"}
            ]
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
    import litellm
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    stream = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}],
        stream=True
    )
    
    for chunk in stream:
        # Get cumulative estimated environmental impacts of the inference
        print(chunk.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    import litellm
    from ecologits import EcoLogits
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    async def main() -> None:
        stream = await litellm.acompletion(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Tell me a funny joke!"}
            ]
        )
        
        async for chunk in stream:
            # Get cumulative estimated environmental impacts of the inference
            print(chunk.impacts)
    
    asyncio.run(main())
    ```
