import requests
import sys

# Getting the save directory from command line arguments
save_directory = sys.argv[1]

# URL of the file to download
file_url = "https://openblocklabs-interview-datasets.s3.amazonaws.com/market_depth/ekubo_market_depth_dataset.parquet"

# Path to save the file (including the filename)
save_path = f"{save_directory}/openblocks.parquet"

# Downloading the file
response = requests.get(file_url)

# Checking if the request was successful
if response.status_code == 200:
    # Writing the content of the request to a local file
    with open(save_path, "wb") as f:
        f.write(response.content)
    print(f"File successfully downloaded and saved as {save_path}")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
