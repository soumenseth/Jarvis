from datasets import load_metric
import numpy as np
from transformers import AutoTokenizer, get_scheduler
from transformers import AutoModelForSequenceClassification
from torch.utils.data import DataLoader
from torch.optim import AdamW
import torch
from tqdm.auto import tqdm
from Utils.utils import *


class BertPytorchNative:
    def __init__(self, num_epochs=3, batch_size=8, lr=5e-5, seed=42, num_labels=4) -> None:
        self.labelled_data_filepath = "data/labelled_sentence_type_dataset.json"
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.metric = load_metric("accuracy")
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.seed = seed
        self.lr = lr
        self.num_labels = num_labels
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        
    def train(self):
        train_dataloader, eval_dataloader = self.get_train_eval_dataloaders()
        
        model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=self.num_labels)
        
        optimizer = AdamW(model.parameters(), lr=self.lr)
        num_training_steps = self.num_epochs * len(train_dataloader)
        lr_scheduler = get_scheduler(
            name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
        )
        model.to(self.device)
        
        progress_bar = tqdm(range(num_training_steps))

        model.train()
        for epoch in range(self.num_epochs):
            for batch in train_dataloader:
                batch = {k: v.to(self.device) for k, v in batch.items()}
                outputs = model(**batch)
                loss = outputs.loss
                loss.backward()

                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()
                progress_bar.update(1)
                
        model.eval()
        
        for batch in eval_dataloader:
            batch = {k: v.to(self.device) for k, v in batch.items()}
            with torch.no_grad():
                outputs = model(**batch)

            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)
            self.metric.add_batch(predictions=predictions, references=batch["labels"])

        print(self.metric.compute())
        
    def tokenize_function(self, examples):
        return self.tokenizer(examples["text"], padding="max_length", truncation=True)
    
    def compute_metrics(self, eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return self.metric.compute(predictions=predictions, references=labels)

    def get_train_eval_dataloaders(self):
        dataset = get_dataset(self.labelled_data_filepath)
        tokenized_datasets = dataset.map(self.tokenize_function, batched=True)
        
        tokenized_datasets = tokenized_datasets.remove_columns(["text"])
        tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
        tokenized_datasets.set_format("torch")
        
        small_train_dataset = tokenized_datasets["train"].shuffle(seed=self.seed).select(range(100))
        small_eval_dataset = tokenized_datasets["test"].shuffle(seed=self.seed).select(range(10))
        
        train_dataloader = DataLoader(small_train_dataset, shuffle=True, batch_size=self.batch_size)
        eval_dataloader = DataLoader(small_eval_dataset, batch_size=self.batch_size)
        return train_dataloader, eval_dataloader

if __name__ == "__main__":
    classifier = BertPytorchNative()
    classifier.train()
    