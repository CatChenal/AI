# A crypto-arithmetics Z3-solver class  

This is a side-project that takes on the *Cryptarithmetic Challenges* described in the notebook on [Constraint Satisfaction](AIND-Constraint_Satisfaction.ipynb).

I created a class that takes a crypto-arithmetric puzzle as a string, and output a possible solution (if any) as determined by the constraint satisfaction tool called [Z3](https://github.com/Z3Prover/z3) from Microsoft Research.

As per the [Exercises README](README.md):  
>There are many different kinds of CSP solvers available for CSPs. Z3 is a "Satisfiability Modulo Theories" (SMT) solver, which means that unlike the backtracking and variable assignment heuristics discussed in lecture, Z3 first converts CSPs to satisfiability problems then uses a [boolean satisfiability](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem) (SAT) solver to determine feasibility. Z3 includes a number of efficient solver algorithms primarily developed to perform formal program verification, but it can also be used on general CSPs. Google's [OR tools](https://developers.google.com/optimization/) includes a CSP solver using backtracking with specialized subroutines for some common CP domains.


## 1. Crypto-arithmetic (CA) puzzles

These puzzles typically add two or more words together and indicate the total with another word. Below, are just a few examples or the starting puzzles and their solutions:  
```
  T W O  :    9 3 8
+ T W O  :  + 9 3 8
-------  :  -------
F O U R  :  1 8 7 6
```

```
```

## 2. CA Input format  

A CA string follows this format: `"WORD + WORD + WORD [+...] == TOTAL_WORD"`, where each WORD is not necessarily the same.

## 3. Anatomy of the CA_Z3_solver class

## 4. Testing the class


## x. Operation extension  
:TODO:
I pan to extend the operation on words in the puzzle to multiplication.  
Phase 1: Limit to two words.
Phase 2: Add one, then a few more...
Phase 3: Can the class handle an arbitrary number of multiplicands (?)