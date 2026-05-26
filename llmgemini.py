import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

# --- Step 1: Configure the Gemini API ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC2O-_ViAmC-eUqpGe7VshJLKDtzt21sD0")  # Use env variable or default
genai.configure(api_key=GOOGLE_API_KEY)

# --- Step 2: Load the IPC Sections from JSON ---
json_path = r"C:\Users\raji\Downloads\garbage_ml\ipc.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"JSON file '{json_path}' not found.")

with open(json_path, "r", encoding="utf-8") as file:
    ipc_data = json.load(file)

# Convert JSON data to DataFrame
df_ipc = pd.DataFrame(ipc_data)

# Ensure required columns exist
required_columns = {"Section", "section_title", "section_desc"}
if not required_columns.issubset(df_ipc.columns):
    raise ValueError(f"JSON is missing required fields: {required_columns - set(df_ipc.columns)}")

df_ipc.fillna("", inplace=True)  # Handle missing values


# --- Step 3: Define a function to generate an abstract using Gemini 1.5 Flash ---
def generate_abstract(query):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Summarize this legal case accordingly in legal terms : {query}"
        response = model.generate_content(prompt)
        return getattr(response, "text", "").strip()
    except Exception as e:
        return f"Error generating abstract: {e}"


# --- Step 4: Define a function to match the abstract with the most relevant IPC section ---
def match_ipc_sections(abstract, top_n=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    ipc_vectors = vectorizer.fit_transform(df_ipc["section_desc"])
    query_vector = vectorizer.transform([abstract])
    similarities = cosine_similarity(query_vector, ipc_vectors).flatten()

    # Get top N most relevant IPC sections
    top_indices = similarities.argsort()[-top_n:][::-1]
    top_matches = df_ipc.iloc[top_indices].copy()
    top_matches["similarity_score"] = similarities[top_indices]

    return top_matches


# --- Step 5: Visualization Function ---
def visualize_top_ipc_sections(top_matches):
    plt.figure(figsize=(10, 6))

    # Convert Section numbers to string to ensure correct plotting
    top_matches["Section"] = top_matches["Section"].astype(str)

    plt.barh(top_matches["Section"], top_matches["similarity_score"], color='skyblue')
    plt.xlabel("Similarity Score")
    plt.ylabel("IPC Section")
    plt.title("Top Matching IPC Sections")
    plt.gca().invert_yaxis()  # Highest similarity on top
    plt.show()



# --- Step 6: Process User Query ---
def process_user_query(user_query):
    print("\n🔹 User Query:", user_query)

    abstract = generate_abstract(user_query)
    if "Error" in abstract:
        print("\n🔹 Error Generating Abstract:", abstract)
        return None

    print("\n🔹 Generated Abstract:", abstract)

    top_matches = match_ipc_sections(abstract, top_n=5)

    print("\n🔹 Top IPC Sections:")
    for _, row in top_matches.iterrows():
        print(f"Section: {row['Section']} | Title: {row['section_title']} | Score: {row['similarity_score']:.4f}")

    visualize_top_ipc_sections(top_matches)


# --- Example Usage ---
user_query = "The case of the prosecution was that Musammat Sobha an old woman aged about 70 resided with her son-in-law Sattan Jadav and grandson Jugeshwar.", "She possessed about 3 1/2 to 4 bighas of land & she had given Jugeshwar on the occasion of his marriage about 1 1/2 bighas of land.", "The remaining lands were cultivated by Sattan on her behalf.", "The Appellant was not directly related to the old woman, but his wife was related to her, the latter being a sister of the maternal grandmother of the Appellant's wife.", "Though Musammat Sobha lived with her son-in-law and grandson, she had occasional differences with them and on such occasions she stayed in the house of the Appellant.", "Some eight or ten days before the night of occurrence, she had been taken to the house of the Appellant on the invitation to partake of some sweets prepared from fresh milk of a she-buffalo, which had recently given birth to a calf.", "She stayed in the house of the Appellant for some days and on the 8th December 1952 she was taken to the office of the Sub-Registrar at Kharagpur where she executed and got registered a deed of sale in favour of the son of the Appellant, in respect of some 2 bighas and 19 dhurs of land.", "When Sattan came to know of the execution of the sale deed he went to the house of the Appellant and made an enquiry.", "On learning that such a sale deed had been executed Sattan gave an information at the police station and filed an application in the name of his son in the office of the Sub-Registrar.", "In the application made to the Sub-Registrar it was alleged that the old woman was of poor understanding and no consideration had been paid for the sale and a prayer was made that an enquiry be made from the people of the village as to the mental capacity of the old woman.", "In the information which was given at the police station it was alleged that the sale deed had been executed as a result of undue influence and pressure.", "This application and the information were given on the morning of the 10th December 1952.", "Early on the 11th December 1952 it was discovered that the old woman was dead.", "The prosecution case was that early in the morning of the 11th, the Appellant went to a neighbouring village to purchase 'coffin' cloth.", "He brought the coffin cloth and was anxious to cremate the dead body.", "Sattan and other villagers came to know of it and suspecting some foul play, they informed the chowkidar and the deffadar, both of whom came and stopped the Appellant from taking away the dead body for cremation.", "One Jagdish Jadav (P.W. 1) was then sent to police station which was at a distance of about 8 miles from the village and he gave an information at about 11 a.m. on the 11th December 1952.", "An inquest was held on the dead body of the old woman and the dead body was sent to the Civil Surgeon of Monghyr for post mortem examination.", "The post mortem examination was held on the 12th December 1952 at 9 a.m. On dissection of the body the Civil Surgeon found a patch of echymosis, 3 \"in diameter on the left side of the chest over the second and third intercostal space along the mammary line.", "The injury had caused a fracture of the third rib and the chest bone near it (sternum) attached to the third rib.", "In the opinion of Civil Surgeon the injuries on the chest resulting in the fractures were ante mortem injuries and were caused either by blows with a hard and blunt substance or by applying heavy pressure on the chest.", "The doctor explained that the injuries on the chest could be caused by putting the weight of one's body on to the chest of the deceased woman while the latter was lying down, either through the hands or by using one knee, thereby leaving no external marks of injury on the chest.", "The doctor was definitely of the opinion that the old woman died as a result of shock caused by the injuries on her chest."
process_user_query(user_query)
