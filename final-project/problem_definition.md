# TSDAP
## Time Dependent Activity Scheduling Problem

$\tau_i(t_i)$ is the time required to complete activity $i$ at time $t_i$.  
$e_i, l_i$ are the earliest start time and latest end time of activity $i$.  
$\rho_i(t_i)$ is the resource consumption of activity $i$ at time $t_i$.  
$Q$ is the total resource capacity  
$\theta_i(t_i) = t_i + \tau_i(t_i)$ is the completion time function.  

Minimize
$$\min_{t_j} \theta_n(t_n) = \min_{t_j} t_n + \tau_n(t_n)$$

subject to
$$\theta_i(t_i) \le t_{i+1}$$
$$\sum_{i=1}^{n} \rho_i(t_i) \le Q$$
$$t_i \in [e_i, l_i]$$

We assume the FIFO property: $\theta_i(t) \le \theta_i(t')$ if $t \le t'$

## Solve TSDAP

$V_i = \{e_i, e_i + \epsilon, ..., l_i \}$ set of vertices for activity $i$  
$V = V_1 \cup ... \cup V_n$  
$q_{(i,t)} = \rho_i(t)$  
$l_{(i,t)}$ cumulative resource consumption prior to starting activity $i$ at time $t_i$.  
$W = \{(i, t) \in V \setminus \bar V \; | \; l_{(i, t)} + q_{(i,t)} \le Q\}$ set of still available vertices.


![](algorithm_1.png)

### Implemented solution

The implemented algorithm differs from the one described in the paper by using a MinHeap to store the vertexes $W$ instead of a sorted list. This choice was made by analyzing the time complexity of the two algorithms, with the sorted list implementation taking time $O(n^2m^2)$ to keep it sorted, while the MinHeap implementation takes time $O(nm\log(mn)) = O(nm)$ when $n=am$ for $a>0$ which is the case in the article. This enhanced version of the algorithm, has also been discussed with the authors of the paper, who agree on the complexity.  