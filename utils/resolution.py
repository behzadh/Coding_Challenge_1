import pandas as pd

class TimeResolution:

    '''
    A Class to perform a pandas Dataframe with 2-hours resolution in between 7:00 - 17:00

    __init__(self)
    load_data(self)
    two_hour_resolution(self)
    days_two_hour_resolution(self)
    final_merged_dataset(self)
    main(self)
    '''
    def __init__(self) -> None:

        self.path = '/Users/behzad/My_codings/Petroineos_Test/raw_data/'

    def load_data(self):

        '''
        Loads raw data and removes null values

        RETURNS
        -------
        df (DataFrame)
            Returens a pandas DataFrame
        '''
        
        df = pd.read_csv(self.path + "Merge.csv", parse_dates=['Datetime'], index_col=['Datetime'])
        df = df[df.Price.notnull()]
        return df

    def two_hour_resolution(self):

        '''
        Merges data with 2-hours resolution in between 7:00 - 17:00

        Returns
        -------
        df_2H (DataFrame)
            Returns data with 2-hours resolution
        '''

        df = self.load_data()
        df_cut = df[(df.index.hour >= 7) & (df.index.hour <= 17)]
        df_2H = df_cut.resample("2H",base=1).mean().dropna()
        return df_2H
    
    def days_two_hour_resolution(self):

        '''
        1-day resolution prices in the 2-hours window in between 7:00 - 17:00. Prices have been
        forward fill for the 1-day resolution in the 2-hours window.

        Returns
        -------
        df_D_2H (DataFrame)
            Returns data for 1-day dataset with 2-hours resolution
        '''

        df = self.load_data()
        df_D = df[(df['Resolution']=='D')]
        dti = pd.DataFrame((pd.date_range(start = df_D.index[0], end = df_D.index[-1], freq = '2H')), columns=['time'])
        dti = dti.set_index('time',drop=True)
        df_merge = df_D.join(dti,how='outer').ffill()
        df_merge = df_merge.drop(['Resolution'], axis=1)
        df_cut = df_merge[(df_merge.index.hour >= 7) & (df_merge.index.hour <= 17)]
        df_D_2H = df_cut.resample("2H",base=1).mean().dropna()
        return df_D_2H

    def final_merged_dataset(self):

        '''
        Merges the two hour resolution and days data together

        Returns
        -------
        final (DataFrame)
            Returns final merged data
        '''

        two_hour = self.two_hour_resolution()
        days = self.days_two_hour_resolution()
        result = pd.concat([two_hour,days], axis=0)
        return result

    def main(self):

        data = self.final_merged_dataset()
        print(data)

if __name__ == '__main__':
    res = TimeResolution() 
    res.main()