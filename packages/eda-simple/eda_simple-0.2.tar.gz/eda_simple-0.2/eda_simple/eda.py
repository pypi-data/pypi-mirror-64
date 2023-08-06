class Eda:
    def __init__(self):
        self.data = []
        
       
    def read_data_file(self, file_path):
        self.data=pd.read_csv(file_path)
        return self.data
        
    def plot(self):
        numeric=self.data.select_dtypes(include=['float64'])
        plt.plot(numeric)
        display()
    def correlation_plot(self,data, method = "pearson", triangle = True, shrink = 0.5, orientation = "vertical", my_palette = None):
        """
        Function to obtain correlation matrix and associated correlation plot.
        :param data: pandas dataframe - data set to calculate correlations from.
        :param method: Default "pearson". Type of correlation to compute. See pandas.DataFrame.corr() for more information.
        :param triangle: Either True or False; default is True, Whether to plot the full heatmap of correlations or only the lower triangle.
        :param shrink: Governs the size of the color bar legend. See matplotlib.pyplot.colorbar() for more information.
        :param orientation. Either "vertical" or "horizontal"; default is "vertical". Governs where the color bar legend is plotted. See matplotlib.pyplot.colorbar() for more information.
        :return: tuple of (corr_mat, ax.figure). corr_mat is a pandas.DataFrame() holding the correlations. ax.figure is the plot-object of the heatmap.
        """
        data=self.data
        corr_mat = data.corr(method=method)

        if triangle == True:
          mask = np.zeros_like(corr_mat)
          mask[np.triu_indices_from(mask)] = True
        else:
          mask = None

        with sns.axes_style("white"):
            plt.figure(figsize=(15,15))
            ax = sns.heatmap(corr_mat, vmin = -1,vmax= 1, square=True, cmap = my_palette, cbar_kws={"shrink": shrink, "orientation": orientation}, mask=mask)
            ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize = 6)
            ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize = 6)
        return corr_mat, ax.figure