# Anthropic

This guide focuses on the integration of :seedling: **EcoLogits** with the [Anthropic official python client :octicons-link-external-16:](https://github.com/anthropics/anthropic-sdk-python).

Official links:

* Repository: [:simple-github: anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)
* Documentation: [:material-file-document: docs.anthropic.com](https://docs.anthropic.com)

## Installation

To install EcoLogits along with all necessary dependencies for compatibility with the Anthropic client, please use the `anthropic` extra-dependency option as follows:

```shell
pip install ecologits[anthropic]
```

This installation command ensures that EcoLogits is set up with the specific libraries required to interface seamlessly with Anthropic's Python client.

## Chat Completions

### Example

Integrating EcoLogits with your applications does not alter the standard outputs from the API responses. Instead, it enriches them by adding the `Impacts` object, which contains detailed environmental impact data.

=== "Sync"

    ```python
    from anthropic import Anthropic
    from ecologits import EcoLogits
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = Anthropic(api_key="<ANTHROPIC_API_KEY>")
    
    response = client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Tell me a funny joke!"}],
        model="claude-3-haiku-20240307",
    )
    
    # Get estimated environmental impacts of the inference
    print(response.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    from anthropic import AsyncAnthropic
    from ecologits import EcoLogits
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = AsyncAnthropic(api_key="<ANTHROPIC_API_KEY>")
    
    async def main() -> None:
        response = await client.messages.create(
            max_tokens=100,
            messages=[{"role": "user", "content": "Tell me a funny joke!"}],
            model="claude-3-haiku-20240307",
        )
        
        # Get estimated environmental impacts of the inference
        print(response.impacts)
    
    
    asyncio.run(main())
    ```


### Streaming example

**In streaming mode, the impacts are calculated in the last chunk for the entire request.**

=== "Sync"

    ```python
    from anthropic import Anthropic
    from ecologits import EcoLogits
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = Anthropic(api_key="<ANTHROPIC_API_KEY>")
    
    with client.messages.stream(
        max_tokens=100,
        messages=[{"role": "user", "content": "Tell me a funny joke!"}],
        model="claude-3-haiku-20240307",
    ) as stream:
        for text in stream.text_stream:
            pass
        # Get estimated environmental impacts of the inference
        print(stream.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    from anthropic import AsyncAnthropic
    from ecologits import EcoLogits
    
    # Initialize EcoLogits
    EcoLogits.init()
    
    client = AsyncAnthropic(api_key="<ANTHROPIC_API_KEY>")
    
    async def main() -> None:
        async with client.messages.stream(
            max_tokens=100,
            messages=[{"role": "user", "content": "Tell me a funny joke!"}],
            model="claude-3-haiku-20240307",
        ) as stream:
            async for text in stream.text_stream:
                pass
            # Get estimated environmental impacts of the inference
            print(stream.impacts)
    
    
    asyncio.run(main())
    ```

