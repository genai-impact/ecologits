from genai_impact.gen_ai_impacts import GenAIImpacts

client = GenAIImpacts()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...]  # Your messages here
)

impacts = client.get_impacts(response)
print(impacts)
# Outputs: Impacts(energy=42, energy_unit='kWh', gwp=15, gwp_unit='kgCO2eq')
