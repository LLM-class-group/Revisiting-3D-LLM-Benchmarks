prompt = """
What object does this rendered point cloud represent? Give a **consice, short** description. 

Remember: 1. **Start with 'A' or 'An'**
          2. **Though this point cloud rendering might appear spongy or textured, the actual object has a smooth surface. Imagine the object in real-life and tell what it actually is.**
          3. **It might be a model of big object, like a building, village, or small object, like a cup, a chair.**
          4. **Don't give vague descriptions of what it looks like, instead specify exactly what it is in real life.**
            Instead of saying "cylindrical container", say "waste bin".
            Instead of saying "sharp black and white object", say "knife".

examples: 
- A vintage brass trumpet with polished valves and an engraved bell.
- A black leather briefcase.
- A green glass wine bottle with golden labels on the neck of the bottle.
- A vase with a floral pattern and geometric designs, featuring a narrow neck.
- A street lamp mounted on a concrete post.
- A pair of headphones with black plastic frame and blue ear cushions.
- A bronze wall clock.
- A light grey guitar and case.
- A vibrant rubber toy car shaped like a banana.
- A modern white refrigerator in the shape of a rectangle with a handle and shelves.
- One green vase and one red vase.
"""