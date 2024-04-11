import os
import glob
from evaluator import Evaluator

EXCEPT_ONE = 44
SEED = 27
test_size = 1.0
TARGETS = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 23, 24, 25, 27, 31, 32, 33, 34, 35, 36, 37, 40, 41, 42, 43,
           44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
TARGETS.remove(EXCEPT_ONE)
dataset_path = 'dataset/'
tokenizer = 'bert-base-cased'
result_output_path = 'result.csv'
checkpoint_path = 'path_to_model_checkpoint/'

result_accuracy = ''


def run_one_evaluation(target):
    global result_accuracy

    print(f'{target = }')

    if (os.path.getsize(f'{dataset_path}{target}.json') < 4):
        result_accuracy += f'{target},0\n'
        return

    model_checkpoint = glob.glob(f'{checkpoint_path}{target}/checkpoint-*')[0]

    print(model_checkpoint)

    evaluator = Evaluator(dataset_path, model_checkpoint, SEED, tokenizer, test_size=test_size)

    ret = evaluator.run(EXCEPT_ONE)
    print(f'precision: {ret["eval_precision"]}')
    print(f'recall:    {ret["eval_recall"]}')
    print(f'f1:        {ret["eval_f1"]}')
    print(f'accuracy:  {ret["eval_accuracy"]}')

    result_accuracy += f'{target},{ret["eval_accuracy"]},{ret["eval_precision"]},{ret["eval_recall"]},{ret["eval_f1"]}\n'

for i in range(len(TARGETS)):
    run_one_evaluation(TARGETS[i])

print(result_accuracy)
with open(result_output_path, 'w') as f:
    f.write(result_accuracy)

print('Done!')
