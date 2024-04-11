import os
import glob
from evaluator import Evaluator

TARGETS = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 23, 24, 25, 27, 31, 32, 33, 34, 35, 36, 37, 40, 41, 42, 43,
           44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
dataset_path = 'dataset/'
tokenizer = 'bert-base-cased'
seed = 27
test_size = 1.0
result_output_path = 'result.csv'
checkpoint_path = 'path_to_model_checkpoint/'

result_accuracy = ''


def run_one_evaluation(target, prev_id):
    global result_accuracy

    print(f'{target = }, {prev_id = }')

    if (os.path.getsize(f'{dataset_path}{target}.json') < 4):
        result_accuracy += f'{target},0\n'
        return

    model_checkpoint = glob.glob(f'{checkpoint_path}{prev_id}/checkpoint-*')[0]
    print(model_checkpoint)

    evaluator = Evaluator(dataset_path, model_checkpoint, seed, tokenizer, test_size=test_size)

    ret = evaluator.run(target)
    print(f'precision: {ret["eval_precision"]}')
    print(f'recall:    {ret["eval_recall"]}')
    print(f'f1:        {ret["eval_f1"]}')
    print(f'accuracy:  {ret["eval_accuracy"]}')

    result_accuracy += f'{target},{ret["eval_accuracy"]},{ret["eval_precision"]},{ret["eval_recall"]},{ret["eval_f1"]}\n'


for i in range(len(TARGETS)-1):
    run_one_evaluation(TARGETS[i+1], TARGETS[i])

print(result_accuracy)

with open(result_output_path, 'w') as f:
    f.write(result_accuracy)

print('Done!')
