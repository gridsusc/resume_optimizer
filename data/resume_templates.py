# Template that wait to put into chromadb to filter
RESUME_TEMPLATES = [

# Art
{
    "input": """
"work": [
  {
    "highlights": [
      "Painted murals for a few local cafes — they gave me free reign on design",
      "Also made digital illustrations for some small online businesses",
      "One client asked for revisions last-minute and I had to totally redo the layout"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Commissioned to design and paint large-scale murals for local businesses, incorporating custom themes and branding",
      "Produced digital illustrations for e-commerce clients, enhancing their visual identity across web and social media",
      "Adapted quickly to client feedback by redesigning a complete layout under a tight deadline, meeting final approval within 24 hours"
    ]
  }
]
"""},

# Game Design
{
    "input": """
"work": [
  {
    "highlights": [
      "Made a small game in Unity for a class project with 3 friends — I did most of the level design",
      "We didn’t use any assets at first but then added some from the Unity store",
      "Had to fix some physics bugs that made the player get stuck"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Led level design for a Unity-based indie game developed in a team of four, emphasizing gameplay pacing and challenge balance",
      "Integrated third-party assets to enhance visual appeal while maintaining design consistency",
      "Diagnosed and resolved critical player movement bugs in Unity physics engine, improving overall user experience"
    ]
  }
]
"""},

# Business/Marketing
{
    "input": """
"work": [
  {
    "highlights": [
      "Helped run some Facebook ads for my uncle’s store",
      "Wrote some posts and tried to make them sound interesting",
      "Tracked how many clicks we got and made changes when things weren’t working"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Developed and managed Facebook ad campaigns for a small business, increasing site traffic by 25%",
      "Created engaging social media content tailored to target demographics, enhancing online brand presence",
      "Monitored campaign analytics and implemented iterative changes to optimize click-through rates and engagement"
    ]
  }
]
"""},

# Engineering (Mechanical)
{
    "input": """
"work": [
  {
    "highlights": [
      "Worked in a lab where we tested how different materials bend under pressure",
      "Used a bunch of measuring tools and had to log data every day",
      "One of our machines broke and I helped take it apart and replace a part"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Conducted mechanical stress tests on various materials, logging detailed performance data for engineering research",
      "Utilized precision instruments such as strain gauges and micrometers to collect accurate test results",
      "Assisted in diagnosing and repairing lab equipment malfunctions, contributing to uninterrupted testing operations"
    ]
  }
]
"""},

# Education
{
    "input": """
"work": [
  {
    "highlights": [
      "Tutored some kids in algebra and geometry after school",
      "Tried to make it fun by turning it into games",
      "One kid really hated math but I helped him pass"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Provided after-school tutoring in algebra and geometry, using gamified methods to enhance student engagement",
      "Developed personalized learning plans based on student needs and learning styles",
      "Helped a struggling student improve math performance, ultimately passing the course with confidence"
    ]
  }
]
"""},

# Psychology
{
    "input": """
"work": [
  {
    "highlights": [
      "Worked at a helpline for a few months during the summer",
      "Answered calls and just talked to people who were feeling stressed",
      "Had to take notes on how they were doing and report to the supervisor"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Volunteered at a mental health support helpline, providing empathetic peer support to individuals in distress",
      "Documented caller concerns and emotional states in compliance with confidentiality protocols",
      "Collaborated with supervisors to ensure appropriate referrals and follow-ups"
    ]
  }
]
"""},

# Journalism
{
    "input": """
"work": [
  {
    "highlights": [
      "Wrote some articles for the school paper — mostly about campus events",
      "Tried to interview people but not everyone wanted to talk",
      "I edited a bunch of stuff for other writers too"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Authored campus news articles for the university newspaper, covering events and student initiatives",
      "Conducted interviews and gathered quotes to enhance reporting accuracy and narrative depth",
      "Edited peer submissions for grammar, clarity, and AP style compliance, improving overall publication quality"
    ]
  }
]
"""},

# Environmental Science
{
    "input": """
"work": [
  {
    "highlights": [
      "Volunteered at a community garden and helped with composting stuff",
      "We tried to track how much waste we diverted from the landfill",
      "Also made a little flyer to tell people how to sort their trash"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Assisted with composting and waste reduction efforts at a local community garden, promoting sustainable practices",
      "Tracked and recorded landfill diversion metrics to evaluate program impact",
      "Designed educational flyers on proper waste sorting to increase public awareness"
    ]
  }
]
"""},

# Law/Pre-Law
{
    "input": """
"work": [
  {
    "highlights": [
      "Interned at a law firm — mostly helped with paperwork",
      "Sometimes looked up case law and tried to find similar cases",
      "Went to a couple court hearings and took notes"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Supported administrative and legal research tasks at a civil litigation firm during summer internship",
      "Conducted case law research to assist attorneys in preparing legal briefs and arguments",
      "Attended court hearings and documented proceedings for internal case tracking"
    ]
  }
]
"""},

# Healthcare/Pre-Med
{
    "input": """
"work": [
  {
    "highlights": [
      "Volunteered at a hospital — brought food to patients and talked to them",
      "Shadowed a couple doctors when they were doing rounds",
      "Watched a surgery once but just stood in the back"
    ]
  }
]
""",
    "output": """
"work": [
  {
    "highlights": [
      "Volunteered in patient services at a local hospital, offering support and comfort to patients during recovery",
      "Shadowed physicians during clinical rounds, gaining exposure to patient care and diagnostic processes",
      "Observed surgical procedures to better understand clinical protocols and sterile environments"
    ]
  }
]
"""},
    # Data science - to be retrieved

    {
        "input": """
"work": [
  {
    "highlights": [
      "Worked on this project at my internship where we had to clean a ton of messy sales data — I wrote a few scripts in Python to fix formatting and missing stuff",
      "I also helped make some visuals in Tableau to show trends to the marketing team",
      "At one point, we had a bug that was breaking everything — I figured out it was due to mismatched date formats"
    ]
  }
]
""",

        "output": """
"work": [
  {
    "highlights": [
      "Developed Python scripts for data cleaning and transformation, reducing manual data wrangling time by 40%",
      "Created interactive Tableau dashboards to visualize sales trends and support marketing decision-making",
      "Identified and resolved critical data pipeline issue related to inconsistent date formats, ensuring report accuracy"
    ]
  }
]
"""},

  {
    "input": """
      "work": [
        {
          "highlights": [
           "I messed around with some Twitter data for a research assistant gig — used tweepy to pull tweets and tried to do some basic sentiment stuff",
            "My advisor wanted to see if we could find anything about public opinion shifts during a product launch",
            "I didn’t know much NLP but figured out how to use NLTK and TextBlob after watching some YouTube videos"
          ]
        }
      ]""",
    "output": """
      "work": [
        {
          "highlights": [
            "Collected and analyzed Twitter data using Tweepy and NLP libraries (NLTK, TextBlob) to study sentiment around product launches",
            "Performed sentiment analysis on thousands of tweets to detect public opinion shifts during a high-profile event",
            "Delivered insights that contributed to a research paper on real-time consumer behavior tracking via social media"
          ]
        }
      ]
    """
  }
]
