---
title: Submodular function maximization
date: \today
author: PGD
header-includes:
  - \usepackage{amsmath}
  - \DeclareMathOperator*{\argmax}{arg\,max}
  - \DeclareMathOperator*{\argmin}{arg\,min}
---

Let $V$ be a finite ground set, and let $f : \wp(V) \to
\mathbb{R}_+$ be a set function. Define $\Delta_f(e \mid S)$ for $S
\subseteq V$ as:

$$
\Delta_f(e \mid S) \triangleq f(S \cup \{e\}) - f(S).
$$

We call $\Delta_f$ the *discrete derivative*.

A set function $f$ is *submodular* if, for all $A \subseteq B \subseteq
V$ with $e \notin B$,

$$
\Delta_f(e \mid A) \geq \Delta_f(e \mid B).
$$

This captures the concept of diminishing returns.

A set function $f$ is *monotone* if, for every $A \subseteq B \subseteq
V$, $f(A) \leq f(B)$. Equivalently, $f$ is monotone if all its discrete
derivatives are non-negative, i.e., $\Delta_f(e \mid A) \geq 0$.

The class of *monotone submodular set functions* comprises those $f$ for
which, for all $A \subseteq B \subseteq V$ and $e \in V$,

$$
\Delta_f(e \mid A) \geq \Delta_f(e \mid B).
$$

Note that $e \notin B$ is no longer required. From now on, we assume $f$
is a fixed monotone submodular set function, accessed via an oracle.

The submodular maximization problem seeks to maximize $f$ under
constraints:

$$
\max_{S \subseteq V} f(S) \quad \text{subject to some constraints on } S.
$$

For a *cardinality constraint*, the problem becomes:

$$
\max_{S \subseteq V} f(S) \quad \text{subject to } |S| \leq k.
$$

Nemhauser, Wolsey, and Fisher (1978) proposed a greedy algorithm that
provides a $(1 - 1/e)$-approximation ($1 - 1/e \approx 63.2\%$). The algorithm works as follows:

- Start with $S_0 = \emptyset$.
- At iteration $i \geq 1$, add the element that maximizes the discrete
  derivative at $S_{i-1}$, $\Delta_f(e \mid S_{i-1})$:

$$
S_i = S_{i-1} \cup \{\argmax_e \Delta_f(e \mid S_{i-1})\}.
$$

Nemhauser and Wolsey (1978) proved that no algorithm can achieve an
approximation ratio better than $(1 - 1/e)$ using only polynomially many
function evaluations.

For the problem of finding the smallest set $S$ such that $f(S) \geq q$,
where $0 \leq q \leq f(V)$, the goal is:

$$
S^* = \argmin_S |S| \quad \text{subject to } f(S) \geq q.
$$

Here, the same greedy algorithm achieves a $(1 + \ln \max_{v \in V}
f(\{v\}))$-approximation.

For a non-uniform cost function $c(v) \geq 0$ for $v \in V$, we aim to
maximize $f$ under a budget constraint $B$:

$$
\max_S f(S) \quad \text{subject to } \sum_{v \in S} c(v) \leq B.
$$

This is known as a *knapsack constraint*. Ignoring costs in the greedy
algorithm can result in arbitrarily bad solutions.  However, by
considering the cost-benefit ratio, the algorithm can be modified to
guarantee a $(1 - 1/e)$-approximation:

$$
S_{i+1} = S_i \cup \left\{ \argmax_{v \in V \setminus S_i : c(v) \leq B - c(S_i)} \frac{\Delta_f(v \mid S_i)}{c(v)} \right\}.
$$

By enumerating all subsets $S$ of size 3 and augmenting them using the
cost-benefit greedy algorithm, the approximation guarantee can be
achieved.


\paragraph{Speeding up the greedy algorithm through lazy evaluations.}
In some applications, evaluating the function $f$ can be expensive. A
common optimization technique, known as *lazy evaluations*, reduces the
number of function evaluations required by leveraging the submodularity
property.

The key observation is that discrete derivatives $\Delta_f(e \mid S)$
decrease as $S$ grows due to diminishing returns. This allows us to use
priority queues to maintain a sorted order of candidate elements based
on their marginal gains, without reevaluating all candidates at every
iteration.

\clearpage

Outline of the greedy algorithm with lazy evaluations:

1. Start with an empty set $S = \emptyset$. Compute $\Delta_f(e \mid
   \emptyset)$ for all $e \in V$ and insert them into a max-priority
   queue $Q$, keyed by $\Delta_f(e \mid S)$.

2. At each step:
   - Extract the element $e$ with the highest marginal gain from $Q$.
   - Recompute $\Delta_f(e \mid S)$ based on the current set $S$.
   - If $e$ still has the highest marginal gain, add it to
     $S$. Otherwise, reinsert $e$ into $Q$ with its updated marginal
     gain and repeat.

By deferring recalculations for elements that are unlikely to be
selected (those not at the top of the queue), the algorithm
significantly reduces the number of evaluations. This lazy strategy is
particularly effective when $|V|$ is large and $f$ is computationally
expensive to evaluate.

The lazy greedy algorithm maintains the same theoretical guarantees as
the standard greedy algorithm, including the $(1 - 1/e)$-approximation
for monotone submodular maximization under a cardinality constraint.
