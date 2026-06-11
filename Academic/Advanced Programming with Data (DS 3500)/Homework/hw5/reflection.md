**What does your animation show about the storm's impact? Describe specifically what you see around February 23–24 in both animations. Which stops or line segments were most affected? How quickly did service recover?**

Maverick & Ava: Our animations reflected very little change in the typical function of the Green Line. It seems to already function sporadically and travel at a slower rate than its scheduled time. Some of the stops which were most affected can be seen in animation b. These include Ball Sq, Brico, South St, St. Mary's St, East Somerville, and Chiswick. These stops were not significanly impacted, though they were effected more than other stations, so they recovered quickly - mostly over a day or two.
Animation a shows no almost no notable difference in the green line service times. There is also little change in the difference between Actual vers Expected time. More of a difference can be seen earlier in the month.

**Data limitations. The scheduled_travel_time field has missing values on storm days because the MBTA ran non-standard service that didn't match the planned schedule. How did you handle this in your cleaning step, and how does it affect what your Animation A shows?**

Maverick: We already marked "sheduled_travel_time" as a required column, so all null valued rows were dropped earlier in the cleaning process. So, when the instructions for the cleaning layer were outlined, we had already dropped the null values from this column. The column had 33,300 rows containing nulls before cleaning, 2211 of which were from 02/22 to 02/24. So, I don't believe that dropping such values significantly impacted the animation for storm days more than the other days in February.
  
**Layered architecture. Describe one specific moment during development where the layer separation made something easier — for example, debugging the model without touching the animation, or swapping a computed field without changing either animation. If you hit a moment where the separation felt annoying rather than helpful, describe that too.**

Ava: A specific moment during development where the layer separation made something easier was when there was an issue with the values used and what was imported from the model layer. Because there was a seperate field for animation_a, animation_b and model and animation_b worked. I could see that the bug was in the animation_a file and leave the other two untouched.
Maverick:  Similar to what Ava said, the layer separation made it easier to create animations, as the model layer configured all values necessary for the animation's input. So, the functions from the model layer only needed to be imported and defined.

**AI Usage statement. If you decided to use generative AI for this assignment, in less than 10 sentences, list your AI tools, the level of success you had with them, and if, where, and how you had to step in**

Ava: AI was used to fine tune animation_b as it had many viewing errors. This includes finding a good size, picking more contrasting colors and margin/tick sizing. 
