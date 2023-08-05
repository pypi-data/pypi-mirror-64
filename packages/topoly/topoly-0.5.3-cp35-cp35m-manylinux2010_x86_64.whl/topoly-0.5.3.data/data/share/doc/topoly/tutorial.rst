.. _tutorial:

***************
Tutorial
***************
All examples are taken from topoly_test package available at github. Here is
presented usage of all functions in our package. For more information look into
our `documentation <https://topoly.cent.uw.edu.pl/documentation.html>`_.

Whatever you want to do start with importing topoly functions::

    from topoly import *


Knot, link, theta-curve and handcuff type identification (invariants calculation)      
============================================================================
Checking knot type using knot invariants. Here we have two structures: .xyz 
with true knot and .pdb protein structure with probabilistic knot. We can pass
such structure directly into the function::

    true_knot = 'data/31.xyz'
    probabilistic_knot = 'data/1j85.pdb'                                                           
    alexander(true_knot, closure=Closure.CLOSED)
    alexander(probabilistic_knot)

In first case the result is '3_1'. In second case most probably outcome is also
'3_1'.

One can try with other invariants. There are few example structures available
in 'data' folder in out topoly_test project::

    conway(curve) 
    jones(curve)   
    homfly(curve)
    kauffman_bracket(curve)
    kauffman_polynomial(curve)
    blmho(curve)  
    yamada(curve)
    aps(curve)
    writhe(curve)

Default closure method is probabilistic one „TWO_POINTS". If you are interested
in how it works and what are other possible methods looks into PARAMS.PY (link).

You are not restricted to .pdb and .xyz formats, you can also pass .cif, and
mathematica output files. .xyz format can have indexes in its first column
but it is not required. You can also pass python list of lists (where internal 
list stores coordinates or index and coordinates) or PDcode or EMcode.

There are more options worth checking in documentation (link).


Calculating invariants of conjoined structures                                  
==================================================
In our dictionary of topologies are mainly prime structures. You may want to
find polynomials of structures which are compositions, which are not in our 
dictionary. Then you need to start with creating objects of your basic 
structures. Lets start with 3_1 knot::

    knot_31 = getpoly('HOMFLYPT', '3_1')

Which gives lists of correspoding structures::

    [+3_1: [-1 0 -2 0 [0]]|[0]|1 0 [0], -3_1: [[0] 0 -2 0 -1]|[0]|[0] 0 1]

Since there are two kinds of 3_1 knot with different chirality, we got list of
two objects, which are printed as list of two records with their data. First is
its name, second is code corresponding to coefficients of its polynomial. Now
I want to check what are polynomial of +3_1 # -3_1 and +3_1 U 3_1. It is simple
as it::

    plus_31, minus_31 = knot_31
    plus_31 + minus_31
    plus_31 * minus_31

and as a result it will give two records::

    +3_1 U -3_1: [[0]]|-2 0 -3 [0] 3 0 2|[0]|1 0 3 [0] -3 0 -1|[0]|-1 [0] 1
    +3_1 # -3_1: [2 0 [5] 0 2]|[0]|-1 0 [-4] 0 -1|[0]|[1]

Which are coefficients of HOMFLYPT polynomial of knot compositions. List of
such objects can be exported to new dictionary file::

    exportpoly(polynomials, exportfile='new_polvalues.py')

Lasso type indentification (minimal surface calculation)                        
==========================================================
For checking lasso topology we calculate minimal surface of lasso loop and
and check if it is crossed by lasso tail. Just input data and first and last 
indices of loop.::

    lasso_type('data/lasso_00.txt', [1,30])

to get output::

    '0 4 1 X X -33 +34 -35 -43 XX 0 2 1 X X -33 -43 XX LS2--C XX 10.4002 30 2.42151'

which means: ......

If you are interested in shape of minimal surface, type::

    make_surface('data/lasso_00.txt', [1,30])

which gives list of triangles that form minimal surface.


Random polygons generation
=============================

You can generate equilateral random walks, random loops and structures composed
of them: lassos and handcuffs. Loop generation is based on Jason Cantarellas
work (link). To generate such structures type::

    generate_walk(30, 100)           # 100 walks of length 30
    generate_loop(27, 100)           # 100 loops of length 27
    generate_lasso(12, 8, 100)       # 100 lassos with loop length of 12 and tail length of 8
    generate_handcuff([4,7], 5, 100) # 100 handcuffs with loops of length 4 and 7 and tail length of 5

They will be written in folder with name corresponding to passed parameters.
If you want to change default format check the documentation.

Visualization
=================

If you want to view .xyz structure in VMD, type::

    xyz2vmd('file.xyz')

function converts .xyz file into .pdb structure file and .psf topology file.
To open them in vmd type::
    
    vmd file.pdb -psf file.psf                                               

Data manipulation
==================
To translate polynomial coefficient data to topology type, write i.e.::

    find_matching('1 1 1 1 1 1 1 1 1', 'Yamada')

to get the result::

    '2^2_1'

You can also insert more complicated inputs like dictionary of polynomials with
their probabilities::

    find_matching({'1 -1 1': 0.8, '1 -3 1': 0.2}, 'Alexander')

or dictionary of probabilities for each subchain::

    find_matching({(0, 100): {'1 -1 1': 0.8, '1 -3 1': 0.2},(50, 100): {'1 -1 1': 0.3, '1': 0.7}},'Alexander')


Not described functions
========================
Functions for finding loops, lassos and theta-curves::

    find_loops(structure)
    find_lassos(structure)
    find_thetas(structure)

Matrix functions::

    find_spots(matrix)
    translate_matrix(matrix)
    plot_matrix(matrix)

Other::
    
    plot_graph(structure)
    close_curve(structure)
    reduce(structure)
    translate(strucutre)
    import_structure(structure_name)
    


