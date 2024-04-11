import torch
from importlib import import_module


class TextPredictor:
    _instance = None

    def __new__(cls, model_name='bert', dataset_name='chenle/bert_model/PatentData'):
        if cls._instance is None:
            cls._instance = super(TextPredictor, cls).__new__(cls)
            cls._instance.setup(model_name, dataset_name)
        return cls._instance

    def setup(self, model_name, dataset_name):
        self.key = {
            0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
            5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
            10: '10', 11: '11'
        }
        x = import_module('chenle.bert_model.models.' + model_name)
        self.config = x.Config(dataset_name)
        self.model = x.Model(self.config).to("cpu")
        self.model.load_state_dict(torch.load(self.config.save_path, map_location='cpu'))

    def build_predict_text(self, text):
        token = self.config.tokenizer.tokenize(text)
        token = ['[CLS]'] + token
        seq_len = len(token)
        mask = []
        token_ids = self.config.tokenizer.convert_tokens_to_ids(token)
        pad_size = self.config.pad_size
        if pad_size:
            if len(token) < pad_size:
                mask = [1] * len(token_ids) + ([0] * (pad_size - len(token)))
                token_ids += ([0] * (pad_size - len(token)))
            else:
                mask = [1] * pad_size
                token_ids = token_ids[:pad_size]
                seq_len = pad_size
        ids = torch.LongTensor([token_ids])
        seq_len = torch.LongTensor([seq_len])
        mask = torch.LongTensor([mask])
        return ids, seq_len, mask

    def predict(self, text):
        data = self.build_predict_text(text)
        with torch.no_grad():
            outputs = self.model(data)
            num = torch.argmax(outputs)
        return self.key[int(num)]


def get_predictor():
    return TextPredictor()


# 确保在应用启动时实例化TextPredictor
predictor_instance = get_predictor()
