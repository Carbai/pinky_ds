import pandas as pd

class DataProcessor():
    
    def __init__(self, data, keys=None):
        """
        Initialize the processor with raw data dictionary.
        """
        keys = keys or {
            'all': 'Vittime di omicidio - Totale',
            'male': 'Vittime di omicidio - Maschi',
            'female': 'Vittime di omicidio - Femmine',
            'geo': 'Vittime di omicidio-Regioni'
        }
        self.data = data
        self.df_all = data.get(keys['all'])
        self.df_males = data.get(keys['male'])
        self.df_females = data.get(keys['female'])
        self.df_geo = data.get(keys['geo'])

    def preprocess_df(self, df, type='all'):
        """
        Preprocess a DataFrame by cleaning and reshaping it.
        """
        df.dropna(axis=0,how='all',inplace=True) #drop empty rows
        df=df.drop(df.index[0:1]).reset_index(drop=True) #drop unrequired rows
        df.columns=df.iloc[0]
        df=df.drop(df.index[0:2]).reset_index(drop=True) 
        df.rename(columns={'2022 (b)':2022},inplace=True)
        df_tot_raw=df.iloc[0:7]
        sum_close=df_tot_raw.iloc[0:2].sum() #sum rows for partner and ex-partner in one row
        sum_close['RELAZIONE DELLA VITTIMA CON L\'OMICIDA']='Partner or Ex Partner'
        df_tot_raw.iloc[0]=sum_close
        df_tot_raw=df_tot_raw.drop(df_tot_raw.index[1]).reset_index(drop=True)

        # Step 1: Melt the DataFrame to make it long-form
        melted_df = pd.melt(
            df_tot_raw,
            id_vars=['RELAZIONE DELLA VITTIMA CON L\'OMICIDA'], 
            var_name='Year', 
            value_name='Number killed'
        )
        # Step 2: Pivot the melted DataFrame
        transposed_df = melted_df.pivot(
            index='Year', 
            columns='RELAZIONE DELLA VITTIMA CON L\'OMICIDA', 
            values='Number killed'
        ).reset_index().rename_axis(None, axis=1)
        transposed_df.name=None
        transposed_df=transposed_df.add_prefix(type+'_').rename(columns={type+'_Year': 'Year'})
      #  print(transposed_df.head(), type, 'yo')
        return transposed_df

    def merge_df(self):#, df):
        """
        Merge preprocessed DataFrames for all, male, and female data.
        """
        df_all=self.preprocess_df(self.df_all, type='all')
        df_males=self.preprocess_df(self.df_males, type='males')
        df_females=self.preprocess_df(self.df_females, type='females')
        merged_df = df_all.merge(df_males, on='Year').merge(df_females, on='Year')
        merged_df['Year']=pd.to_datetime(merged_df['Year'], format='%Y')
        return merged_df

    def get_bar_df(self, merged_df, type='females'):
        """
        Create a long-form DataFrame for bar plots.
        """
        new_categories={type+'_Altro conoscente ': 'Acquaintance',
        type+'_Altro parente': 'Relative',
        type+'_Autore non identificato': 'Unknown',
        type+'_Autore sconosciuto alla vittima': 'Stranger',
        type+'_Partner or Ex Partner': 'Partner or ex'}
        val_vars=list(new_categories.keys())
        df = merged_df.melt(
        id_vars=['Year'],  # The column to keep fixed
        value_vars=val_vars, 
        var_name='Category',  # Name for the new category column
        value_name='Count')
        df['Category']=df['Category'].apply(lambda x: new_categories[x])
        df['Total_Per_Year'] = df.groupby('Year')['Count'].transform('sum')
        df['Count'] = df['Count'].astype('int')
        df['Percentage'] = (df['Count'] / df['Total_Per_Year']) * 100
        df['Percentage'] = df['Percentage'].astype('int').astype(str)+'%'
        df['Label'] = df['Count'].astype(int).astype(str) + ' (' + df['Percentage'].astype(str) + '%)'
        return df
    
    def map_regions(self, region, regions_dict):
        try:
            return regions_dict[region]
        except KeyError:  
            return region  
        
    def get_regions(self, cols, regions_dict, population, exclude=['Trento', 'Bolzano/Bozen']):
        """
        Extract data for regions.
        """
        self.df_geo.dropna(axis=0,how='all',inplace=True)
        self.df_geo.dropna(axis=1,how='all',inplace=True)
        self.df_geo.drop(columns=self.df_geo.columns[-6:],inplace=True)
        self.df_geo.drop(index=[0,1,3,4,7],inplace=True)
        self.df_geo.reset_index(drop=True,inplace=True)
        self.df_geo=self.df_geo.iloc[0:22]
     #   print(self.df_geo.head())
        self.df_geo.columns=cols
        self.df_geo['reg_name'] = self.df_geo['reg_name'].apply(lambda x: self.map_regions(x, regions_dict))
        mask = ~self.df_geo['reg_name'].isin(exclude)
        self.df_geo=self.df_geo[mask].reset_index(drop=True)
       # self.df_geo=self.df_geo.apply(pd.to_numeric, errors='ignore', downcast='integer')
        for column in self.df_geo.columns:
            try:
                self.df_geo[column] = pd.to_numeric(self.df_geo[column], downcast='integer')
            except Exception as e:
                pass

        population['Territorio']=population['Territorio'].apply(lambda x: x.replace(' / ', '/') if '/' in x else x)
        population['Territorio']=population['Territorio'].apply(lambda x: x.replace('Trentino Alto', 'Trentino-Alto') if 'Trentino' in x else x)
        df=pd.merge(
            self.df_geo,  # Second DataFrame
            population[['Territorio', 'Value']],  # Select only necessary columns from df1
            left_on='reg_name',  # Match 'reg_name' in df2
            right_on='Territorio',  # Match 'Territorio' in df1
            how='left'  # Use 'left' join to keep all rows in df2
            )
        df.rename(columns={'Value':'Popolazione'}, inplace=True)
        df['Females - Partner or ex partner - norm']=df['Females - Partner or ex partner']/df['Popolazione']*100000
        df['Females - Partner or ex partner - norm']=df['Females - Partner or ex partner - norm'].apply(lambda x: round(x, 2))
        return df



