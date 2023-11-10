import pandas as pd
from google_play_scraper import reviews,Sort
import psycopg2
from sqlalchemy import create_engine
from tqdm import tqdm
import time
from sqlalchemy import exc

max_count_per_fetch = 100
def scrape_apps_review(app_id, n_max=100):
    
    continuation_token = None
    results = [] # variable to keep final data

    p_bar = tqdm(total=n_max + max_count_per_fetch) # progress bar

    star_time = time.time() # record the start time
    while len(results) <= n_max:
        try:
            result, continuation_token = reviews(
                app_id,
                count=max_count_per_fetch,
                continuation_token=continuation_token,
                lang="id",  # defaults to 'en'
                country="id",  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
                filter_score_with=None,  # defaults to None(means all score)
            )
        except:
            continue

        results += result
        p_bar.update(len(results))

        if continuation_token.token is None:
            break


    end_time = time.time() #record the end time
    elapsed_time = end_time - star_time

    df = pd.DataFrame(results)

    # Add 'app_id' and 'date_fetch' columns
    df['app_id'] = app_id
    df['date_fetch'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Data retrieval completed in {elapsed_time:.2f} seconds")
    return df

if __name__ == '__main__':
    app_id_to_scrape = ['com.tokopedia.tkpd','com.shopee.id','com.lazada.android','blibli.mobile.commerce','com.bukalapak.android']
    df_list = []

    for app_id in app_id_to_scrape:
        # Perform some task for each app_id
        print(f"Scraping reviews for {app_id}")
        df = scrape_apps_review(app_id)
        df_list.append(df)
    merged_df = pd.concat(df_list, ignore_index=True)

    print(merged_df["at"])

    # print(merged_df.max())
