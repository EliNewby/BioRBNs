# BioRBNs
Repository to create random networks with structures emulating biological networks and to populate these networks with a dynamical model of Boolean read-once-functions [1].

## Installation
This code functions best in an anaconda environment with these versions:
- Python 3.8.10

## Functions
### buildNetwork
The buildNetworks.py file contains the function `buildNetwork`, which takes a given network size and generates a networkx DiGraph that resembles a biological network. That is, it has a power law out-degree distribution and a Poisson in-degree distribution [2].

### generateRulesets
The generateROFRulesets.py file contains the function `generateRulesets` along with a helper function. The function takes an input networkx DiGraph (with Boolean edge attribute 'negative' to indicate if an edge is a negative edge) and writes 'numRulesets' Boolean rule-sets to a directory that is specified by the user in the Booleannet file format.

## References
[1] Eli Newby, Jorge Gómez Tejeda Zañudo, Réka Albert; Structure-based approach to identify driver nodes in ensembles of biologically inspired Boolean networks. *Phys. Rev. Res.* Jul 2023; 5 (3):033009

[2] Claus Kadelka, Taras-Michael Butrie, Evan Hilton, Jack Kinseth, Addison Schmidt, and Haris Serdarevic, A Meta-Analysis of Boolean Network Models Reveals Design Principles of Gene Regulatory Networksm arXiv:2009.01216.

[3] Ajay Subbaroyan, Olivier C Martin, Areejit Samal, Minimum complexity drives regulatory logic in Boolean models of living systems, *PNAS Nexus*, Volume 1, Issue 1, March 2022, pgac017,
