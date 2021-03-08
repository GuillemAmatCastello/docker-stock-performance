from typing import Tuple, List, Dict
import pandas as pd
import numpy as np
import argparse
import datetime
import os

class style:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def main(day: str, n: int = 5):
    stocks = pd.read_csv(os.path.join(os.getcwd(), 'Individual_Stocks_SPX.csv'))
    stocks['Dates'] =  pd.to_datetime(stocks['Dates'], format='%m/%d/%Y')

    day = datetime.datetime.strptime(day, '%Y-%m-%d')
    prior_week = day - datetime.timedelta(weeks=1)

    #Calculating  difference
    day_stocks       = stocks[stocks['Dates']==day]
    prior_week_stocks = stocks[stocks['Dates']==prior_week]

    stocks_filtered = pd.DataFrame({'Current': day_stocks.T.iloc[1:, 0], 'Prior': prior_week_stocks.T.iloc[1:, 0]}).reset_index()
    stocks_filtered['Change'] = ((stocks_filtered['Current'] - stocks_filtered['Prior'])/stocks_filtered['Prior']).astype(float)*100

    winners = style.UNDERLINE + 'Winners:' + style.END

    winners_names  = stocks_filtered.nlargest(n, 'Change').iloc[:, 0].tolist()
    winners_change = stocks_filtered.nlargest(n, 'Change').iloc[:, 3].tolist()

    for i in range(len(winners_names)):
        winners += f' {winners_names[i]} ({round(winners_change[i], 2)}%)'
        if i < len(winners_names)-1:
            winners += ','
        else:
            winners += '.' 

    losers = style.UNDERLINE + 'Losers:' + style.END

    losers_names  = stocks_filtered.nsmallest(n, 'Change').iloc[:, 0].tolist()
    losers_change = stocks_filtered.nsmallest(n, 'Change').iloc[:, 3].tolist()

    for i in range(len(losers_names)):
        losers += f' {losers_names[i]} ({round(losers_change[i], 2)}%)'
        if i < len(losers_names)-1:
            losers += ','
        else:
            losers += '.' 

    return losers, winners


if __name__=="__main__":
    #Parse command line input
    #Arguments: day -> day of the week on which to base analysis, threshold -> threshold of significance
    parser = argparse.ArgumentParser(description='Top performing Equity stocks in a given week.')
    parser.add_argument('--day', type=str,
                        help='Day for which we want to find top stocks. Format: yyyy-mm-dd.')
    parser.add_argument('--n', type=int, 
                        help="Number of top stocks to be displayed. Format: int")
    args = parser.parse_args()

    c1, c2 = main(args.day, args.n)
    print(c1)
    print(c2)