import pandas as pd

# IPC training data
data = [
    {"text": "User: Someone is threatening me.\nAssistant: This may fall under IPC Section 503 - Criminal Intimidation. It deals with threats that cause alarm or fear of harm to person, reputation, or property."},
    {"text": "User: I was cheated in a business deal.\nAssistant: You may refer to IPC Section 420 - Cheating and dishonestly inducing delivery of property. It applies when someone deceives another to part with property or money."},
    {"text": "User: My neighbor is verbally abusing me.\nAssistant: This could come under IPC Section 504 - Intentional insult with intent to provoke breach of the peace."},
    {"text": "User: A person pushed me and tried to hit me.\nAssistant: This act falls under IPC Section 352 - Punishment for assault or criminal force otherwise than on grave provocation."},
    {"text": "User: Someone spread false rumors about me.\nAssistant: This may fall under IPC Section 499 - Defamation. It punishes harming someone’s reputation through false statements."},
    {"text": "User: A man tried to touch a woman inappropriately.\nAssistant: This is covered under IPC Section 354 - Assault or criminal force to woman with intent to outrage her modesty."},
    {"text": "User: My phone was stolen yesterday.\nAssistant: IPC Section 379 - Punishment for theft applies here. It punishes theft with imprisonment up to 3 years, or fine, or both."},
    {"text": "User: My house was broken into at night.\nAssistant: IPC Section 457 - Lurking house-trespass or house-breaking by night to commit offence punishable with imprisonment."},
    {"text": "User: Someone forged my signature on a cheque.\nAssistant: This comes under IPC Section 465 - Punishment for forgery."},
    {"text": "User: I’m getting threatening messages online.\nAssistant: IPC Section 507 - Criminal intimidation by anonymous communication can be applied in this case."}
]

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("ipc_finetune_data.csv", index=False)
