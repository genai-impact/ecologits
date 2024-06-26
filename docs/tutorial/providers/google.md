# Google Gemini

This guide is focuses on the integration of :seedling: **EcoLogits** with the [Google Gemini official python client :octicons-link-external-16:](https://github.com/google-gemini/generative-ai-python).

Official links:

* Repository: [:simple-github: google-gemini/generative-ai-python](https://github.com/google-gemini/generative-ai-python)
* Documentation: [:material-file-document: ai.google.dev](https://ai.google.dev/gemini-api/docs?hl=fr)


## Installation

To install EcoLogits along with all necessary dependencies for compatibility with the Google Gemini client, please use the `google-generativeai` extra-dependency option as follows:

```shell
pip install ecologits[google-generativeai]
```

This installation command ensures that EcoLogits is set up with the specific libraries required to interface seamlessly with Google Gemini Python client.


## Chat Completions

### Example

Integrating EcoLogits with your applications does not alter the standard outputs from the API responses. Instead, it enriches them by adding the `Impacts` object, which contains detailed environmental impact data.

=== "Sync"

    ```python
    from ecologits import EcoLogits
    import google.generativeai as genai
    
    # Initialize EcoLogits
    EcoLogits.init()

    # Ask something to Google Gemini
    genai.configure(api_key="<GOOGLE_API_KEY>")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    
    # Get estimated environmental impacts of the inference
    print(response.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    from ecologits import EcoLogits
    import google.generativeai as genai
    
    # Initialize EcoLogits
    EcoLogits.init()

    # Ask something to Google Gemini in async mode
    async def main() -> None:
        genai.configure(api_key="<GOOGLE_API_KEY>")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = await model.generate_content_async(
            "Write a story about a magic backpack."
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
    import google.generativeai as genai

    # Initialize EcoLogits
    EcoLogits.init()

    # Ask something to Google Gemini in streaming mode
    genai.configure(api_key="<GOOGLE_API_KEY>")
    model = genai.GenerativeModel("gemini-1.5-flash")
    stream = model.generate_content(
        "Write a story about a magic backpack.", 
        stream = True
    )

    # Get cumulative estimated environmental impacts of the inference
    for chunk in stream:
        print(chunk.impacts)
    ```

=== "Async"

    ```python
    import asyncio
    from ecologits import EcoLogits
    import google.generativeai as genai

    # Initialize EcoLogits
    EcoLogits.init()

    # Ask something to Google Gemini in streaming and async mode
    async def main() -> None:
        genai.configure(api_key="<GOOGLE_API_KEY>")
        model = genai.GenerativeModel("gemini-1.5-flash")
        stream = await model.generate_content_async(
            "Write a story about a magic backpack.", 
            stream = True
        )

        # Get cumulative estimated environmental impacts of the inference
        async for chunk in stream:
            print(chunk.impacts)

    asyncio.run(main())
    ```
