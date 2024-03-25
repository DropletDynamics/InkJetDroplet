import pickle

# Define a file name to store the progress
progress_file = "progress.pkl"

# Define a function to save the progress to the file
def save_progress(V1, V2, V3, w1, w2, w3, d1, d2):
    with open(progress_file, "wb") as f:
        pickle.dump((V1, V2, V3, w1, w2, w3, d1, d2), f)

# Define a function to load the progress from the file
def load_progress():
    with open(progress_file, "rb") as f:
        return pickle.load(f)
    

if __name__ == "__main__":
    # Define the initial values of the loop variables
    V1_init = -94
    V2_init = 14
    V3_init = -5
    w1_init = 26
    w2_init = 11
    w3_init = 31
    d1_init = 6
    d2_init = 6
    save_progress(V1_init, V2_init, V3_init, w1_init, w2_init, w3_init, d1_init, d2_init)
    