# Few-shot examples to help the model understand how to convert natural language to JSON
RESUME_EXAMPLES = [
 {
   "input": {
     """ "work": [
       {
         "highlights": [
           "Worked on this project at my internship where we had to clean a ton of messy sales data — I wrote a few scripts in Python to fix formatting and missing stuff",
           "I also helped make some visuals in Tableau to show trends to the marketing team",
           "At one point, we had a bug that was breaking everything — I figured out it was due to mismatched date formats"
         ]
       }
     ]
   }""",
   "output": {
     """ "work": [
       {
         "highlights": [
           "Developed Python scripts for data cleaning and transformation, reducing manual data wrangling time by 40%",
           "Created interactive Tableau dashboards to visualize sales trends and support marketing decision-making",
           "Identified and resolved critical data pipeline issue related to inconsistent date formats, ensuring report accuracy"
         ]
       }
     ]
   }"""
 }
#  {
#    "input": {
#      "work": [
#        {
#          "highlights": [
#            "I messed around with some Twitter data for a research assistant gig — used tweepy to pull tweets and tried to do some basic sentiment stuff",
#            "My advisor wanted to see if we could find anything about public opinion shifts during a product launch",
#            "I didn’t know much NLP but figured out how to use NLTK and TextBlob after watching some YouTube videos"
#          ]
#        }
#      ]
#    },
#    "output": {
#      "work": [
#        {
#          "highlights": [
#            "Collected and analyzed Twitter data using Tweepy and NLP libraries (NLTK, TextBlob) to study sentiment around product launches",
#            "Performed sentiment analysis on thousands of tweets to detect public opinion shifts during a high-profile event",
#            "Delivered insights that contributed to a research paper on real-time consumer behavior tracking via social media"
#          ]
#        }
#      ]
#    }
#  }
 ]