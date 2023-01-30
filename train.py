"""Trains a preference model.

This is the main entry point to train a preference model (or reward model). WIP.
"""

import dataclasses

from transformers import TrainingArguments, HfArgumentParser

from pm.model import GPTRewardModel


@dataclasses.dataclass
class HParams:
    pretrained_model = 'CarperAI/openai_summarize_tldr_sft'
    use_deepspeed = False


parser = HfArgumentParser(HParams)
parser.add_argument('--use_deepspeed', help='Whether to enable deepspeed.')

if __name__ == "__main__":
    hparams: HParams = parser.parse_args_into_dataclasses()[0]

    training_args = TrainingArguments(
        output_dir="rm_checkpoint/",
        num_train_epochs=5,
        logging_steps=10,
        gradient_accumulation_steps=4,
        save_strategy="steps",
        evaluation_strategy="steps",
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        eval_accumulation_steps=1,
        eval_steps=500,
        save_steps=500,
        warmup_steps=100,
        logging_dir="./logs",
        fp16=False,
        bf16=False,
        learning_rate=1e-5,
        deepspeed="deepspeed_config.json" if hparams.use_deepspeed else None,
        save_total_limit=1,
    )

    # Initialize the reward model from the (supervised) fine-tuned GPT-J
    model = GPTRewardModel(hparams.pretrained_model)
