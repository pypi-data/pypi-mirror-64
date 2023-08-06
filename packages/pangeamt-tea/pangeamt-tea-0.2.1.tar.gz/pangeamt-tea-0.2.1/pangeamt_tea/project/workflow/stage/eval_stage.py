import asyncio
import time
import os
import subprocess
import click
from autoclass import autoclass
from pangeamt_nlp.seg import Seg
from pangeamt_tea.project.workflow.stage.base_stage import BaseStage
# from pangeamt_tea.project.workflow.workflow import WorkflowAlreadyExists
from pangeamt_nlp.tokenizer.tokenizer_factory import TokenizerFactory
from pangeamt_nlp.truecaser.truecaser import Truecaser
from pangeamt_nlp.processor.pipeline_decoding import PipelineDecoding
from pangeamt_nlp.bpe.bpe import BPE
from sacrebleu import corpus_bleu
from pangeamt_nlp.translation_model.translation_model_factory import (
    TranslationModelFactory,
)


class EvalStage(BaseStage):
    NAME = "eval"
    DIR = "04_evaluated"

    def __init__(self, workflow):
        super().__init__(workflow, self.NAME)

    async def run(self):
        project = self.workflow.project
        project_dir = project.config.project_dir
        config = project.config

        workflow_dir = self.workflow.get_dir(project_dir)
        self.stage_dir = os.path.join(workflow_dir, EvalStage.DIR)

        if os.path.isdir(self.stage_dir):
            raise WorkflowAlreadyExists(project_dir)

        os.mkdir(self.stage_dir)

        name = config.translation_model["name"]
        args = config.translation_model["args_decoding"]
        translation_model = TranslationModelFactory.get_class(name)
        model_dir = os.path.join(workflow_dir, "03_trained")

        for file in os.listdir(model_dir):
            if file.endswith(".pt"):
                model_path = os.path.join(model_dir, file)

        self._prepare_dir = os.path.join(workflow_dir, "02_prepared")
        tokenizer = self._init_tokenizer()
        truecaser = Truecaser()

        src_path = os.path.join(self._prepare_dir, "04_bpe", "test_src.txt")
        tgt_path = os.path.join(self._prepare_dir, "01_raw", "test_tgt.txt")
        out_path = os.path.join(self.stage_dir, "test_output.txt")

        decoding_model = translation_model(model_path, **args)

        print("Model loaded")

        bleu = 0

        with open(src_path, "r") as src_file, open(tgt_path, "r") as tgt_file:
            with open(out_path, "w") as out_file:
                batch = []
                for i, (src_line, tgt_line) in enumerate(
                    zip(src_file, tgt_file)
                ):
                    if i % 30 == 0 and batch != []:
                        for translation in decoding_model.translate(batch):
                            translation = BPE.undo(translation)
                            translation = tokenizer.detokenize(
                                translation.split(" ")
                            )
                            translation = truecaser.detruecase(translation)
                            corpus = corpus_bleu([translation], [[tgt_line]])
                            bleu += corpus.score
                            out_file.write(translation)
                        print(bleu)
                        batch = [src_line]
                    else:
                        batch.append(src_line)

        decoding_model = None

        return {
            "Score": bleu/i
        }

    def _init_pipeline(self) -> PipelineDecoding:
        project = self.workflow.project
        config = project.config
        src_lang = config.src_lang
        tgt_lang = config.tgt_lang
        processors = config.processors

        return PipelineDecoding.create_from_dict(
            src_lang, tgt_lang, processors
        )

    def _init_tokenizer(self):
        project = self.workflow.project
        tgt_tok_name = project.config.tokenizer["tgt"]

        tgt_tokenizer = TokenizerFactory.new(
            project.config.tgt_lang, tgt_tok_name
        )

        return tgt_tokenizer
