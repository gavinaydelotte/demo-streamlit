import pandas as pd
import yfinance as yf


class Stock:

    def __init__(self, symbol, start, end, ma_window: int = 10):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.ma_window = ma_window

    def get_data(self):
        try:
            data = yf.download(self.symbol, start=self.start, end=self.end, progress=False, multi_level_index=False)
            if data.empty:
                return None, f"No data found for ticker '{self.symbol}'"
            data = self.calc_returns(data)
            data = self._calc_ma(data)
            return data, f"Successfully retrieved data for ticker '{self.symbol}'"
        except Exception as e:
            return None, f"Error fetching data for ticker '{self.symbol}': {e}"

    def calc_returns(self, df: pd.DataFrame):
        df['change'] = df['Close'] - df['Close'].shift(1)
        df['return'] =np.log(df['Close']).diff().round(4)
        return df

    def _calc_ma(self, df: pd.DataFrame) -> pd.DataFrame:
       df['MA'] = df['Close'].rolling(window=self.ma_window).mean()
       return df

    def plot_return_dist(self): 
        mean_return = self.data['return'].mean()
        fig = px.histogram(self.data, x='return', nbins=35, title=f'Return Distribution for {self.symbol}', labels={'return': 'Daily Return'})
        fig.add_vline(x=mean_return, line_dash="dash", line_color="red")
        return fig


# --- For development testing only ---
def main():
    test = Stock("AAPL", "2023-01-01", "2024-01-01", ma_window=20)
    print(test.symbol)
    fig = test.plot_return_dist()
    fig.show()
    

if __name__ == '__main__':
    main()
