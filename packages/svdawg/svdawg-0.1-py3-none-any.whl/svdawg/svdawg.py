import numpy as np
import sys
import time
import argparse
import math 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler


"""
Reference:
https://www.d.umn.edu/~mhampton/m4326svd_example.pdf
"""


def svd_fp(fp, header='infer', sep='\t', index_col=None):
    """
    Compute SVD directly from filepath to a table of tab-separated numerical values

    Parameters:
            fp: Path to file
            header: Specify header, see Pandas.read_csv documentation for default option
            sep: field separator (default is tab separated). NOTE: this is different than default Pandas behavior
            index_col: specify if dataframe has an existing index (see default Pandas.read_csv documentation)

    Returns:
            A tuple containing the input dataframe and the result of a SVD on the data
            Tuple Contents: (Pandas.DataFrame, (U, S, V^T))
    """
    df = pd.read_csv(fp, header=header, sep=sep, index_col=index_col)
    try:
        df = df.astype(float)
    except (ValueError, TypeError):
        print('Data must be numeric')
        exit(1)
    return df, pd_svd(df)


def _test_equality(df1, df2):
    eq = np.isclose(df1, df2)
    if False in eq:
        return "WARNING: Original and reconstructed matrices are different."
    return "Original and reconstructed are equal"


def plot_mat(mat):
    """
    Plot a scaled matrix using red for negative and green for positive values

    Parameter:
            mat: some 2D matrix of numerical values
    """
    #color_palette = sns.color_palette("PiYG", 50)
    color_palette = sns.diverging_palette(5, 220, n=100, s=99, l=60, center='dark')
    sns.heatmap(mat, cmap=color_palette)
    plt.show()

def generate_synthetic_data(m, n): # noise=None):
    """
    Generate a toy dataset with dimension m x n

    Parameters:
            m: number of rows
            n: number of columns
    """
    pi2 = math.pi * 2
    x1 = np.arange(0, pi2, pi2/m)
    x2 = np.arange(0,pi2, pi2/n)
    y1 = np.sin(x1)
    y2 = np.sin(x2)
    y3 = np.cos(x1)
    y4 = np.cos(x2)
    mat = np.outer(y1, y2)
    mat2 = np.outer(y3, y4)
    return pd.DataFrame(mat + mat2)

# def sort_by_top_value(svd_results):
#     U, sigma, vt = svd_results
#     reconstructed = pd.DataFrame(U @ sigma @ vt)
#     udf = pd.DataFrame(U)
#     vtdf = pd.DataFrame(vt)
#     vtdf = vtdf.sort_values(by=0, axis=1)
#     udf = udf.sort_values(by=0)
#     reconstructed = reconstructed.iloc[udf.index.to_list(), vtdf.columns.to_list()]
#     return reconstructed

# def pd_svd(df):
    
#     U, s, vt = np.linalg.svd(df, full_matrices=False)
#     if len(df.index) > len(df.columns):
#         uidx
#     U = pd.DataFrame(U, index=df.index, columns=df.columns)
#     s = pd.DataFrame(s)
#     vt = pd.DataFrame(vt, index=df.columns, columns=df.columns)
#     return U, s, vt

def pd_scale(df):
    """
    StandardScaler transform of Pandas DataFrame, maintaining row and column labels.

    Parameters:
            df: Pandas DataFrame

    Returns:
            A scaled and labelled Pandas DataFrame
    """
    n = StandardScaler().fit_transform(df)
    return pd.DataFrame(n, index=df.index, columns=df.columns)

def pd_svd(df, scale=True, labels=True):
    """
    Compute SVD on a Pandas DataFrame, maintaining row and column labels.

    Parameters:
            df: Pandas DataFrame

    Returns:
            Returns decomposition of D = U.S.V^T as labelled
            Pandas DataFrames as a 3-ple, (U, S, V^T) 
    """
    if scale:
        U, s, vt = np.linalg.svd(pd_scale(df), full_matrices=False)
    else:
        U, s, vt = np.linalg.svd(df, full_matrices=False)
    if labels:
        if len(df.index) > len(df.columns):
            vtcols = df.columns
            vtidx = df.columns
            ucols = df.columns
            uidx = df.index
        else:
            vtcols = df.columns
            vtidx = df.index
            uidx = df.index
            ucols = df.index
        U = pd.DataFrame(U, index=uidx, columns=ucols)
        #s = np.diag(s)
        vt = pd.DataFrame(vt, index=vtidx, columns=vtcols)
    else:
        U = pd.DataFrame(U)
        vt = pd.DataFrame(vt)
    return U, pd.DataFrame(s), vt

def _plot_mat_ax(mat, ax, cbar=True):
    #color_palette = sns.color_palette("PiYG", 50)
    color_palette = sns.diverging_palette(5, 220, n=100, s=99, l=60, center='dark')
    sns.heatmap(mat, cmap=color_palette, ax=ax, cbar=cbar)
    #plt.show()

def fillnans(df, fill=0):
    """
    Parameters:
            df: Pandas DataFrame to clean
            fill: Value to use when replacing np.nan and np.inf (default=0)
    
    Returns:
            Returns a copy of the input Pandas DataFrame replacing all np.nan and np.inf with the specified value
    """
    rdf = df.replace([np.inf, -np.inf], np.nan)
    rdf = df.fillna(fill)
    return rdf

def plot_svs(svd, top=5):
    """
    Tool for plotting U and V^T sorted by top singular values

    Parameters:
            svd: A 3-ple containing the result of a SVD computed by 'pd_svd'
            top: Integer indicating which top singular values to sort by
    """
    sigma = [0 if np.isclose(0, s) else s for s in svd[1]]
    fig, ax = plt.subplots(2, top)
    for i in range(top):
        _plot_mat_ax(svd[0].sort_values(by=svd[0].columns[i]), ax[0,i])
        ax[0,i].set_title('Sorted by U column %d'%i)
        _plot_mat_ax(svd[2].sort_values(by=svd[2].index[i], axis = 1), ax[1,i])
        ax[1,i].set_title('Sorted by V transpose row %d'%i)

def plot_svd(svd):
    """
    Tool for plotting U and V^T

    Parameters:
            svd: A 3-ple containing the result of a SVD computed by 'pd_svd'
            sv: Integer indicating which singular value to sort by
    """
    fig, ax = plt.subplots(1, 2)
    _plot_mat_ax(svd[0], ax=ax[0])
    _plot_mat_ax(svd[2], ax=ax[1])
    plt.show()
        
def plot_sv(svd, sv=0):
    """
    Tool for plotting U and V^T sorted by a specified singular value

    Parameters:
            svd: A 3-ple containing the result of a SVD computed by 'pd_svd'
            sv: Integer indicating which singular value to sort by
    """
    fig, ax = plt.subplots(1, 2)
    _plot_mat_ax(svd[0].sort_values(by=sv), ax=ax[0])
    _plot_mat_ax(svd[2].sort_values(by=sv, axis=1), ax=ax[1])
    plt.show()
    #return plot_mat(svd[0].sort_values(by=sv)), plot_mat(svd[2].sort_values(by=sv, axis=1))
    
def svdfilter(svd, noise=[0]):
    """
    Tool for filtering a singular value and reconstructing a data set
    
    Parameters:
            svd: A 3-ple containing the result of a SVD
            noise: A list enumerating the singular values to set to 0

    Returns:
            Reconstruction of the filtered dataset as a NumPy array
    """
    #U, s, vt = svd
    U = svd[0].to_numpy()
    s = svd[1][0].to_numpy()
    vt = svd[2].to_numpy()
    for i in noise:
        s[i] = 0
    return U @ np.diag(s) @ vt

def _plotlines(data, ax, orient='wide'):
    if orient=='wide':
        ax.scatter(range(len(data)), data, c='red')
        ax.plot(range(len(data)), data, c='red')
        ax.scatter(range(len(data)), sorted(data), c='blue')
        ax.plot(range(len(data)), sorted(data), c='blue')
    elif orient=='square':
        ax.scatter(range(len(data)), data, c='red')
        ax.plot(range(len(data)), data, c='red')
        ax.scatter(range(len(data)), sorted(data), c='blue')
        ax.plot(range(len(data)), sorted(data), c='blue')
        ax.set_aspect('equal')
    else:
        ax.scatter(data, range(len(data)), c='red')
        ax.plot(data, range(len(data)), c='red')
        ax.scatter(sorted(data), range(len(data)), c='blue')
        ax.plot(sorted(data), range(len(data)), c='blue')


def lineplot_svs(svd, top=5):
    """
    Create lineplots of top singular values in U and V^T sorted and unsorted

    Parameters:
            svd: A 3-ple containing the result of a SVD
            top: Integer indicating which top singular values to include
    """
    svd = list(svd)
    if isinstance(svd[0], pd.DataFrame):
        svd[0] = np.array(svd[0])
        svd[2] = np.array(svd[2])
    topU = [svd[0][:,num] for num in range(top)]
    topvt = [svd[2][num,:] for num in range(top)]
    if len(svd[0]) > len(svd[0][0]): # if U has more columns than rows
        # vT will be wide
        fig, ax = plt.subplots(top, 2)
        for i, sv in enumerate(topU):
            ax[i][0].set_title('Column ' + str(i) + ' of U')
            _plotlines(sv, ax[i][0], orient='wide')
        for i, sv in enumerate(topvt):
            ax[i][1].set_title('Row ' + str(i) + ' of V-transpose')
            _plotlines(sv, ax[i][1])
    else:
        # U will be long
        fig, ax = plt.subplots(2, top)
        for i, sv in enumerate(topU):
            _plotlines(sv, ax[0][i], orient='long')
        for i, sv in enumerate(topvt):
            _plotlines(sv, ax[1][i])
    fig.tight_layout(pad=1.0)

def svd_overview(data, top=3, scale=True): #, sort=False):
    """
    Display original data with line plots of top singular values from V^T and U

    Parameters:
            data:   untransformed dataframe
            top:    top n singular values to plot
            scale:  Preprocess data before SVD (boolean)
    """
    sort= False
    bigw = 3
    bigh = 4
    fig, axs = plt.subplots(nrows=bigh + top, ncols=bigw + top)
    # get rid of plots we don't need
    for crap_array in axs[-top:,-top:]:
        for crap in crap_array:
            crap.remove()
    uaxs = []
    for i, lstrip_arr in enumerate(axs[:bigh,-top:].T):
        for lstrip in lstrip_arr:
            lstrip.remove()
        gs = axs[0, (i+bigw)].get_gridspec()
        uaxs.append(fig.add_subplot(gs[:bigh, (i+bigw)]))

    vtaxs = []
    for i, hstrip_arr in enumerate(axs[bigh:, :bigw]):
        for hstrip in hstrip_arr:
            hstrip.remove()
        gs = axs[(i+bigh), 0].get_gridspec()
        vtaxs.append(fig.add_subplot(gs[(i+bigh), :bigw]))

    for pane in axs[:bigh, :bigw]:
        for p in pane:
            p.remove()
    gs = axs[0,0].get_gridspec()
    dataxs = fig.add_subplot(gs[:bigh, :bigw])

    svd = pd_svd(data, scale=scale)
    if sort:
        exit(1)
    else:
        _plot_mat_ax(data, dataxs, cbar=False)
    topU = [svd[0].iloc[:,num] for num in range(top)]
    topvt = [svd[2].iloc[num,:] for num in range(top)]
    for i, vals in enumerate(topU):
        _plotlines(vals, uaxs[i], orient='long') 
    for i, vals in enumerate(topvt):
        _plotlines(vals, vtaxs[i], orient='wide')
    fig.tight_layout(pad=1)


if __name__=="__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', action='store', dest='filepath', help='path to file with tab separated numeric values')
    parser.add_argument('-d', '-delimiter', action='store', dest='delim', help='value separator (default is tab/indent)')
    parser.add_argument('-i', '--header', action='store_true', dest='header', help='use this flag if input file has a header row')
    parser.add_argument('--test', action='store_true', dest='testrun')
    args = parser.parse_args()
    #print(args)
    # if args.testrun:
    #     plot_mat(sort_by_top_value(svd_df(generate_synthetic_data())))
    #     exit(0)
    # if args.header:
    #     headerval = 'infer'
    # else:
    #     headerval = None
    # results = svd_fp(args.filepath, header=headerval, delim=args.delim)
    # plot_mat(sort_by_top_value(results))

# bigw = 3
# bigh = 4
# fig, axs = plt.subplots(nrows=bigh + top, ncols=bigw + top)
# # get rid of plots we don't need
# for crap_array in axs[-top:,-top:]:
#     for crap in crap_array:
#         crap.remove()
# uaxs = []
# for i, lstrip_arr in enumerate(axs[:bigh,-top:].T):
#     for lstrip in lstrip_arr:
#         lstrip.remove()
#     gs = axs[0, (i+bigw)].get_gridspec()
#     uaxs.append(fig.add_subplot(gs[:bigh, (i+bigw)]))

# vtaxs = []
# for i, hstrip_arr in enumerate(axs[bigh:, :top]):
#     for hstrip in hstrip_arr:
#         hstrip.remove()
#     gs = axs[(i+bigh), 0].get_gridspec()
#     vtaxs.append(fig.add_subplot(gs[(i+bigh), :top]))

# for pane in axs[:bigh, :bigw]:
#     for p in pane:
#         p.remove()
# gs = axs[0,0].get_gridspec()
# dataxs = fig.add_subplot(gs[:bigh, :bigw])
# svd = pd_svd(data, scale=scale)
# if sort:
#     exit(1)
# else:
#     _plot_mat_ax(data, dataxs)
#     topU = [svd[0][:,num] for num in range(top)]
#     topvt = [svd[2][num,:] for num in range(top)]
#     for i, vals in enumerate(topU):
#         _plotlines(vals, uaxs[i], orient='long') 
#     for i, vals in enumerate(topvt):
#         _plotlines(vals, vtaxs[i], orient='wide')
# fig.tight_layout(pad=1)