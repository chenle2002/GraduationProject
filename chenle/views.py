from django.http import JsonResponse
import torch

from importlib import import_module


class TextPredictor:
    def __init__(self, model_name='bert', dataset_name='PatentData'):
        self.key = {
            0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
            5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
            10: '10', 11: '11'
        }

        x = import_module('models.' + model_name)
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


# Django视图函数
def predict_text(request):
    text = "本发明公开了一种基于深度学习的动脉瘤分割方法和装置，其中，该方法包括：获取头部扫描CT血管造影CTA图像"
    predictor = TextPredictor()
    result = predictor.predict(text)
    print({'result': result})
    return JsonResponse({'result': result})
    # if request.method == 'POST':
    #     text = request.POST.get('text', '')
    #     predictor = TextPredictor()
    #     result = predictor.predict(text)
    #     return JsonResponse({'result': result})
    # else:
    #     return JsonResponse({'error': 'This endpoint only supports POST requests.'})
