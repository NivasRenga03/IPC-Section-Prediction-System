import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd

# Load training data from CSV file
data = pd.read_csv("ipc_finetune_data.csv")

# Convert the dataframe to a list of dictionaries
data = [{"text": row["text"]} for _, row in data.iterrows()]

# Convert data to Hugging Face dataset format
dataset = Dataset.from_list(data)

# Load tokenizer and model
model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Tokenization function
def tokenize_function(examples):
    tokens = tokenizer(examples["text"], truncation=True, max_length=128, padding="max_length")
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

# Tokenize the dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Training configuration
training_args = TrainingArguments(
    output_dir="./ipc_finetuned_model",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    logging_steps=1,
    save_strategy="no",
    no_cuda=True,  # Set to False if you have a GPU
    fp16=False
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Fine-tune the model
trainer.train()

# Save model and tokenizer
trainer.save_model("./ipc_finetuned_model")
tokenizer.save_pretrained("./ipc_finetuned_model")

# Test generation
def generate_response(prompt, max_length=128):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example test prompt
prompt = "User: Someone blackmailed me.\nAssistant:"
print("Response:", generate_response(prompt))
