from src.oram.OramClient import OramClient
from src.storage.LocalFsClient import LocalFsClient
import pandas as pd
import time
import matplotlib

if __name__ == '__main__':
    number_of_access_patterns = 20
    maximum_level = 18
    df_as_dict = dict()
    for i in range(2, maximum_level):
        print(f"Running for {i}")
        number_of_files = 2 ** i
        oram_manager: OramClient = OramClient(number_of_files, 512, LocalFsClient())

        start = time.time()
        for _ in range(number_of_access_patterns):
            oram_manager.write("test", b"test")

        end = time.time()
        total_time = end - start
        number_of_requests_per_sec = number_of_access_patterns / total_time
        df_as_dict[i] = number_of_requests_per_sec

    s = pd.Series(df_as_dict, name="number_of_requests_per_sec")
    s.index.name = "level"
    s.plot(x='col_name_1', y='col_name_2', style='o')
    s.to_csv('oram_write_performance.csv')
