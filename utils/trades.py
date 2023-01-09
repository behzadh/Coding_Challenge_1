import pandas as pd
from datetime import datetime, timedelta
import plotly.figure_factory

pd.options.mode.chained_assignment = None

class TradingOHLC:

    '''
    This Class will perform a pandas Dataframe with OHLC format and plot a candlestick plot for every
    given products and contracts. It has the following methods

    __init__(self)
    load_data(self)
    creating_OHLC_dataset(self, start: datetime, end: datetime, product: str, freq: str)
    candlestick_plot(self, df: pd.DataFrame(), contract: str)
    main(self)
    '''

    def __init__(self) -> None:

        self.path = '/Users/behzad/My_codings/Petroineos_Test/raw_data/'

    def load_data(self):

        '''
        Loads raw data and replace Venue A and B with Venue AB as they are the same product 
        trading in two different venues.

        RETURNS
        -------
        df (DataFrame)
            It returens a pandas DataFrame
        '''

        df = pd.read_csv(self.path + "Trades.csv", parse_dates=['TradeDateTime'], index_col=['TradeDateTime'])
        df['Product'] = df['Product'].str.replace('Emission - Venue A','Emission - Venue AB')
        df['Product'] = df['Product'].str.replace('Emission - Venue B','Emission - Venue AB')
        return df

    def creating_OHLC_dataset(self, start: datetime, end: datetime, product: str, freq: str):
        
        '''
        This method generates OHLC dataset for a specific time intervals provided by user.
        They can choose between 15MIN, 1H, 1D intervals.

        Parameters
        ----------
        start (datetime)
            start time and date
        end (datetime)
            end time and date
        product (str)
            products trading 
        freq (str)
            the intrvals that user can select: ["15MIN","1H","1D"]

        Returns
        -------
        df_OHLC (DataFrame)
            Returns a data set in format of OHLC for all products and contracts
        '''

        df = self.load_data()
        self.product = product
        # select data for a specific product
        df = df[df['Product']==product]
        start = start
        end = end
        # defining three different intervals
        if freq =='15MIN': 
            intrval = timedelta(minutes=14)        
        
        elif freq =='1H': 
            intrval = timedelta(minutes=59)
        
        elif freq =='1D': 
            # replace hours with 0 to include data outside of 7:00-17:00 period
            start = start.replace(hour=0)
            # add one more day to the end time to include the last day data as well
            end = end.replace(hour=0) + timedelta(days=1)
            intrval = timedelta(days=1)
        
        else:
            print('Please choose the intrval between this options ["15MIN","1H","1D"]')

        current = start
        df_OHLC = pd.DataFrame()
        while current < end:
            start_time = current
            current += intrval
            # prepare data for each interval to be anlyzed
            df_temp = df[start_time : current]
            if freq =='15MIN': 
                df_cut = df_temp[(df_temp.index.hour >= 7) & (df_temp.index.hour < 17)]
                df_cut['Date'] = df_cut.index
                current = current+timedelta(minutes=1)
            
            elif freq =='1H': 
                df_cut = df_temp[(df_temp.index.hour >= 7) & (df_temp.index.hour < 17)]
                df_cut['Date'] = df_cut.index
                df_cut['Date'] = df_cut.Date.dt.to_period('H')
                current = current+timedelta(minutes=1)
            
            else:
                df_cut = df_temp
                df_cut['Date'] = df_cut.index
                df_cut['Date'] = df_cut.Date.dt.to_period('D')
            
            if not df_cut.empty:
                # creates OHLC dataset
                OHLC = df_cut.groupby(['Contract']).agg({'Date':'first','Price': ['first', 'max', 'min', 'last'],'Quantity': 'sum'})
                df_OHLC = pd.concat([df_OHLC,OHLC], axis=0)

        # rename the final dataframe columns
        df_OHLC.columns = ['DateTime','Open','High','Low','Close','Volume']
        return df_OHLC

    def candlestick_plot(self, df: pd.DataFrame(), contract: str):

        '''
        Candlestick plot for each spesific contract provided

        Parameters
        ----------
        df (DataFrame)
            OHLC style dataframe for candelstick plot
        contract (str)
            contract(s) of each product tradings
        '''

        # select data for each contract
        df = df[df.index.get_level_values('Contract')==contract]
        fig = plotly.figure_factory.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.DateTime.astype('str'))
        # adds title to the plot
        fig.update_layout(title_text=f'{self.product} / Contract {contract}')
        fig.show()

    def main(self):

        start = datetime(2022, 4, 18, 7)
        end = datetime(2022, 4, 21, 17)
        freq = '1H'
        product = 'Energy'
        result = self.creating_OHLC_dataset(start,end,product,freq)
        print(result)
        self.candlestick_plot(result,'Q01')   
        
if __name__ == '__main__':
    trd = TradingOHLC() 
    trd.main()