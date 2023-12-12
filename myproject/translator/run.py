import argparse
import infer

def main():
    parser = argparse.ArgumentParser(description='Transformer dialect machine translation')
    parser.add_argument('--data-dir', default='./dataset',type=str,
                        help='path to dataset directory')
    parser.add_argument('--ckpt', default='./results/model.pth',type=str,
                        help='Path in which saved the model file')
    parser.add_argument('--dial-num', default=4, type=int, help='Number of dialects')
    parser.add_argument('--input-sent', default='안녕', help='Input sentence to translate')
    args = parser.parse_args()

    # Modify the input-sent argument
    args.input_sent = input("Enter the new input sentence: ")

    # Call the main function from infer.py
    translated_text = infer.main(args)

    return translated_text

if __name__ == '__main__':
    translated_text = main()
    print(translated_text)