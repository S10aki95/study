import pandas as pd
import numpy as np
import torch
from transformers import BertJapaneseTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, AdamW
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from tqdm import tqdm
import itertools

# %%
class IMDbDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


class bert_fine_tuning:
    def __init__(self, train_text, train_label, num_labels = 2):
        self.num_labels = num_labels
        self.model_path = 'cl-tohoku/bert-base-japanese-whole-word-masking'
        self.train = train_text
        self.labels = train_label

        self.tokenize_japanese()
    

    def tokenize_japanese(self):
        JP_tokenizer = BertJapaneseTokenizer.from_pretrained(self.model_path)

        #トークン化
        train_encodings = JP_tokenizer(self.train, truncation= True, padding=True)
        
        #Dataset型に変換
        train_dataset = IMDbDataset(train_encodings, self.labels)
        self.train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    

    def model_build(self):
        self.model = BertForSequenceClassification.from_pretrained(self.model_path, num_labels= self.num_labels)
    

    def model_parameter_fix(self, fix_layer_num):
        if fix_layer_num >=0 and fix_layer_num <=13:
            #上から何レイヤー固定するかの指定(0～13まで)
            #Embeddingを含める
            if fix_layer_num == 0:
                pass
            else:
                for params in self.model.bert.embeddings.parameters():
                    params.requires_grad = False
                
                for i in range(fix_layer_num):
                    for params in self.model.bert.encoder.layer[i].parameters():
                        params.requires_grad = False
                    
            #念のための確認(固定している最終レイヤーまで)
            print('trueなら微分実行')
            print('固定最終行', [para.requires_grad for para in self.model.bert.encoder.layer[fix_layer_num - 1].parameters()])
            print('学習レイヤー開始行', [para.requires_grad for para in self.model.bert.encoder.layer[fix_layer_num].parameters()])
        
        else:
            print('レイヤー数は0以上13以下です')

    def model_learning_rate(self, Decay_factor, learning_rate):
        
        # Emmbedding Layer, Encoder Layer 0～11, Pooling Layer, Classifer Layerの、15個のレイヤーについての学習率を用意する
        LearingRate_list = [learning_rate * (Decay_factor ** i) for i in range(15)]

        Embedding_lr = [{'params' : self.model.bert.embeddings.parameters(), 'lr' : LearingRate_list[0]}]
        Layers_lr = [{'params' : layer.parameters(), 'lr' : LearingRate_list[i+1]} for i, layer in enumerate(self.model.bert.encoder.layer)]
        Pooling_lr = [{'params' : self.model.bert.pooler.parameters(), 'lr' : LearingRate_list[13]}]
        Classifier_lr = [{'params' : self.model.classifier.parameters(), 'lr' : LearingRate_list[14]}]

        self.optim = AdamW(Embedding_lr + Layers_lr + Pooling_lr + Classifier_lr)

    def train_model(self):
        #モデルの学習(トレーニングの準備)
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(device)
        self.model.train()

        for epoch in range(3):
            running_loss = 0.0
            for i,batch in enumerate(tqdm(self.train_loader)):
                self.optim.zero_grad()
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs[0]
                loss.backward()
                self.optim.step()

                # print statistics
                running_loss += loss.item()
                if i % 10 == 9:    # print every 10 mini-batches
                    print('[%d, %5d] loss: %.3f' %(epoch + 1, i + 1, running_loss / 10))
                    running_loss = 0.0

    def Get_all_finetune_res(self, fix_layer_num, Decay_factor = 0.95, learning_rate = 2.0e-5, path_to_save = None):

        for comb in itertools.product(Decay_factor, learning_rate, fix_layer_num):
            Decay_factor, learning_rate, fix_layer_num = comb
            self.model_build()
            self.model_parameter_fix(fix_layer_num)
            self.model_learning_rate(Decay_factor= Decay_factor, learning_rate= learning_rate)
            self.train_model()
            if path_to_save is None:
                pass
            else:
                print('モデル保存')
                self.model.save_pretrained(path_to_save)
            del self.model
            torch.cuda.empty_cache()

#%%
if __name__ == '__main__':
    FineTune = bert_fine_tuning(train_text=None, train_label=None)
# %%
