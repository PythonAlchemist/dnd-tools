from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os


# os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
# os.environ["OPENAI_MODEL_NAME"] = "crewai-llama3"  # Adjust based on available model
os.environ["OPENAI_API_KEY"] = "NA"


llm = ChatOpenAI(model="crewai-llama3", base_url="http://localhost:11434/v1")

dungeon_master = Agent(
    role="Dungeon Master",
    goal="""To provide a fun and engaging experience for the players. This includes narration of locations and events, as well as deleating to other agents to provide information or resolve actions.""",
    backstory="""You are a digital clone of Mathew Mercer, the famous Dungeon Master of Critical Role. You have been tasked with running a game for a group of players in a virtual world.""",
    # You have access to a vast library of information and the ability to create new content on the fly. You are a master of improvisation and storytelling.""",
    verbose=True,
    memory=True,
    llm=llm,
)
inn_keeper = Agent(
    role="Inn Keeper",
    goal="""To provide a place for the players to rest and recover. This includes renting rooms, serving food and drink, and providing information about the local area.""",
    backstory="""You are the owner of the local inn and tavern. You are a friendly and welcoming host who enjoys meeting new people and hearing their stories. You have a wealth of knowledge about the local area and can provide information about quests and points of interest.""",
    verbose=True,
    llm=llm,
)
blacksmith = Agent(
    role="Blacksmith",
    goal="""To provide the players with weapons, armor, and other equipment. This includes crafting new items, repairing damaged gear, and providing advice on the best gear for their needs.""",
    backstory="""You are the local blacksmith, skilled in the art of metalworking.""",
    # You take pride in your work and are always looking for new challenges.\
    # You have a deep knowledge of weapons and armor and can provide the players with the best gear for their needs.""",
    verbose=True,
    llm=llm,
)
regular = Agent(
    role="Townsperson",
    goal="""To live a peaceful life in the town. This includes going about your daily routine, interacting with other townspeople, and avoiding danger whenever possible.""",
    backstory="""You are a regular townsperson, going about your daily life in the town. You have friends and family, a job, and a place to live. You are not a hero or an adventurer, but you are an important part of the community. And you are a gossip.""",
    verbose=True,
    llm=llm,
)

run = Task(
    description="""The player adventurer has just arrived in the town of Greenhaven and just entered the Golden Griffin Inn.""",
    # You should provide a description of the inn, including the layout, the patrons, and the atmosphere. \
    # Engage with the player adventurer and respond to their actions and questions. \
    # You can delegate to the other agents to provide information or resolve actions as needed. Have fun!""",
    expected_output="A back and forth conversation between the character player and any agents that are delegated to.",
    agent=dungeon_master,
    # human_input=True,
)

crew = Crew(
    agents=[dungeon_master, inn_keeper, blacksmith, regular],
    tasks=[run],
    verbose=2,
    memory=True,
)

result = crew.kickoff()

print("#############################")
print(result)
