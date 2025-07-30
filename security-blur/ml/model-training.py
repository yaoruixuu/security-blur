
# generate dataset
from data import generate_data

labels, texts = generate_data()

from datasets import Dataset
dataset = Dataset.from_dict({"text": texts, "label": labels})

dataset = dataset.train_test_split(test_size=0.2)

# load distilbert tokenizer
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")

# preprocess function
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# data padding obj
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# evaluate
import evaluate

accuracy = evaluate.load("accuracy")

import numpy as np

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

# label mapping
id2label = {0: "UNCLASSIFIED", 1: "CLASSIFIED", 2: "SECRET", 3: "TOP SECRET"}
label2id = {"UNCLASSIFIED": 0, "CLASSIFIED": 1, "SECRET": 2, "TOP SECRET": 3}

# training
# load model and trainer
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert/distilbert-base-uncased", num_labels=4, id2label=id2label, label2id=label2id
)

# set args and train
training_args = TrainingArguments(
    output_dir="security-level-classifier",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    processing_class=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

train_result = trainer.train()

print(train_result.metrics)

metrics = trainer.evaluate()
print(metrics)

# Save model and tokenizer at the end
trainer.save_model("security-level-classifier")
tokenizer.save_pretrained("security-level-classifier")

