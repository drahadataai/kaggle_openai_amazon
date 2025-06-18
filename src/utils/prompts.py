user_agent_prompt_v1 = """Hello, I want to search an area in the Amazon rainforest for potential archaeological sites. Given the location coordinates of the area with lat: -10.48284 and long: -67.070378, please try to get a list of potential archaeological sites in the area."""




z_agent_prompt_v1 = """Hello, I want to find potential archaeological sites in the Amazon rainforest. Please help me check where the following satellite image is a true archaeological site. <img https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.gearthblog.com%2Fblog%2Farchives%2F2010%2F01%2Fdeforestation_of_the_amazon_is_unco.html&psig=AOvVaw322czSQ_po-q39wew4laMq&ust=1748691608156000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCJijgoOOy40DFQAAAAAdAAAAABAX>."""

z_agent_prompt_v2 = """You are an professional archaeologist. You are tasked with finding potential archaeological sites in the Amazon rainforest. Given the location coordinates of the area with lat: -10.48284 and long: -67.070378, please try to call the tool of "get_archaeological_sites" to get a list of potential archaeological sites in the area. """