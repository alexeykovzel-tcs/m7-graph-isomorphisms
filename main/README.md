# How to run?

in main.py, write the names of the files that you want to test and which basic operations to apply (GI, Aut, GIAut). The files should be located in the same directory as main.py.

Moreover, in graph_iso.py, you can switch between basic and fast color refinements, whether to apply preprocessing (trees/forests and false tweens) by changing the corresponding boolean variables at the top of the file.

# Project Structure

| file name         | description                                        |
| ----------------- | -------------------------------------------------- |
| color_ref_fast.py | color refinement with DFA minimization             |
| color_ref.py      | basic color refinement                             |
| color.py          | color-related classes such as Color and ColorGroup |
| graph_io.py       | utils for reading / writing graphs                 |
| graph_iso.py      | algorithm for finding and counting isomorphisms    |
| graph.py          | Graph, Vertex, Edge classes                        |
| basic.py          | basic functionality (GI, Aut, GIAut)               |