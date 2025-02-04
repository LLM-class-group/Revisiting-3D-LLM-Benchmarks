# Where
prompt_where_bev = """You are a scene analysis assistant. You will be provided with a bird's-eye view of a real indoor scene. I will ask you a question about where some object is. Please answer based on its relative position in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Preposition] ([Adjective]) [Object]

Examples:
Question: Where is the beige wooden working table placed?
Answer: right of tall cabinet
Question: Where is the silver bread toaster placed?
Answer: countertop
Question: Where is the brown wooden cabinet located?
Answer: above kitchen counter tops
Question: Where is the coffee table kept?
Answer: in middle of seating area
Question: Where is the brown door located?
Answer: between 2 tall cabinets
Question: Where is the triangular shape table located?
Answer: in front of radiator
Question: Where is the tv stand sitting?
Answer: under 2 windows
Question: Where is the trash can located?
Answer: under white shelf
Question: Where is the tv mounted?
Answer: on white wall
Question: Where is the black office chair located on the table?
Answer: at end of table in middle of room
---
Your Question is:
"""

prompt_where_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene, and ask you about an item's location. Please describe its relative position in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Preposition] ([Adjective]) [Object]

Examples:
Question: Where is the beige wooden working table placed?
Answer: right of tall cabinet
Question: Where is the silver bread toaster placed?
Answer: countertop
Question: Where is the brown wooden cabinet located?
Answer: above kitchen counter tops
Question: Where is the coffee table kept?
Answer: in middle of seating area
Question: Where is the brown door located?
Answer: between 2 tall cabinets
Question: Where is the triangular shape table located?
Answer: in front of radiator
Question: Where is the tv stand sitting?
Answer: under 2 windows
Question: Where is the trash can located?
Answer: under white shelf
Question: Where is the tv mounted?
Answer: on white wall
Question: Where is the black office chair located on the table?
Answer: at end of table in middle of room
---
Your Question is:
"""

prompt_where_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and ask you about an item's location. Please describe its relative position in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Preposition] ([Adjective]) [Object]

Examples:
Question: Where is the beige wooden working table placed?
Answer: right of tall cabinet
Question: Where is the silver bread toaster placed?
Answer: countertop
Question: Where is the brown wooden cabinet located?
Answer: above kitchen counter tops
Question: Where is the coffee table kept?
Answer: in middle of seating area
Question: Where is the brown door located?
Answer: between 2 tall cabinets
Question: Where is the triangular shape table located?
Answer: in front of radiator
Question: Where is the tv stand sitting?
Answer: under 2 windows
Question: Where is the trash can located?
Answer: under white shelf
Question: Where is the tv mounted?
Answer: on white wall
Question: Where is the black office chair located on the table?
Answer: at end of table in middle of room
---
Your Question is:
"""

prompt_where_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. You'll be asked about an item's location. Please describe its relative position in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Preposition] ([Adjective]) [Object]

Examples:
Question: Where is the beige wooden working table placed?
Answer: right of tall cabinet
Question: Where is the silver bread toaster placed?
Answer: countertop
Question: Where is the brown wooden cabinet located?
Answer: above kitchen counter tops
Question: Where is the coffee table kept?
Answer: in middle of seating area
Question: Where is the brown door located?
Answer: between 2 tall cabinets
Question: Where is the triangular shape table located?
Answer: in front of radiator
Question: Where is the tv stand sitting?
Answer: under 2 windows
Question: Where is the trash can located?
Answer: under white shelf
Question: Where is the tv mounted?
Answer: on white wall
Question: Where is the black office chair located on the table?
Answer: at end of table in middle of room
---
Your Question is:
"""


# Number
prompt_number_bev = """This is a bird's-eye view of a real indoor scene. I will ask you about the number of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Number] ([Adjective] [Object])

Examples:
Question: How many trash cans can be seen on your right when you enter?
Answer: 2 small white trash cans
Question: How many coffee tables does the brown armchair face?
Answer: 2
Question: How many individual shelves does the shelf have?
Answer: 3
Question: How many trash cans are in a row?
Answer: 4 trash cans
Question: How many round white chairs are in front of the breakfast bar?
Answer: 3 white chairs
Question: How many black chairs surrounds the brown table?
Answer: 4 black chairs
Question: How many chairs does the breakfast bar have?
Answer: 5
---
Your Question is:
"""

prompt_number_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will ask you about the number of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Number] ([Adjective] [Object])

Examples:
Question: How many trash cans can be seen on your right when you enter?
Answer: 2 small white trash cans
Question: How many coffee tables does the brown armchair face?
Answer: 2
Question: How many individual shelves does the shelf have?
Answer: 3
Question: How many trash cans are in a row?
Answer: 4 trash cans
Question: How many round white chairs are in front of the breakfast bar?
Answer: 3 white chairs
Question: How many black chairs surrounds the brown table?
Answer: 4 black chairs
Question: How many chairs does the breakfast bar have?
Answer: 5
---
Your Question is:
"""

prompt_number_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene. I will ask you about the number of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Number] ([Adjective] [Object])

Examples:
Question: How many trash cans can be seen on your right when you enter?
Answer: 2 small white trash cans
Question: How many coffee tables does the brown armchair face?
Answer: 2
Question: How many individual shelves does the shelf have?
Answer: 3
Question: How many trash cans are in a row?
Answer: 4 trash cans
Question: How many round white chairs are in front of the breakfast bar?
Answer: 3 white chairs
Question: How many black chairs surrounds the brown table?
Answer: 4 black chairs
Question: How many chairs does the breakfast bar have?
Answer: 5
---
Your Question is:
"""

prompt_number_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I will ask you about the number of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Number] ([Adjective] [Object])

Examples:
Question: How many trash cans can be seen on your right when you enter?
Answer: 2 small white trash cans
Question: How many coffee tables does the brown armchair face?
Answer: 2
Question: How many individual shelves does the shelf have?
Answer: 3
Question: How many trash cans are in a row?
Answer: 4 trash cans
Question: How many round white chairs are in front of the breakfast bar?
Answer: 3 white chairs
Question: How many black chairs surrounds the brown table?
Answer: 4 black chairs
Question: How many chairs does the breakfast bar have?
Answer: 5
---
Your Question is:
"""


# Color
prompt_color_bev = """This is a bird's-eye view of a real indoor scene. I will ask you about the color of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Color] ([Object])

Examples:
Question: What color is the chair on the right of the white table?
Answer: black
Question: What color is the table at the center of the room?
Answer: brown table
Question: What color wall is on the left of the monitor?
Answer: white
Question: What is the color of the table?
Answer: brown
Question: What color is the wooden door?
Answer: Dark brown
Question: What color is the chair on the left side?
Answer: blue
Question: What color is the desk on the right side?
Answer: brown desk
---
Your Question is:
"""

prompt_color_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will ask you about the color of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Color] ([Object])

Examples:
Question: What color is the chair on the right of the white table?
Answer: black
Question: What color is the table at the center of the room?
Answer: brown table
Question: What color wall is on the left of the monitor?
Answer: white
Question: What is the color of the table?
Answer: brown
Question: What color is the wooden door?
Answer: Dark brown
Question: What color is the chair on the left side?
Answer: blue
Question: What color is the desk on the right side?
Answer: brown desk
---
Your Question is:
"""

prompt_color_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene. I will ask you about the color of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Color] ([Object])

Examples:
Question: What color is the chair on the right of the white table?
Answer: black
Question: What color is the table at the center of the room?
Answer: brown table
Question: What color wall is on the left of the monitor?
Answer: white
Question: What is the color of the table?
Answer: brown
Question: What color is the wooden door?
Answer: Dark brown
Question: What color is the chair on the left side?
Answer: blue
Question: What color is the desk on the right side?
Answer: brown desk
---
Your Question is:
"""

prompt_color_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I will ask you about the color of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Color] ([Object])

Examples:
Question: What color is the chair on the right of the white table?
Answer: black
Question: What color is the table at the center of the room?
Answer: brown table
Question: What color wall is on the left of the monitor?
Answer: white
Question: What is the color of the table?
Answer: brown
Question: What color is the wooden door?
Answer: Dark brown
Question: What color is the chair on the left side?
Answer: blue
Question: What color is the desk on the right side?
Answer: brown desk
---
Your Question is:
"""


# Shape
prompt_shape_bev = """This is a bird's-eye view of a real indoor scene. I will ask you about the shape of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Shape] ([Object])

Examples:
Question: What shaped plain table is kept near the arm chair?
Answer: triangular
Question: What shape is the mirror to the right of the tv?
Answer: circular
Question: What shape is the table in the corner of the room?
Answer: round
Question: What shape is the brown desk?
Answer: rectangle desk
Question: What shape of striped ottoman is on the floor next to the bed?
Answer: rectangular
Question: What shape is the desk?
Answer: l shaped desk
---
Your Question is:
"""

prompt_shape_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will ask you about the shape of some objects in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Shape] ([Object])

Examples:
Question: What shaped plain table is kept near the arm chair?
Answer: triangular
Question: What shape is the mirror to the right of the tv?
Answer: circular
Question: What shape is the table in the corner of the room?
Answer: round
Question: What shape is the brown desk?
Answer: rectangle desk
Question: What shape of striped ottoman is on the floor next to the bed?
Answer: rectangular
Question: What shape is the desk?
Answer: l shaped desk
---
Your Question is:
"""

prompt_shape_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and ask you about an item's shape in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Shape] ([Object])

Examples:
Question: What shaped plain table is kept near the arm chair?
Answer: triangular
Question: What shape is the mirror to the right of the tv?
Answer: circular
Question: What shape is the table in the corner of the room?
Answer: round
Question: What shape is the brown desk?
Answer: rectangle desk
Question: What shape of striped ottoman is on the floor next to the bed?
Answer: rectangular
Question: What shape is the desk?
Answer: l shaped desk
---
Your Question is:
"""

prompt_shape_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I will ask you about an item's shape in the scene. 

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Shape] ([Object])

Examples:
Question: What shaped plain table is kept near the arm chair?
Answer: triangular
Question: What shape is the mirror to the right of the tv?
Answer: circular
Question: What shape is the table in the corner of the room?
Answer: round
Question: What shape is the brown desk?
Answer: rectangle desk
Question: What shape of striped ottoman is on the floor next to the bed?
Answer: rectangular
Question: What shape is the desk?
Answer: l shaped desk
---
Your Question is:
"""


# Type
prompt_type_bev = """You are a scene analysis assistant. This is a bird's-eye view of a real indoor scene. I will describe an object in the scene, please tell me what type the object is.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Type] ([Object])

Examples:
Question: What type of wood is the coffee table?
Answer: brown coffee table
Question: What type of coffee table is in the room?
Answer: square wood coffee table
Question: What type of couch is placed next to the light wood tea table?
Answer: loveseat
Question: What type of bag is on the floor?
Answer: green
Question: What type of cabinet is next to the bin?
Answer: single lower kitchen cabinet
Question: refrigerator
Answer: What type of cooler is next to a cabinet?
Question: What type of kitchen cabinets are under a black counter top?
Answer: wooden lower cabinets
Question: What type of kitchen cabinets are these?
Answer: brown wooden
---
Your Question is:
"""

prompt_type_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will describe an object in the scene, please tell me what type the object is.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Type] ([Object])

Examples:
Question: What type of wood is the coffee table?
Answer: brown coffee table
Question: What type of coffee table is in the room?
Answer: square wood coffee table
Question: What type of couch is placed next to the light wood tea table?
Answer: loveseat
Question: What type of bag is on the floor?
Answer: green
Question: What type of cabinet is next to the bin?
Answer: single lower kitchen cabinet
Question: refrigerator
Answer: What type of cooler is next to a cabinet?
Question: What type of kitchen cabinets are under a black counter top?
Answer: wooden lower cabinets
Question: What type of kitchen cabinets are these?
Answer: brown wooden
---
Your Question is:
"""

prompt_type_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene. I will describe an object in the scene, please tell me what type the object is.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Type] ([Object])

Examples:
Question: What type of wood is the coffee table?
Answer: brown coffee table
Question: What type of coffee table is in the room?
Answer: square wood coffee table
Question: What type of couch is placed next to the light wood tea table?
Answer: loveseat
Question: What type of bag is on the floor?
Answer: green
Question: What type of cabinet is next to the bin?
Answer: single lower kitchen cabinet
Question: refrigerator
Answer: What type of cooler is next to a cabinet?
Question: What type of kitchen cabinets are under a black counter top?
Answer: wooden lower cabinets
Question: What type of kitchen cabinets are these?
Answer: brown wooden
---
Your Question is:
"""

prompt_type_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I will describe an object in the scene, please tell me what type the object is.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Type] ([Object])

Examples:
Question: What type of wood is the coffee table?
Answer: brown coffee table
Question: What type of coffee table is in the room?
Answer: square wood coffee table
Question: What type of couch is placed next to the light wood tea table?
Answer: loveseat
Question: What type of bag is on the floor?
Answer: green
Question: What type of cabinet is next to the bin?
Answer: single lower kitchen cabinet
Question: refrigerator
Answer: What type of cooler is next to a cabinet?
Question: What type of kitchen cabinets are under a black counter top?
Answer: wooden lower cabinets
Question: What type of kitchen cabinets are these?
Answer: brown wooden
---
Your Question is:
"""


# Kind
prompt_kind_bev = """This is a bird's-eye view of a real indoor scene. I will ask you a question about the kind of some objects.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective]/[Material] ([Object])

Examples:
Question: What kind of dispenser is on the wall next to the sink?
Answer: soap dispenser
Question: What kind of cabinets are above a microwave?
Answer: wooden kitchen cabinets
Question: What kind of table is in front of a window?
Answer: small white round
Question: What kind of chair is to the left of the table?
Answer: grey and blue sofa chair
Question: What kind of base does the table have?
Answer: metal
Question: What kind of cabinets are in the kitchen?
Answer: wooden
Question: What kind of shelf is next to the door?
Answer: 3 layered wooden shelf
Question: What kind of cushion is on top of a bed?
Answer: blue rectangular pillow
Question: What kind of shelf is in the bed?
Answer: wood
Question: What kind of cabinet on the wall?
Answer: dark brown cabinet
---
Your Question is:
"""

prompt_kind_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will ask you a question about the kind of some objects.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective]/[Material] ([Object])

Examples:
Question: What kind of dispenser is on the wall next to the sink?
Answer: soap dispenser
Question: What kind of cabinets are above a microwave?
Answer: wooden kitchen cabinets
Question: What kind of table is in front of a window?
Answer: small white round
Question: What kind of chair is to the left of the table?
Answer: grey and blue sofa chair
Question: What kind of base does the table have?
Answer: metal
Question: What kind of cabinets are in the kitchen?
Answer: wooden
Question: What kind of shelf is next to the door?
Answer: 3 layered wooden shelf
Question: What kind of cushion is on top of a bed?
Answer: blue rectangular pillow
Question: What kind of shelf is in the bed?
Answer: wood
Question: What kind of cabinet on the wall?
Answer: dark brown cabinet
---
Your Question is:
"""

prompt_kind_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and ask you about the kind of some objects in the scene.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective]/[Material] ([Object])

Example:
Question: What kind of dispenser is on the wall next to the sink?
Answer: soap dispenser
Question: What kind of cabinets are above a microwave?
Answer: wooden kitchen cabinets
Question: What kind of table is in front of a window?
Answer: small white round
Question: What kind of chair is to the left of the table?
Answer: grey and blue sofa chair
Question: What kind of base does the table have?
Answer: metal
Question: What kind of cabinets are in the kitchen?
Answer: wooden
Question: What kind of shelf is next to the door?
Answer: 3 layered wooden shelf
Question: What kind of cushion is on top of a bed?
Answer: blue rectangular pillow
Question: What kind of shelf is in the bed?
Answer: wood
Question: What kind of cabinet on the wall?
Answer: dark brown cabinet
---
Your Question is:
"""

prompt_kind_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I'll ask you about the kind of some objects in the scene.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective]/[Material] ([Object])

Example:
Question: What kind of dispenser is on the wall next to the sink?
Answer: soap dispenser
Question: What kind of cabinets are above a microwave?
Answer: wooden kitchen cabinets
Question: What kind of table is in front of a window?
Answer: small white round
Question: What kind of chair is to the left of the table?
Answer: grey and blue sofa chair
Question: What kind of base does the table have?
Answer: metal
Question: What kind of cabinets are in the kitchen?
Answer: wooden
Question: What kind of shelf is next to the door?
Answer: 3 layered wooden shelf
Question: What kind of cushion is on top of a bed?
Answer: blue rectangular pillow
Question: What kind of shelf is in the bed?
Answer: wood
Question: What kind of cabinet on the wall?
Answer: dark brown cabinet
---
Your Question is:
"""


# What
prompt_what_bev = """You are a scene analysis assistant. This is a bird's-eye view of a real indoor scene. I will describe the location of an item in the scene, please tell me what this item is.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective] [Object]

Example:
Question: What is in front of the shower?
Answer: shower curtain
Question: What is on the wall close to the toilet?
Answer: picture
Question: What is next to a trash can?
Answer: paper towel dispenser
Question: What is next to the oval white sink?
Answer: bathroom vanity
Question: What is on the chair facing the table?
Answer: red backpack
Question: What is mounted on the wall behind the table with a single chair?
Answer: large rectangular whiteboard
Question: What is the last chair on the left?
Answer: grey chair with folding seat
Question: What is the object behind a white toilet?
Answer: shelf
Question: What is the object that sits between the toilet and the sink?
Answer: short round trash can
Question: What is next to the ball?
Answer: standing rack of smaller balls
---
Your Question is:
"""

prompt_what_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will describe the location of an item in the scene, please tell me what this item is.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective] [Object]

Example:
Question: What is in front of the shower?
Answer: shower curtain
Question: What is on the wall close to the toilet?
Answer: picture
Question: What is next to a trash can?
Answer: paper towel dispenser
Question: What is next to the oval white sink?
Answer: bathroom vanity
Question: What is on the chair facing the table?
Answer: red backpack
Question: What is mounted on the wall behind the table with a single chair?
Answer: large rectangular whiteboard
Question: What is the last chair on the left?
Answer: grey chair with folding seat
Question: What is the object behind a white toilet?
Answer: shelf
Question: What is the object that sits between the toilet and the sink?
Answer: short round trash can
Question: What is next to the ball?
Answer: standing rack of smaller balls
---
Your Question is:
"""

prompt_what_multiview = """You are a scene analysis assistant. You will be provided with multiple stitched photos showing different angles of an indoor scene. I will describe the location of an item in the scene, please tell me what this item is.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective] [Object]

Examples:
Question: What is in front of the shower?
Answer: shower curtain
Question: What is on the wall close to the toilet?
Answer: picture
Question: What is next to a trash can?
Answer: paper towel dispenser
Question: What is next to the oval white sink?
Answer: bathroom vanity
Question: What is on the chair facing the table?
Answer: red backpack
Question: What is mounted on the wall behind the table with a single chair?
Answer: large rectangular whiteboard
Question: What is the last chair on the left?
Answer: grey chair with folding seat
Question: What is the object behind a white toilet?
Answer: shelf
Question: What is the object that sits between the toilet and the sink?
Answer: short round trash can
Question: What is next to the ball?
Answer: standing rack of smaller balls
---
Your Question is:
"""

prompt_what_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I will describe the location of an item in the scene, please tell me what this item is.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Format for reference: [Objective] [Object]

Examples:
Question: What is in front of the shower?
Answer: shower curtain
Question: What is on the wall close to the toilet?
Answer: picture
Question: What is next to a trash can?
Answer: paper towel dispenser
Question: What is next to the oval white sink?
Answer: bathroom vanity
Question: What is on the chair facing the table?
Answer: red backpack
Question: What is mounted on the wall behind the table with a single chair?
Answer: large rectangular whiteboard
Question: What is the last chair on the left?
Answer: grey chair with folding seat
Question: What is the object behind a white toilet?
Answer: shelf
Question: What is the object that sits between the toilet and the sink?
Answer: short round trash can
Question: What is next to the ball?
Answer: standing rack of smaller balls
---
Your Question is:
"""


# Other
prompt_other_bev = """You are a scene analysis assistant. This is a bird's-eye view of a real indoor scene. I will ask a question about an object in the scene, please answer the question based on the view.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Examples:
Question: On which side of the window is the gray trash bin seated?
Answer: on right side of window
Question: The trash can is to the left of which can?
Answer: black trash can
Question: In which row is the chair in the last row from left?
Answer: middle
Question: On which side of the first row of chairs is a chair on?
Answer: right
Question: The chair is facing which direction?
Answer: facing in direction toward tables
Question: On which side of the room is the square desk located?
Answer: left side of blackboard
Question: On which side of the table is the middle chair located?
Answer: on left and right side of 2 tables
Question: On which side of the desk is the shelf located?
Answer: far middle side of desk
---
Your Question is:
"""

prompt_other_single_view = """You are a scene analysis assistant. I will provide a photo showing an indoor scene. I will ask a question about an object in the scene, please answer the question based on the view.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Examples:
Question: On which side of the window is the gray trash bin seated?
Answer: on right side of window
Question: The trash can is to the left of which can?
Answer: black trash can
Question: In which row is the chair in the last row from left?
Answer: middle
Question: On which side of the first row of chairs is a chair on?
Answer: right
Question: The chair is facing which direction?
Answer: facing in direction toward tables
Question: On which side of the room is the square desk located?
Answer: left side of blackboard
Question: On which side of the table is the middle chair located?
Answer: on left and right side of 2 tables
Question: On which side of the desk is the shelf located?
Answer: far middle side of desk
---
Your Question is:
"""

prompt_other_multiview = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene. I will ask a question about an object in the scene, please answer the question based on the view.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Examples:
Question: On which side of the window is the gray trash bin seated?
Answer: on right side of window
Question: The trash can is to the left of which can?
Answer: black trash can
Question: In which row is the chair in the last row from left?
Answer: middle
Question: On which side of the first row of chairs is a chair on?
Answer: right
Question: The chair is facing which direction?
Answer: facing in direction toward tables
Question: On which side of the room is the square desk located?
Answer: left side of blackboard
Question: On which side of the table is the middle chair located?
Answer: on left and right side of 2 tables
Question: On which side of the desk is the shelf located?
Answer: far middle side of desk
---
Your Question is:
"""

prompt_other_multiview_bev = """You are a scene analysis assistant. I will provide multiple stitched photos showing different angles of an indoor scene, and the one in the upper left corner is a bird's-eye view. I will ask a question about an object in the scene, please answer the question based on the view.

The rendered results may appear incomplete or have some occlusions - this is **does not mean the house is damaged**! Please carefully observe the views from different angles, think about and examine the room layout, then answer the questions.

Note: Give a consice response. Your answer could be a word or a phrase, but **NOT a sentence**!

Examples:
Question: On which side of the window is the gray trash bin seated?
Answer: on right side of window
Question: The trash can is to the left of which can?
Answer: black trash can
Question: In which row is the chair in the last row from left?
Answer: middle
Question: On which side of the first row of chairs is a chair on?
Answer: right
Question: The chair is facing which direction?
Answer: facing in direction toward tables
Question: On which side of the room is the square desk located?
Answer: left side of blackboard
Question: On which side of the table is the middle chair located?
Answer: on left and right side of 2 tables
Question: On which side of the desk is the shelf located?
Answer: far middle side of desk
---
Your Question is:
"""
