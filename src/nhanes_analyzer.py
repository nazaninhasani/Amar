import pandas as pd

class NhanesAnalyzer:
    def __init__(self, demo_file_path, bmx_file_path):
        self.demo_df = pd.read_sas(demo_file_path)
        self.bmx_df = pd.read_sas(bmx_file_path)
        self.merged_df = None
        self.analytical_population = None

    def merge_files(self):
        self.merged_df = pd.merge(self.demo_df, self.bmx_df, on='SEQN', how='inner')
        return len(self.demo_df), len(self.merged_df)

    def define_population(self, min_age=20):
        self.analytical_population = self.merged_df[self.merged_df['RIDAGEYR'] >= min_age].copy()
        dropped_count = len(self.merged_df) - len(self.analytical_population)
        return len(self.analytical_population), dropped_count

    def get_descriptive_stats(self, column_name):
        if self.analytical_population is None:
            raise ValueError("ابتدا باید متد define_population را اجرا کنید.")
            
        col_data = self.analytical_population[column_name].dropna()
        stats = {
            'تعداد': col_data.count(),
            'میانگین': col_data.mean(),
            'میانه': col_data.median(),
            'انحراف معیار': col_data.std(),
            'حداقل': col_data.min(),
            'چارک اول (25%)': col_data.quantile(0.25),
            'چارک سوم (75%)': col_data.quantile(0.75),
            'حداکثر': col_data.max()
        }
        return pd.Series(stats)