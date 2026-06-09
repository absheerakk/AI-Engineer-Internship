import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("fifty_docs")

documents = [
    # Technology
    "Python is widely used for data science and machine learning.",
    "JavaScript is the primary language of web development.",
    "Rust is known for memory safety and performance.",
    "Docker containers make software deployment consistent.",
    "Git is the standard tool for version control.",
    "APIs allow different software systems to communicate.",
    "Cloud computing provides on-demand computing resources.",
    "Open source software is freely available to modify and share.",
    "Databases store and organise structured data.",
    "Machine learning models improve with more training data.",
    # Science
    "The speed of light is approximately 300,000 km per second.",
    "DNA carries genetic information in living organisms.",
    "Photosynthesis converts sunlight into energy for plants.",
    "Black holes have gravitational pull so strong light cannot escape.",
    "The periodic table organises all known chemical elements.",
    "Quantum mechanics describes physics at the subatomic level.",
    "Climate change is driven largely by greenhouse gas emissions.",
    "The human brain contains roughly 86 billion neurons.",
    "Vaccines train the immune system to fight specific diseases.",
    "Evolution occurs through natural selection over generations.",
    # History
    "The Second World War ended in 1945.",
    "Pakistan gained independence on 14 August 1947.",
    "The invention of the printing press changed the spread of knowledge.",
    "The Industrial Revolution transformed manufacturing in the 18th century.",
    "The moon landing took place in July 1969.",
    "The Roman Empire lasted for over a thousand years.",
    "The Silk Road was an ancient trade route connecting East and West.",
    "The French Revolution began in 1789.",
    "Genghis Khan founded the Mongol Empire in the 13th century.",
    "The Berlin Wall fell in 1989.",
    # Health
    "Regular exercise reduces the risk of cardiovascular disease.",
    "Sleep deprivation impairs memory and cognitive function.",
    "A balanced diet includes proteins, carbohydrates, and healthy fats.",
    "Stress can have significant negative effects on physical health.",
    "Drinking enough water is essential for bodily functions.",
    "Mental health is as important as physical health.",
    "Smoking is a leading cause of preventable death worldwide.",
    "Meditation has been shown to reduce anxiety and improve focus.",
    "Vitamin D deficiency is common in regions with low sunlight.",
    "Hand washing is one of the most effective ways to prevent illness.",
    # Business
    "A startup is a young company trying to solve a problem at scale.",
    "Cash flow is often more important than profit for small businesses.",
    "Marketing involves understanding and reaching your target audience.",
    "Supply chain disruptions can affect product availability globally.",
    "Remote work has become common since the COVID-19 pandemic.",
    "Venture capital funds early-stage companies in exchange for equity.",
    "Customer retention is cheaper than acquiring new customers.",
    "A business model describes how a company creates and captures value.",
    "Data-driven decisions tend to outperform decisions based on intuition.",
    "Branding is how a company presents itself to the world."
]

embeddings = model.encode(documents).tolist()
ids = [f"doc_{i}" for i in range(len(documents))]
collection.add(documents=documents, embeddings=embeddings, ids=ids)

print(f"Stored {collection.count()} documents.\n")

queries = [
    "programming languages",
    "human body and health",
    "ancient history",
    "running a company",
    "space and physics",
]

for query in queries:
    results = collection.query(
        query_embeddings=model.encode([query]).tolist(),
        n_results=3,
    )
    print(f"Query: '{query}'")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        print(f"  {1 - distance:.3f}  {doc}")
    print()
