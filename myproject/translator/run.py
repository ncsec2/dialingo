# import infer
from . import infer
class Args:
    def __init__(self, data_dir='./dataset', ckpt='./results/model.pth', dial_num=4, input_sent='안녕'):
        self.data_dir = data_dir
        self.ckpt = ckpt
        self.dial_num = dial_num
        self.input_sent = input_sent

def main(user_sentences):
    print("main:", user_sentences)
    args = Args(input_sent = user_sentences)

    # Call the main function from infer.py
    translated_text = infer.main(args)

    return translated_text

if __name__ == '__main__':
    translated_text = main()
    print(translated_text)