user_agent_prompt_v1 = """Hello, I want to search an area in the Amazon rainforest for potential archaeological sites. Given the location coordinates of the area with lat: -9.855331 and long: -67.232337, please try to get a list of potential archaeological sites in the area."""

user_agent_prompt_v2 = """You are assisting in the search for potential archaeological sites in the Amazon rainforest.

Task:
Given the coordinates (latitude: -9.867941, longitude: -67.232337), generate a list of possible archaeological sites within this area.

Please provide:
- The names or descriptions of potential sites.
- Any relevant details or reasoning for their selection.

"""


# z_agent_prompt_v1 = """Hello, I want to find potential archaeological sites in the Amazon rainforest. Please help me check where the following satellite image is a true archaeological site. <img https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.gearthblog.com%2Fblog%2Farchives%2F2010%2F01%2Fdeforestation_of_the_amazon_is_unco.html&psig=AOvVaw322czSQ_po-q39wew4laMq&ust=1748691608156000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCJijgoOOy40DFQAAAAAdAAAAABAX>."""

z_agent_prompt_v2 = """You are an professional archaeologist. You are tasked with finding potential archaeological sites in the Amazon rainforest. Given the location coordinates of the area, please try to call the tool of "get_archaeological_sites" with the provided lat and long to get a list of potential archaeological sites in the area. After get the prediciton, the predicted image will be saved to <img https://lh3.googleusercontent.com/_x55N8AADB6Hl0g6rRwcgwSDVTQRVZRFkrdx7OcxrmOaFC3aHNDQNy84bVtdWHqt4qziR4Tc9nGfXWyqJ3eRZNuaSglaIAfMrfgaB6kWrQAWQ31vbAcpRwqnrHPgAyfqT2sXwbiyBIU=w1280>, try to analyze the image first, partuliar whether we detect the site correctly or not. Then using the location infomation to check it further according to your knowlege about this area"""

z_agent_prompt_v3 = """You are an expert in identifying archaeological sites in the Amazon rainforest using satellite imagery.

Task:
Review the following satellite image and determine if it likely represents a true archaeological site.

Satellite image URL:
https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.gearthblog.com%2Fblog%2Farchives%2F2010%2F01%2Fdeforestation_of_the_amazon_is_unco.html&psig=AOvVaw322czSQ_po-q39wew4laMq&ust=1748691608156000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCJijgoOOy40DFQAAAAAdAAAAABAX

Please provide:
- A clear yes/no answer on whether this is an archaeological site.
- A brief explanation for your decision, referencing visible features in the image.a"""

z_agent_prompt_v4 = """
You are an expert in analyzing satellite images to identify potential archaeological sites in the Amazon rainforest.

Given the following satellite image and its coordinates, please:
1. Determine if the image shows signs of a true archaeological site.
2. Briefly explain your reasoning based on visible features (e.g., geometric shapes, clearings, patterns).
3. If possible, suggest what type of archaeological site it might be (e.g., geoglyph, settlement, road).

Satellite image URL: <INSERT_IMAGE_URL_HERE>
Coordinates: lat: -9.867941, long: -67.232337

Respond in a clear and concise manner.
"""
