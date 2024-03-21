from huggingface_hub import InferenceClient
client = InferenceClient()

# image = client.text_to_image("An astronaut riding a horse on the moon with colors")
# image.save("astronaut.png")

res = client.text_generation("Today is ", max_new_tokens=12, details=True)
print(res)
