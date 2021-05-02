import json
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        try:
            vectors = json.load(file)
            print("Vectors : ", vectors)
            print("Parsed Succesfully!")
        except json.decoder.JSONDecodeError:
            print("Decoding JSON has failed.")
    file.close()

