<div style="{width: 80%}"><div style="border-style: solid; border-width:thin; border-color: #4d0000; padding:40px;">
    <h1> Classical Planning Report</h1>
    <h3> Author: Cat Chenal</h3><div></div>


<div style="{width: 80%}">
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
</div>

<div style="{width: 80%}">
        <h1>Analysis of the output of Problems 1 and 2 </h1>
        <p style="font-size:110%;">
            All four problems differ by the number of nodes, cargo loads, airports, and specificity of goals. 
            The Complexity column holds a problem's total number of parameters:<br>
            <pre>
                <table border="1"  style="text-align: center;">
  <thead>
    <tr>
      <th>Air cargo problem</th>
      <th>Cargos</th>
      <th>Planes</th>
      <th>Airports</th>
      <th>Goal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>4</td>
      <td>4</td>
    </tr>
    <tr>
      <td>4</td>
      <td>5</td>
      <td>2</td>
      <td>4</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
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
    </div>



<div style="{width: 80%}"><h1>* Complexity differences</h1>
    <p style="font-size:110%;">There is only one order of magnitude difference in the number 
    of Actions between Problem 2 and Problem 1 (72 vs. 20), but this yields multiple orders 
    of magnitude differences for both New Nodes and Search Time.</p>
</div>

<div style="{width: 80%}">
      <figure style="display:inline-block;text-align:left;">
      <img src="C:\Users\catch\Documents\GitHub\AI\Projects\2_Classical Planning\images\p12_NewNodes_Actions.png" 
         alt="x"
         style="display:block;width:600;height:500;"
         title="NewNodes"
      >
      <figcaption style="color:teal;font-weight:bold;font-family:Arial, Helvetica, sans-serif;">
         Figure 1 - NewNodes expanded in each search function for Problems 1 and 2 (log scale).
      </figcaption>
    </figure>
    </div>

<div style="{width: 80%}">
      <figure style="display:inline-block;text-align:left;">
      <img src="C:\Users\catch\Documents\GitHub\AI\Projects\2_Classical Planning\images\p12_ElapsedSeconds_Actions.png" 
         alt="x"
         style="display:block;width:600;height:500;"
         title="Seconds"
      >
      <figcaption style="color:teal;font-weight:bold;font-family:Arial, Helvetica, sans-serif;">
         Figure 2 - ElapsedSeconds in each search function for Problems 1 and 2.
      </figcaption>
    </figure>
    </div>






<div style="{width: 80%}"><h3>* Insights from Problems 1 and 2</h3><p style="font-size:110%;">On the basis of Figures 1 and 2, which show the number of new nodes created, 
    and the time spent by each search function, respectively, the searches that are candidates 
    for elimination for more complex problems are those at the intersection of the average-ranked 
    costliest sets viz new nodes creation and search time.<br>These searches are:</p><pre><dl><dl><dt><b>10: astar_search h_pg_maxlevel</b></dt><dt><b> 8: astar_search h_unmet_goals</b></dt><dt><b> 3: uniform_cost_search</b></dt></dl></p></pre></div>


<div style="{width: 80%}">
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
</div>

<div style="{width: 80%}">
      <figure style="display:inline-block;text-align:left;">
      <img src="C:\Users\catch\Documents\GitHub\AI\Projects\2_Classical Planning\images\p34_NewNodes_Actions.png" 
         alt="x"
         style="display:block;width:600;height:500;"
         title="NewNodes"
      >
      <figcaption style="color:teal;font-weight:bold;font-family:Arial, Helvetica, sans-serif;">
         Figure 3 - NewNodes expanded in each search function for Problems 3 and 4.<br>
<pre>         <mark>Search 11, A* with setlevel heuristic</mark>: aborted after 1 hour.<pre>
      </figcaption>
    </figure>
    </div>

<div style="{width: 80%}">
      <figure style="display:inline-block;text-align:left;">
      <img src="C:\Users\catch\Documents\GitHub\AI\Projects\2_Classical Planning\images\p34_ElapsedSeconds_Actions.png" 
         alt="x"
         style="display:block;width:600;height:500;"
         title="Minutes"
      >
      <figcaption style="color:teal;font-weight:bold;font-family:Arial, Helvetica, sans-serif;">
         Figure 4 - Elapsed minutes in each search function for Problems 1 and 2.<br>
<pre>         <mark>Search 11, A* with setlevel heuristic</mark>: aborted after 1 hour.<pre>
      </figcaption>
    </figure>
    </div>

<div style="{width: 80%}"><div style="float:left; width:100%; padding:1px;">
      <div style="float:left; width:50%; padding:2px;">
        <table border="1"  style="text-align: center;">
  <thead>
    <tr>
      <th>Search function</th>
      <th>Frequency where PlanLength &gt;=10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>greedy_best_first_graph_search</td>
      <td>8</td>
    </tr>
    <tr>
      <td>depth_first_graph_search</td>
      <td>4</td>
    </tr>
    <tr>
      <td>breadth_first_search</td>
      <td>2</td>
    </tr>
    <tr>
      <td>astar_search</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
       </div>
      <div style="float:left; width:50%; padding:2px;">
        <table border="1"  style="text-align: center;">
  <thead>
    <tr>
      <th>Search function</th>
      <th>Frequency where PlanLength &lt;10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>greedy_best_first_graph_search</td>
      <td>8</td>
    </tr>
    <tr>
      <td>astar_search</td>
      <td>8</td>
    </tr>
    <tr>
      <td>uniform_cost_search</td>
      <td>2</td>
    </tr>
    <tr>
      <td>breadth_first_search</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
      </div>
    </div></div>


<div style="{width: 80%}">Out of 36 completed searches, 44% (16), have double-digit or longer PlanLength.<br>In that subset, 12 (75%) involve the search functions `greedy_best_first_graph_search` and `depth_first_graph_search`. And this occurs for all Problems.<br></div>


<div style="{width: 80%}">Out of 36 completed searches, 56% (20), have single-digit or longer PlanLength.<br>In that subset, 16 (80%) involve the search functions `greedy_best_first_graph_search` and `astar_search`. And this occurs only for Problems: 2,1.<br><br></div>


<div style="{width: 80%}">
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
</div>


