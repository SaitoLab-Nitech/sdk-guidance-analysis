import os
import time
import math
import evaluate
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from transformers import DataCollatorForTokenClassification
from transformers import TrainingArguments, Trainer

LABEL_NAMES = [
    'O', 'B-SDK', 'I-SDK', 'B-PRA', 'I-PRA', 'B-DAT', 'I-DAT',
    'B-DES', 'I-DES', 'B-CON', 'I-CON', 'B-EPH', 'I-EPH',
    'B-PUR', 'I-PUR', 'B-ENC', 'I-ENC', 'B-DEL', 'I-DEL'
]
METRIC = evaluate.load("seqeval")

def align_labels_with_tokens(labels, word_ids):
    new_labels = []
    current_word = None
    for word_id in word_ids:
        if word_id != current_word:
            # Start of a new word!
            current_word = word_id
            label = -100 if word_id is None else labels[word_id]
            new_labels.append(label)
        elif word_id is None:
            # Special token
            new_labels.append(-100)
        else:
            # Same word as previous token
            label = labels[word_id]
            # If the label is B-XXX we change it to I-XXX
            if label % 2 == 1:
                label += 1
            new_labels.append(label)

    return new_labels

def tokenize_and_align_labels(examples, tokenizer):
    tokenized_inputs = tokenizer(
        examples["tokens"], truncation=True, is_split_into_words=True
    )
    all_labels = examples["ner_tags"]
    new_labels = []
    for i, labels in enumerate(all_labels):
        word_ids = tokenized_inputs.word_ids(i)
        new_labels.append(align_labels_with_tokens(labels, word_ids))

    tokenized_inputs["labels"] = new_labels
    return tokenized_inputs

def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)

    # Remove ignored index (special tokens) and convert to labels
    true_labels = [[LABEL_NAMES[l] for l in label if l != -100] for label in labels]
    true_predictions = [
        [LABEL_NAMES[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    all_metrics = METRIC.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
    }


class Evaluator:
    def __init__(self, dataset_path, model_checkpoint, seed, tokenizer, test_size=0.3):
        self.dataset_path = dataset_path
        self.seed = seed
        self.test_size = test_size

        self.args = TrainingArguments(
            output_dir='tc_checkpoints/',
            no_cuda=True,
        )
        print(f'{self.args.no_cuda = }')

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        print(f'{self.tokenizer.is_fast = }')
        assert self.tokenizer.is_fast

        self.data_collator = DataCollatorForTokenClassification(tokenizer=self.tokenizer)

        id2label = {i: label for i, label in enumerate(LABEL_NAMES)}
        label2id = {v: k for k, v in id2label.items()}
        self.model = AutoModelForTokenClassification.from_pretrained(
            model_checkpoint,
            id2label=id2label,
            label2id=label2id,
        )
        print(f'{self.model.config.num_labels = }')
        assert self.model.config.num_labels == len(LABEL_NAMES)

    def run(self, target):
        data_files = {
            'train': f'{self.dataset_path}{target}.json',
            'test': f'{self.dataset_path}{target}.json',
        }
        raw_dataset = load_dataset('json', data_files=data_files)
        shuffled_dataset = raw_dataset.shuffle(seed=self.seed)

        if (self.test_size < 1):
            splitted_dataset = shuffled_dataset['train'].train_test_split(test_size=self.test_size, shuffle=False)
        else:
            assert self.test_size == 1
            splitted_dataset = shuffled_dataset

        print(splitted_dataset['test'])
        print(splitted_dataset['test'][0]['tokens'])
        print(splitted_dataset['test'][0]['ner_tags'])
        print(f'num data: {len(splitted_dataset["test"])}')

        tokenized_datasets = splitted_dataset.map(
            tokenize_and_align_labels,
            batched=True,
            remove_columns=splitted_dataset["test"].column_names,
            fn_kwargs={'tokenizer': self.tokenizer},
        )

        trainer = Trainer(
            model=self.model,
            args=self.args,
            eval_dataset=tokenized_datasets["test"],
            data_collator=self.data_collator,
            compute_metrics=compute_metrics,
            tokenizer=self.tokenizer,
        )

        start = time.time()

        result = trainer.evaluate()

        print(f'The evaluation took {time.time() - start} seconds')

        return result
