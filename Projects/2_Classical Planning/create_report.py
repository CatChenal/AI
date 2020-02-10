from pathlib import Path

import report as rpt
from display_figure import display_figure


#... constants .......................................
DIR_IMG = Path.cwd().joinpath('images')

DIR_DATA = Path.cwd().joinpath('data')
DATA_DIRS = [DIR_DATA.joinpath('raw'), DIR_DATA.joinpath('processed')]
    
problems = rpt.problems

fig1 = DIR_IMG.joinpath('p12_NewNodes_Actions.png')
fig2 = DIR_IMG.joinpath('p12_ElapsedSeconds_Actions.png')
fig3 = DIR_IMG.joinpath('p34_NewNodes_Actions.png')
fig4 = DIR_IMG.joinpath('p34_ElapsedSeconds_Actions.png')

#... reportparts .........................
title = """<div style="border-style: solid; border-width:thin; border-color: #4d0000; padding:40px;">
    <h1> Classical Planning Report</h1>
    <h3> Author: Cat Chenal</h3><div>"""

intro = """
<h1> Introduction</h1>
    <h2> Planning problems</h2>
    
    <p style="font-size:110%;">
        In this project, the planning problem is that of Air Cargo Transport: given some cargo, a plane, an origin, a destination, a start state, and a goal, we
        want to find a way to achieve the goal optimally or according to some search heuristics. Once we deal with multipicity in the parameters, the search space 
        of the possible actions to take become astronomical, hence infeasible even with a powerful computer. Thus, we rely on programming to implement a planning 
        search agent to solve the problem with different approaches.<br>
        The implementation relies on the Planning Domain Definition Language (PDDL), a framework that allows a planner to codify all the needed parameters using 
        first-order-logic:<br>
        <ul>
            <li>The initial (known) state: what has to be true in order to have a valid problem, e.g. at least one empty plane!</li>
            <li>The actions that are available in the state: e.g., [Un]LoadCargo, Fly, etc.</li>
            <li>The result of applying the action: e.g.: flying Plane1 to destination means no Plane1 at origin airport.</li>
            <li>The goal state: Cargo at destination.</li>
        </ul>
       <br>
       Several of two types of searches are implemented: Uninformed and Informed. Uninformed searches only know/check whether a given state is 
       the stated goal or not, while Informed searches employ a heuristic, or strategy, to ween out unacceptable states, and thus can apply to more complex problems.<br>
       <br>
       This report analyzes Project 2 of Udacity AI Nanodegree, in which the <code>my_planning_graph.py</code> module was completed with the required code.<br>
       After successful testing, the data files for all four air cargo problems was generated as tab-separated files using modifications of the existing code.<br>
        <ul>
            <li><code>run_report.py</code>: a copy of <code>run_search.py</code> that uses a modified <code>main()</code> function</li>
            <li><code>_utils.run_search_rpt()</code>: a new function that changes the output of <code>_utils.run_search()</code></li>
        </ul>
        This report will answer three questions:
        <ol>
            <li>Which algorithm or algorithms would be most appropriate for planning in a very restricted domain (i.e., one that has only a few actions) and needs to operate in real time?</li>
            <li>Which algorithm or algorithms would be most appropriate for planning in very large domains (e.g., planning delivery routes for all UPS drivers in the U.S. on a given day)?</li>
            <li>Which algorithm or algorithms would be most appropriate for planning problems where it is important to find only optimal plans?</li>
        </ol>
</p>
"""

p34_intro = """
<h2>Air cargo problems 3 and 4:</h2>
   <p style="font-size:110%;">
    After elimination of problems 3, 8, and 10, the searches performed on both Problems 3 & 4 were the following<br>
    (with the number corresponds to the number passed to `run_report.py` in the -s argument):
    </p>
    <pre> 
      <b>Uninformed searches </b>
        1: breadth_first_search
        2: depth_first_graph_search
      <b>Informed searches with two different heuristics </b>
        4: greedy_best_first_graph_search + h_unmet_goals
        5: greedy_best_first_graph_search + h_pg_levelsum
        6: greedy_best_first_graph_search + h_pg_maxlevel
        7: greedy_best_first_graph_search + h_pg_setlevel
        9: astar_search + h_pg_levelsum
        11: <mark>astar_search + h_pg_setlevel</mark>
    </pre>
    <p style="font-size:110%;">
      Note: Search <mark>11</mark> was aborted on both problems due to excessive run time (> 1 hour).<br>
      The raw data files were generated at the comman line using the `run_report.py` module, 
      which is a copy of the original `run_search.py` module with modifications on output string formats. 
      Note that `_utils.py.run_search` was amended accordingly.
    </p>
"""

complexities = """<h1>* Complexity differences</h1>
    <p style="font-size:110%;">There is only one order of magnitude difference in the number 
    of Actions between Problem 2 and Problem 1 (72 vs. 20), but this yields multiple orders 
    of magnitude differences for both New Nodes and Search Time.</p>
"""

#.... Answers ..................................         
answers = """
<h3>* Anwers to questions</h3>
<blockquote class="w3-panel w3-leftbar w3-light-grey">
<strong>Question 1:</strong>
<p style="font-size:110%;">
Which algorithm(s) would be most appropriate for planning in a very restricted domain
(i.e., one that has only a few actions) and needs to operate in real time?
</p>
</blockquote>
<blockquote class="w3-panel w3-leftbar w3-light-grey">
<strong>&#187; Answer:</strong>
<p style="font-size:110%;">
A domain with few actions would be like Problem 1. All search algorithms would be appropriate in this case as they all performed under 1 second.
</p>
</blockquote>
<blockquote class="w3-panel w3-leftbar w3-light-grey">
<strong>Question 2:</strong>
<p style="font-size:110%;">
Which algorithm or algorithms would be most appropriate for planning in very large domains 
(e.g., planning delivery routes for all UPS drivers in the U.S. on a given day.)
</p>
</blockquote>
<blockquote class="w3-panel w3-leftbar w3-light-grey">
<strong>&#187; Answer:</strong>
<p style="font-size:110%;">
For problems with more than 100 and with a search time restricted to under 1 second, algorithm <b>4</b>: <i>greedy_best_first_graph_search h_unmet_goals</i> would be the best.
</p>
</blockquote>
<blockquote class="w3-panel w3-leftbar w3-light-grey">
<strong>Question 3:</strong>
<p style="font-size:110%;">
Which algorithm(s) would be most appropriate for planning problems where it is important to find only optimal plans?
</p>
</blockquote>
<blockquote class="w3-panel w3-leftbar w3-light-grey">
<strong>&#187; Answer:</strong>
<p style="font-size:110%;">
The algorithms that guarantee to find the shortest path and are thus optimal are: <b>1</b>: <i>breadth_first_search</i> and <b>3</b>: <i>uniform_cost_search</i>.
</p>
</blockquote>
"""
#... fig display ............................................
style_dict = {'div': {'width': 7},
              'figure': {'display':'inline-block', 'text-align':'left'},
              'image': {'display':'block', 'width': 600, 'height':500},
              'caption': {'color':'teal','font-weight':'bold', 'font-family': 'Arial, Helvetica, sans-serif'}
             }

caption1_dict = {'number': 1,
                'caption': 'NewNodes expanded in each search function for Problems 1 and 2 (log scale).'}

caption2_dict = {'number': 2,
                'caption': 'ElapsedSeconds in each search function for Problems 1 and 2.'}

cap3 = """NewNodes expanded in each search function for Problems 3 and 4.<br>
<pre>         <mark>Search 11, A* with setlevel heuristic</mark>: aborted after 1 hour.<pre>"""
caption3_dict = {'number': 3, 'caption': cap3}

cap4 = """Elapsed minutes in each search function for Problems 1 and 2.<br>
<pre>         <mark>Search 11, A* with setlevel heuristic</mark>: aborted after 1 hour.<pre>"""
caption4_dict = {'number': 4, 'caption': cap4}


#... dataframes .......................................
specs = rpt.specs

redo = False
df1 = rpt.get_problem_data_df('prob_1', problems[0], 
                              DATA_DIRS[0], DATA_DIRS[1], file_as_tsv=True, replace=redo)
df2 = rpt.get_problem_data_df('prob_2', problems[1], 
                              DATA_DIRS[0], DATA_DIRS[1], file_as_tsv=True, replace=redo)

df3 = rpt.get_problem_data_df('prob_3', problems[2], 
                              DATA_DIRS[0], DATA_DIRS[1], file_as_tsv=True, replace=redo)
df4 = rpt.get_problem_data_df('prob_4', problems[3], 
                              DATA_DIRS[0], DATA_DIRS[1], file_as_tsv=True, replace=redo)

dfa = rpt.concat_all_dfs([df1, df2, df3, df4])

# ... analysis functions ..........................................
def analyze_12():
    specs_ml = specs[specs.columns[1:]].to_html(index=False, justify='center')
    replace_str1 = ' style="text-align: center;"'
    replace_str2 = 'class="dataframe"'
    specs_ml = specs_ml.replace(replace_str1, '')
    specs_ml = specs_ml.replace(replace_str2, replace_str1) #replace_str2+replace_str1)

    analysis = f"""
        <h1>Analysis of the output of Problems 1 and 2 </h1>
        <p style="font-size:110%;">
            All four problems differ by the number of nodes, cargo loads, airports, and specificity of goals. 
            The Complexity column holds a problem's total number of parameters:<br>
            <pre>
                {specs_ml}
            </pre>

            The first two problems are the less complex and are used to decide on the appropriate choices of search 
            functions and heuristic on more "real life" problems (Problems 3 and 4).<br>
            The analysis relies on three charts:
            <ul>
                <li> Number of nodes expanded against number of actions in the domain</li>
                <li> Search time against the number of actions in the domain</li>
                <li> Length of the plans returned by each algorithm on all search problems</li>
            </ul>
        </p>
    """
    return analysis
#        </p>
#        <p style="font-size:110%;">

analysis_12 = analyze_12()

candidates = rpt.get_elim_candidates(df2, df1)
insights = rpt.paragraph_p12(candidates, return_html=True)

dbl_tbl, dbl_para, df_dbl = rpt.plans_length(dfa, 'double')
sgl_tbl, sgl_para, df_sgl = rpt.plans_length(dfa, 'single')

tbls_html = """<div style="float:left; width:100%; padding:1px;">
      <div style="float:left; width:50%; padding:2px;">
        {}
       </div>
      <div style="float:left; width:50%; padding:2px;">
        {}
      </div>
    </div>"""
tables_in_row = tbls_html.format(dbl_tbl, sgl_tbl)


#... write report functions ...................................
report_parts = [title, intro, analysis_12, complexities, insights, 
                p34_intro, tables_in_row, dbl_para, sgl_para,
                answers]

def html_fig(num):
    if num == 1:
        return display_figure(fig1, style_dict, caption1_dict, img_title='NewNodes')
    elif num == 2:
        return display_figure(fig2, style_dict, caption2_dict, img_title='Seconds')
    elif num == 3:
        return display_figure(fig3, style_dict, caption3_dict, img_title='NewNodes')
    elif num == 4:
        return display_figure(fig4, style_dict, caption4_dict, img_title='Minutes')
    else:
        pass
    