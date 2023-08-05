import seaborn as sns

class MLS():
    def __init__(self):
        self.x=0

    def checkSkeweness(self,df):
        columns=df.columns.tolist()
        categoricalColumns=[]
        numericalColumns=[]
        for column in columns:
            if df[column].dtype=="object":
                categoricalColumns.append(column)
            else:
                numericalColumns.append(column)

        # plot disctribution and check skewness:
        for column in numericalColumns:
            a = sns.FacetGrid(df, aspect=4)
            a.map(sns.kdeplot, column, shade=True)
            a.add_legend()
            print('Skew for ', str(column), df[column].skew())


