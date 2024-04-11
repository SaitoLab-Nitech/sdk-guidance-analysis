import os
import time
import math
import evaluate
import numpy as np
from datasets import load_dataset, concatenate_datasets, DatasetDict
from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from transformers import DataCollatorForTokenClassification
from transformers import TrainingArguments, Trainer


SEED = 20
OUTPUT_DIR = 'path_to_model_checkpoint/'
DATASET = 'dataset/'
MODEL_CHECKPOINT = 'bert-base-cased'

EPOCHS = 20
SAVE_PER_EPOCHS = 20
BATCH_SIZE = 32

TARGETS = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 23, 24, 25, 27, 31, 32, 33, 34, 35, 36, 37, 40, 41, 42, 43,
           44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
dataset_train = []
dataset_validation = []
for target in TARGETS:
    target_dataset_path = f'{DATASET}{target}.json'
    if (os.path.getsize(target_dataset_path) > 3):
        raw_dataset = load_dataset('json', data_files=target_dataset_path)
        shuffled_dataset = raw_dataset.shuffle(seed=SEED)

        splitted_dataset = shuffled_dataset['train'].train_test_split(test_size=0.3, shuffle=False)
        dataset_train.append(splitted_dataset['train'])
        dataset_validation.append(splitted_dataset['test'])

my_dataset = DatasetDict({
    'train': concatenate_datasets(dataset_train),
    'validation': concatenate_datasets(dataset_validation),
})

LABEL_NAMES = ['O', 'B-SDK', 'I-SDK', 'B-PRA', 'I-PRA', 'B-DAT', 'I-DAT', 'B-DES', 'I-DES', 'B-CON', 'I-CON', 'B-EPH', 'I-EPH', 'B-PUR', 'I-PUR', 'B-ENC', 'I-ENC', 'B-DEL', 'I-DEL']

print(my_dataset)
print(my_dataset['train'][0]['tokens'])
print(my_dataset['train'][0]['ner_tags'])
print(f'num data: {len(my_dataset["train"])}')

tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)

print(tokenizer.is_fast)
assert tokenizer.is_fast

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

def tokenize_and_align_labels(examples):
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

tokenized_datasets = my_dataset.map(
    tokenize_and_align_labels,
    batched=True,
    remove_columns=my_dataset["train"].column_names,
)

data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

metric = evaluate.load("seqeval")

def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)

    # Remove ignored index (special tokens) and convert to labels
    true_labels = [[LABEL_NAMES[l] for l in label if l != -100] for label in labels]
    true_predictions = [
        [LABEL_NAMES[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
    }

id2label = {i: label for i, label in enumerate(LABEL_NAMES)}
label2id = {v: k for k, v in id2label.items()}

model = AutoModelForTokenClassification.from_pretrained(
    MODEL_CHECKPOINT,
    id2label=id2label,
    label2id=label2id,
)

print(model.config.num_labels)
assert model.config.num_labels != 0
assert model.config.num_labels == len(LABEL_NAMES)

args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,

    # save_strategy="epoch",
    save_strategy="steps",
    save_steps=math.ceil(len(tokenized_datasets['train'])/BATCH_SIZE)*SAVE_PER_EPOCHS,

    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,

    no_cuda=True,
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
)

print(f'{args.save_strategy = }')
print(f'{args.save_steps = }')
print(f'{args.per_device_train_batch_size = }')
print(f'{args.per_device_eval_batch_size = }')
print(f'{args.num_train_epochs = }')
print(f'{args.no_cuda = }')

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    tokenizer=tokenizer,
)

start = time.time()

trainer.train()

print(f'The training took {time.time() - start} seconds')
print('Done!!')
