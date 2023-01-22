import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings("ignore")

class ConsumptionData:

    '''
    This Class will perform a Pandas DataFrame with to show the consumption of each year. 
    It also creates a seasonal plot showing all 7-years of 2016-2022.

    __init__(self)
    load_data(self)
    group_by_year(self)
    plot_seasonal(self)
    main(self)
    '''
    def __init__(self) -> None:
        self.path = '/Users/behzad/My_codings/Petroineos_Test/raw_data/'

    def load_data(self):

        '''
        Loads and cleans raw data, and store it in a DataFrame

        RETURNS
        -------
        df_final (DataFrame)
            returens a pandas DataFrame
        '''

        df = pd.read_csv(self.path + "Consumption.csv")
        date_frmt1 = pd.to_datetime(df['Date'], errors='coerce', format='%d/%m/%Y')
        date_frmt2 = pd.to_datetime(df['Date'], errors='coerce', format='%Y%m%d')
        df['Date'] = date_frmt1.fillna(date_frmt2)
        return df

    def group_by_year(self):

        '''
        Creates a Pandas DataFrame for the energy consumption of each year in a way that having
        the years as columns and months-days (mm-dd) as index.

        Returns
        -------
        df_pvt (DataFrame)
            Returns a DataFrame for the consumption of each year with having the year as column 
            name and mm-dd as index
        '''

        df = self.load_data()
        df['Year'] = df['Date'].dt.year
        df = df.rename(columns = {'Date':'mm-dd'})
        df_pvt = pd.pivot_table(df, index=df['mm-dd'].dt.strftime('%m-%d'), columns='Year', values='Consumption')
        df_pvt['avg_all'] = df_pvt.mean(axis=1)
        df_pvt['5y_min'] = df_pvt[[2016,2017,2018,2019,2020]].min(axis=1)
        df_pvt['5y_max'] = df_pvt[[2016,2017,2018,2019,2020]].max(axis=1)
        return df_pvt

    def plot_seasonal(self):

        '''
        This method will provid a seasonal plot for the energy consumption showing 5-years range of 
        2016-2020 shaded, total average as dashed line, and years 2021 - 2022 as separate lines.
        '''

        df = self.group_by_year()
        fig, ax = plt.subplots(1, figsize=[14,6])

        ax.fill_between(df.index, df["5y_min"], df["5y_max"], label="5y range (2016-2020)", facecolor="gray")
        ax.plot(df.index, df[2021], label="2021", c="r")
        ax.plot(df.index, df[2022], label="2022", c="g")
        ax.plot(df.index, df.avg_all, label="total avg", c="k", ls='dashed', lw=3)

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.set_ylabel('Consumption')
        comment = "As illustrated, energy consumption starts to raise from the middle of October until the end \n" \
                "of May each year. On average, the energy consumption in winter is about double compared \n" \
                "with summertime. In 2021, energy usage follows an unexpected patern, which can have \n" \
                "several reasons such as COVID19 or climate changes (colderwinter).\n" \
                "The plot also shows the energy usage for 2022 has dropped below average, which could \n" \
                "be dueto changes in energy provider situations (such as the Ukraine war) and the \n" \
                "energy cost increases."
        ax.text(68, 435, comment, style='italic', bbox={
        'facecolor': 'grey', 'alpha': 0.1, 'pad': 10})
        ax.legend(loc = 'best')
        plt.savefig('seasonal_plot.png')
        plt.show()

    def main(self):
        
        data = self.group_by_year()
        print(data.head(1464))
        self.plot_seasonal()

if __name__ == '__main__':
    cons = ConsumptionData()
    cons.main()
