import pickle
import os

def pickle_file(file_path, pickle_path):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        with open(pickle_path, 'wb') as pkl_file:
            pickle.dump(file_data, pkl_file)
        
        print(f"File '{file_path}' pickled successfully to '{pickle_path}'")
    except Exception as e:
        print(f"Error pickling file: {e}")

def unpickle_file(pickle_path):
    try:
        with open(pickle_path, 'rb') as pkl_file:
            original_data = pickle.load(pkl_file)
        
        original_file_path = "unpickled_file"
        with open(original_file_path, 'wb') as f:
            f.write(original_data)
        
        print(f"Pickled data unpickled and saved to '{original_file_path}'")
    except Exception as e:
        print(f"Error unpickling file: {e}")

original_file = 'weather_data.json'
pickled_file = 'save.pkl'

pickle_file(original_file, pickled_file)


#unpickle_file(pickled_file)
