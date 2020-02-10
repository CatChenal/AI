import numpy as np
import pandas as pd
from pathlib import Path

import matplotlib as mpl
from matplotlib import pyplot as plt
plt.style.use('seaborn-muted')

#from IPython import get_ipython
from IPython.display import HTML, Markdown

import air_cargo_problems as acp


problems = ['Air Cargo Problem 1', 
            'Air Cargo Problem 2',
            'Air Cargo Problem 3',
            'Air Cargo Problem 4']

SEARCHES = ['breadth_first_search',
            'depth_first_graph_search',
            'uniform_cost_search',
            'greedy_best_first_graph_search h_unmet_goals',
            'greedy_best_first_graph_search h_pg_levelsum',
            'greedy_best_first_graph_search h_pg_maxlevel',
            'greedy_best_first_graph_search h_pg_setlevel',
            'astar_search h_unmet_goals',
            'astar_search h_pg_levelsum',
            'astar_search h_pg_maxlevel',
            'astar_search h_pg_setlevel']


def get_prob_specs():
    Probs = [acp.air_cargo_p1(), acp.air_cargo_p2(),
             acp.air_cargo_p3(), acp.air_cargo_p4()]

    problems_specs = {'Problem': [name for name in problems],
                      'Air cargo problem': [i+1 for i in range(len(problems))],
                      'Cargos': [len(p.cargos) for p in Probs],
                      'Planes': [len(p.planes) for p in Probs],
                      'Airports': [len(p.airports) for p in Probs],
                      'Goal': [len(p.goal) for p in Probs]}
    return pd.DataFrame(problems_specs)

specs = get_prob_specs()


def df2tsv(df, fname, replace=False):
    if Path(fname).exists():
        if replace:
            df.to_csv(fname, sep='\t')
        #else:
        #    print(f'File {fname} not replaced.')
        return
    
    df.to_csv(fname, sep='\t')
    return


def get_problem_data_df(file_stem, problem, raw_dir, out_dir, file_as_tsv=False, replace=False):
    """
    Combine all processed files of a problem found in Path(data_dir) with given stem.
    The file to be saved to/retrieved from out_dir is passed in file_as_tsv, tab separated csv.
    
    Input example:
    file_stem = 'prob_2'
    problem = 'Air Cargo Problem 2'
    Output: a dataframe, saved to tsv if file_as_tsv=True and not replace; saved as file_stem+'_df.csv'.
    """
    if file_stem is None or problem is None:
        print('file_stem and problem must have a value.')
        return
    
    t = '\t'
    
    # input/output file suffixes:
    sfx = ['.csv', '_df.csv']
    
    # Try retrieving it from out_dir if not replacing it:
    fout = None
    if file_as_tsv:
        fout = Path(out_dir).joinpath(file_stem + sfx[1])
        if fout.exists() and not replace:
            df = pd.read_csv(fout, sep=t)
            try:
                return df.drop('Unnamed: 0', axis=1)
            except KeyError:
                pass
    # else: (re)process
    
    pfiles = list(Path(raw_dir).glob(file_stem + '*'))
    if len(pfiles) == 0:
        print(f'No raw files with stem: {file_stem}')
        return
    
    dflist = []
    for f in pfiles:
        df, err = get_results_df(f, problem)
        
        if df is not None:
            df = df.merge(specs)
            df['index'] = df['Searcher'].apply(lambda x: SEARCHES.index(x)+1)
            df['index'] = df['index'].astype(int)
            df.set_index('index', drop=True, inplace=True)
            
            dflist.append(df)
            del df
        else:
            print(f'Error from get_results_df:\n\t{err}')
        
    dfout = pd.concat(dflist, ignore_index=False)
    dfout.sort_index(inplace=True)
    
    if file_as_tsv:
        df2tsv(dfout, fout, replace=replace)
    
    return dfout


def get_results_df(fname, problem):
    """Process csv into dataframe.
    """
    t = '\t'
    
    # Cols to add:
    val_cols = ['Actions','Expansions','GoalTests','NewNodes','PlanLength','ElapsedSeconds']
    err = ''
    df = pd.read_csv(fname, sep=t)
    if df.shape[0] < len(val_cols):
        err = f'Data for {fname.name} is incomplete.'
        return None, err
    
    # Rename cols: c (temp) -> Searcher
    df.columns = ['c', 'Searcher']
    # Add new cols & reindex
    df = df.reindex(columns = df.columns.tolist() + val_cols)
    
    # Populate new cols according to row with search name:
    sr = df.loc[df.c == 'Searcher', 'Searcher'] 
    for (idx, sr_row) in sr.items():
        j = idx
        for c in df.columns[2:].tolist():
            j += 1
            if c == 'ElapsedSeconds':
                df.loc[idx, c] = float(df.loc[j, 'Searcher'])
            else:
                df.loc[idx, c] = int(df.loc[j, 'Searcher'])

    df.dropna(inplace=True)
    # Add a minute column:
    df['Minutes'] = np.round(df.ElapsedSeconds/60, 3)
    
    # Replace values of 1st col with problem name & update col name:
    df['c'] = problem
    df.rename(columns={'c': 'Problem'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df, ''


def concat_all_dfs(dflist):
    """
    Output combined df for complete runs, Actions>0.
    """
    dfall = pd.concat(dflist, ignore_index=False)
    dfall.reset_index(drop=False, inplace=True)
    dfall.rename(columns={'index': 'id'}, inplace=True)
    # reduced
    drop_cols = dfall.columns[-4:-1].tolist() + ['Problem','Minutes','GoalTests']
    dfa = dfall.drop(drop_cols, axis=1)
    del dfall
    # add col for function name
    dfa['search_fn'] = dfa.Searcher.str.partition(' ')[0]
    # reorder cols
    dfa = dfa[['Air cargo problem','id','search_fn','Searcher','Actions',
               'PlanLength', 'NewNodes','Expansions','ElapsedSeconds']]

    # complete runs only:
    return dfa[dfa['Actions'].values > 0]


def plans_length(dfa, which):
    """
    dfa: frame of concatenated df1 to df4.
    Analysis of plan length for which in ['double', 'single']:
    PlanLength is double(single)-digit.
    """
    if which == 'double':
        msk = dfa.PlanLength >= 10
        col2 = 'Frequency where PlanLength >=10'
    else:
        msk = dfa.PlanLength < 10
        col2 = 'Frequency where PlanLength <10'
        
    dfa_rows = dfa.shape[0]
    
    dfout = dfa[msk].sort_values(['PlanLength'], ascending=False)

    uniq_probs = dfout['Air cargo problem'].unique()
    n_plans = dfout.shape[0]
    searcher_cnt = dfout['Searcher'].value_counts()
    fn_cnt = dfout['search_fn'].value_counts()

    # get the html string:
    df_fn = fn_cnt.to_frame()
    df_fn.reset_index(drop=False, inplace=True)
    df_fn.columns = ['Search function', col2]
    
    df_fn_html = df_fn.to_html(index=False, justify='center')
    replace_str1 = ' style="text-align: center;"'
    replace_str2 = 'class="dataframe"'
    df_fn_html = df_fn_html.replace(replace_str1, '')
    df_fn_html = df_fn_html.replace(replace_str2, replace_str1)

    pct_plans = n_plans/dfa_rows
    top2_fn = fn_cnt[0:2].sum()
    pct_top2_fn = top2_fn/n_plans

    text = f"Out of {dfa_rows} completed searches, {pct_plans:.0%} ({n_plans}), have {which}-digit or longer PlanLength.<br>"
    text += f"In that subset, {top2_fn:d} ({pct_top2_fn:.0%}) involve the search functions `{fn_cnt.index[0]}` and `{fn_cnt.index[1]}`."
    if len(uniq_probs) < 4:
        text += " And this occurs only for Problems: "
        pro = ",".join('{}' for p in uniq_probs) +'.<br>'
        text += pro.format(*uniq_probs)
    else:
        text += " And this occurs for all Problems."
    text += "<br>"
    
    return df_fn_html, text, dfout

def make_bar_plots(df_list,
                   x_col, y_col,
                   problems,
                   legend_bbox=(.05, .95),
                   to_file='',
                   show=False,
                   excluded=None):
    """
    To get 2 bar plots in a row.
    """ 
    import matplotlib.patches as mpatches

    def despine(ax):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    a1 = df_list[0][x_col].unique().astype(int)
    a1 = a1[a1>0]
    a2 = df_list[1][x_col].unique().astype(int)
    a2 = a2[a2>0]
    assert len(a1) == len(a2) == 1
    
    action_nums = [a1[0], a2[0]]
    
    p1 = df_list[0]['Air cargo problem'].iloc[0]
    p2 = df_list[1]['Air cargo problem'].iloc[0]
    
    # Seach functions names should be common to all dfs:
    search = df_list[0].Searcher.tolist()
    
    # Sample cmap according to categories:
    s_len = len(search)
    cmap = plt.get_cmap('viridis')
    m = cmap.N // s_len
    colors = [cmap.colors[i*m] for i in range(s_len)]
    
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
    
    # Use the minutes columns for the more complex problems:
    if y_col == 'ElapsedSeconds':
        ty_col = 'Elapsed time'
        if p1 == 3 or p == 4:  # applies to problems 3/4
            y_col = 'Minutes'
    else:
        ty_col = y_col
                
    plt.title(f'{ty_col} vs. {x_col} for Problems {p1} & {p2}',
                 y = 1.05, fontsize=14)

    for i, df in enumerate(df_list):
        ylog = False
        ylab = f'{y_col}'
        # log scale on NewNodes for df2, df3, df4:
        if (i == 1 or p1 == 3) and y_col == 'NewNodes':
            ylog = True
            ylab += ' (log)'
        
        axs[i].set_ylabel(ylab, fontsize=12)

        df[y_col].plot.bar(ax=axs[i], logy=ylog,
                           color=colors,
                           legend=False)
        
        t = '{}, {} = {:d}'.format(problems[i], x_col, action_nums[i])
        axs[i].set_xlabel(t, fontsize=12)
        axs[i].set_xticks([])
        despine(axs[i])

    legt = 'Searchers'
    new_lgd = p1 == 3 and excluded is not None
    if new_lgd:
        # Modify the legend to indicate excluded searches
        # (bc colormap is identical to fig1/2, but some runs have no data).
        legt += ' (X :: excluded)'
        excluded_len = len(excluded)
        x_idx = [excluded[i][0]-1 for i in range(excluded_len)]
    
    legend_patches = []  
    for i, c in enumerate(colors):
        lab = search[i]
        if new_lgd:
            if SEARCHES.index(lab) in x_idx:
                lab = lab.replace(' ', ' + ')
                lab += ' X'
            else:
                lab = lab.replace(' ', ' + ')
        else:
            lab = lab.replace(' ', ' + ')

        legend_patches.append(mpatches.Patch(color=c, label=lab))
       
    axs[1].legend(handles=legend_patches,
                  title=legt,
                  title_fontsize='14',
                  fontsize='medium', 
                  bbox_to_anchor=legend_bbox, 
                  loc='upper left',
                  labelspacing=0.6,
                  fancybox=True)

    plt.tight_layout()
    
    if to_file:
        plt.savefig(to_file)
    
    if show:
        return axs


def format_multiples(multi):
    s = ''
    for i in range(len(multi)):
        s += '{'+ str(i) +':s}, '
    s = s[:-2]
    return '[' + s.format(*multi.values) + ']'


def order_analysis(df2, df1, column_to_compare):
    """
    df2: has the large values.
    """
    colA_larger_values = df2[column_to_compare]
    colA_smaller_values = df1[column_to_compare]

    # orders of magnitude difference btw dfB and dfA (min, max):
    mag = np.round(np.log(colA_larger_values/colA_smaller_values), 0)
    mag.sort_values(ascending=False, inplace=True)
    mag_aver = int(np.round(mag.mean(), 0))

    # get the indices of values above average:
    ma = mag[mag > mag_aver].index.tolist()
    
    # get the names of all searchers corresponding to the ma:
    above_multiples = (mag_aver, df2.loc[ma, 'Searcher'])
    return above_multiples


def comparison_paragraph(df2, df1, heading, column_to_compare, return_html=False):

    p1 = df1.loc[0,'Problem'][-1]
    p2 = df2.loc[0,'Problem'][-1]
    
    order_aver, searches_above = order_analysis(df2, df1, column_to_compare)
    above = format_multiples(searches_above)
    
    headinglc = heading.lower()
    text = f"""<h3>* {heading}</h3><p style="font-size:110%;">For Problems {p1} and {p2}, """
    text += f"the <i>average</i> order of magnitude difference in {headinglc} is "
    text += f"<b>{order_aver:d}</b>, which is surpassed by these searches: {above}.</p>"

    if return_html:
        return text
    else:
        return Markdown(text)


def get_elim_candidates(df2, df1):
    """
    For the analysis of problems 1 & 2. 
    List the costliest searches: candidates for elimination on more complex problems.
    """
    if df1.loc[1,'Problem']!= problems[0]:
        return
    
    nodes_order_av, nodes_above = order_analysis(df2, df1, 'NewNodes')
    time_order_av, time_above = order_analysis(df2, df1, 'ElapsedSeconds')
    elim_candidates = set(nodes_above[:nodes_order_av]).intersection(set(time_above[:time_order_av]))
    # return their 1-base index also:
    out = [(SEARCHES.index(c)+1, c) for c in elim_candidates]
    return out

    
def paragraph_p12(candidates_tup, return_html=False):
    """
    For displaying the analysis of problems 1 & 2.
    """

    elim_list = ""
    for i, c in candidates_tup:
        elim_list += f"<dt><b>{i:>2}: {c}</b></dt>"
        
    text = """<h3>* Insights from Problems 1 and 2</h3><p style="font-size:110%;">"""
    text += """On the basis of Figures 1 and 2, which show the number of new nodes created, 
    and the time spent by each search function, respectively, the searches that are candidates 
    for elimination for more complex problems are those at the intersection of the average-ranked 
    costliest sets viz new nodes creation and search time.<br>These searches are:</p><pre><dl>"""
    text += f"<dl>{elim_list}</dl></p></pre>"
    
    if return_html:
        return text
    else:
        return Markdown(text)  

    
def add_div_around_html(div_html_text, output_string=False, div_style="{width: 80%}"):
    """
    Wrap an html code str inside a div.
    div_style: whatever follows style= within the <div>
    
    Behaviour with `output_string=True`:
    The cell is overwritten with the output string (but the cell mode is still in 'code' not 'markdown')
    The only thing to do is change the cell mode to Markdown.
    If `output_string=False`, the HTML/md output is displayed in an output cell.
    """
    div = f"""<div style="{div_style}">{div_html_text}</div>"""
    if output_string:
        return div
        #get_ipython().set_next_input(div, 'markdown')
    else:
        return Markdown(div)