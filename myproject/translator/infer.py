import argparse
import os
import torch
import json
import sentencepiece as spm

from .model import Transformer, Encoder, Decoder
from django.conf import settings

def main(args):
    absolute_path = os.path.join(settings.TRANSLATOR_ROOT, args.ckpt)
    # Get configuration
    config_path = os.path.join(os.path.dirname(absolute_path), 'configuration.json')

    print("config_path: ", config_path)
    # Get configuration
    # config_path = os.path.dirname(args.ckpt)+'/configuration.json'

    print(config_path)
    with open(config_path,'r') as f:
        print(f)
        config = json.load(f)
        

    # Load Dataset
    sp = spm.SentencePieceProcessor()
    sp.Load(f'{args.data_dir}/bpe_{config["vocab_size"]}.model')

    # Load Model
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    num_vocab = sp.get_piece_size()


    encoder = Encoder(
        input_dim=num_vocab+args.dial_num, 
        hidden_dim=config['hidden_dim'], 
        n_layers=config['enc_layer'], 
        n_heads=config['enc_head'], 
        pf_dim=512, 
        dropout_ratio=0.1, 
        device=device)

    decoder = Decoder(
        output_dim=num_vocab+args.dial_num, 
        hidden_dim=config['hidden_dim'], 
        n_layers=config['dec_layer'], 
        n_heads=config['dec_head'], 
        pf_dim=512, 
        dropout_ratio=0.1, 
        device=device)
    model = Transformer(
        encoder,
        decoder,
        sp.pad_id(),
        sp.pad_id(),
        device
    ).to(device)

    ckpt = torch.load(args.ckpt, map_location=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
    model.load_state_dict(ckpt)

    ### Translate Custom Sequence ###

    # input_list = ['느그 서장 남천동 살제 ?','겅 행 빠젼','그놈은 그냥 미끼를 던져분 것이고 자네 딸래미는 고것을 확 물어분 것이여','고마해라 마이 묵었다 아이가']
    # input_list = ['나 이 양반이영 살암수다 고치',
    #               '양쪽에 꽂으라고 이르케 하고 이르케 하고 이르케 하고 그러라고']
    translated_text = inference(model,sp,device,[args.input_sent])

    return translated_text
    
    ###############


def inference(model, sp, device, input_list):
    # 모델을 평가 모드로 전환합니다.
    model.eval()

    with torch.no_grad():
        for txt in input_list:
            seq = sp.encode_as_ids(txt)
            # print('seq:', seq)
            # print()

            seq = torch.cat((
                torch.tensor([sp.bos_id()]),
                torch.tensor(seq),
                torch.tensor([sp.eos_id()])
            ))
            src = seq.unsqueeze(0).to(device)
            # print('src:', src)
            # print()

            src_mask = model.make_src_mask(src)

            enc_src = model.encoder(src,src_mask)

            tgt_indices = [sp.bos_id()]

            # Generate sequence iteratively
            for i in range(500):
                tgt_tensor = torch.LongTensor(tgt_indices).unsqueeze(0).to(device)

                tgt_mask = model.make_tgt_mask(tgt_tensor)
                output, attention = model.decoder(tgt_tensor,enc_src,tgt_mask,src_mask)

                # print(output.argmax(2))
                
                pred_token = output.argmax(2)[:,-1].item()
                tgt_indices.append(pred_token)

                if pred_token == sp.eos_id():
                    break
            
            # translate = sp.id_to_piece(tgt_indices[1:])
            # Without location info
            # copy = sp.id_to_piece(src[0].tolist()[1:-1])
            # With location info : second token is location token
            # copy = sp.id_to_piece(src[0].tolist()[2:-1])

            translate = ' '.join(sp.id_to_piece(tgt_indices[1:]))
            copy = ' '.join(sp.id_to_piece(src[0].tolist()[2:-1]))

            # print(f"Source Sentence : {copy}")
            # print(f"Translated Sentence : {translate}")
            return translate


if __name__ == '__main__':
    translated_text = main()
    print(translated_text)
