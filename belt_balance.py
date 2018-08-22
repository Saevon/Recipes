from __future__ import division # Switch to sympy rationals later


import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (15, 5)
plt.rcParams['font.size'] = 25

import numpy as np
from sympy import Rational, sympify, nsimplify

import seaborn as sb

def set_balancer_flow(junctions,upstream_densities,downstream_velocities,debug=False,maxiter=100,tol=0):
    """
        Compute the flow in a given balancer configuration.  The flow consists of a density (rho)
        and velocity (v) for each tile of each belt, such that the conservation condition
        (flow in = flow out) is enforced at each junction.

        Required inputs:
            - junctions: a list of triples (x,y1,y2) that means belts y1 and y2 are
              joined at the left edge of tile x (x>0).  Note that belts are indexed
              from zero; tiles are also indexed from zero but no junctions are allowed
              on tile zero (it is reserved for the upstream inflow).
            - upstream_densities: a list of densities, one for the upstream flow of
              each belt.  A value of 1 means the belt is fully loaded, while zero
              means it is empty.
            - downstream_velocities: a list of velocities, one for each belt.
              Velocity one means items on the belt are moving at normal speed.
              Smaller velocity is possible only if the belt is full (rho=1).
              Zero velocity means the belt is completely stopped/blocked
              downstream.

        Outputs: rho and v, the density and velocity of each tile of each belt.
              Usually visualized using plot_belts().

        Optional inputs:
            - debug: makes a plot at every step of the solution process; be warned
              that this can generate hundreds of plots, which might exhaust your
              graphics memory.
            - maxiter: maximum number of iterations allowed before giving up.  If this
              is exceeded, it often means that there is a feedback loop that won't
              converge in a finite number of iterations, but stopping after many iterations
              will usually give a very accurate approximation of the true solution.
            - tol: a numerical tolerance; once differences in flow across junctions are
              smaller than this, the solver will terminate.  For an exact solution, the
              default value of zero must be used.  Setting this larger than zero is useful for
              cases in which the exact solution will never be reached.
    """
    # Get problem domain bounds
    n_belts = len(upstream_densities)
    x, y1, y2 = zip(*junctions)
    length = max(x)

    # Create more convenient lists of junctions, ordered by tile or belt
    junctions_x = [ [] for i in range(length+1)]
    junctions_by_belt = [ [] for i in range(n_belts)]
    for x, y1, y2 in junctions:
        assert(x>0)  # No junctions allowed at x=0
        junctions_x[x].append( (y1,y2) )
        junctions_by_belt[y1].append(x)
        junctions_by_belt[y2].append(x)

    # Check for overlapping junctions
    for belt in range(n_belts):
        for x in range(length+1):
            assert(junctions_by_belt[belt].count(x)<=1)

    # Make sure all boundary conditions are set
    assert len(upstream_densities) == len(downstream_velocities)

    # Check all velocities and densities are in [0,1]
    assert( all([0<=m<=1 for m in upstream_densities]) )
    assert( all([0<=m<=1 for m in downstream_velocities]) )

    # Use rational arithmetic if possible
    try:
        upstream_densities    = [nsimplify(d) for d in upstream_densities]
        downstream_velocities = [nsimplify(d) for d in downstream_velocities]
    except:
        pass

    # Set all densities to zero and velocities to one
    rho = [ [0 for i in range(n_belts)] for j in range(length+1) ]
    v   = [ [1 for i in range(n_belts)] for j in range(length+1) ]

    # Set inflow densities
    for belt, rho_upstream in enumerate(upstream_densities):
        rho[0][belt] = rho_upstream
    # Set outflow velocities
    for belt, v_downstream in enumerate(downstream_velocities):
        v[length][belt] = v_downstream
        if v_downstream < 1:
            rho[length][belt] = 1

    propagate_downstream(rho,junctions_by_belt,n_belts,length)
    propagate_upstream(rho,v,junctions_by_belt,n_belts,length)

    something_changed = True
    iterations = 0
    # Loop until convergence
    while something_changed:
        iterations += 1
        if iterations > maxiter:
            print('Maximum number of iterations reached')
            break
        something_changed = False
        for i in range(1,length+1):         # Loop over x
            for junction in junctions_x[i]: # Loop over junctions
                y1, y2 = junction           # Belts involved in this junction
                inn = i-1                   # inflow tile
                out = i                     # outflow tile
                flux_in  = [rho[inn][y]*v[inn][y] for y in (y1,y2)]
                flux_out = [rho[out][y]*v[out][y] for y in (y1,y2)]

                # If inflow > outflow:
                if sum(flux_out) > sum(flux_in):
                    raise Exception('inverted flux condition!')
                if sum(flux_in) > sum(flux_out)+tol:
                    # If possible, increase both outflow densities to the average inflow density
                    mean_upstream_density = (rho[inn][y1]+rho[inn][y2])/2
                    if (rho[out][y1] <= mean_upstream_density) and (rho[out][y2] <= mean_upstream_density) and \
                       (v[out][y1]==1) and (v[out][y2]==1):
                        rho[out][y1] = mean_upstream_density
                        rho[out][y2] = mean_upstream_density
                        something_changed = True
                    # Otherwise, at least one outflow density is 1.
                        # If possible, assign all the
                        # surplus outflow to the non-full outflow by increasing its density.
                    elif (rho[out][y1] == 1) and (rho[out][y2] <= sum(flux_in) - v[out][y1] <= 1) and (rho[out][y2]<1):
                        rho[out][y2] = sum(flux_in) - v[out][y1]
                        something_changed = True
                    elif (rho[out][y2] == 1) and (rho[out][y1] <= sum(flux_in) - v[out][y2] <= 1) and (rho[out][y1]<1):
                        rho[out][y1] = sum(flux_in) - v[out][y2]
                        something_changed = True
                    else:  # Both outflows are maxed out
                        if rho[out][y1] < 1: rho[out][y1] = Rational(1)
                        if rho[out][y2] < 1: rho[out][y2] = Rational(1)
                        flux_out = [rho[out][y]*v[out][y] for y in (y1,y2)]
                        mean_v_out = (v[out][y1]+v[out][y2])/2
                        # If the density of one inflow branch is less than the mean outflow velocity,
                        # leave that one alone; set the density of the other inflow to 1 and reduce
                        # its velocity so that conservation is enforced
                        if (rho[inn][y1]<=mean_v_out): # Inflow 1 is okay; assign excess to inflow 2
                            rho[out][y1] = Rational(1)
                            rho[out][y2] = Rational(1)
                            rho[inn][y2] = Rational(1)
                            v[inn][y2] = sum(flux_out) - rho[inn][y1]
                            something_changed = True
                            propagate_upstream(rho,v,junctions_by_belt,n_belts,length)
                        elif (rho[inn][y2]<=mean_v_out): # Inflow 2 is okay; assign excess to inflow 1
                            rho[inn][y1] = 1
                            v[inn][y1] = sum(flux_out) - rho[inn][y2]
                            something_changed = True

                        # If the density of both inflow branches is greater than (or equal to) the
                        # mean outflow velocity,
                        # set each inflow density to 1 and inflow velocity to the mean outflow velocity
                        elif (rho[inn][y1]>=mean_v_out) and (rho[inn][y2]>=mean_v_out):
                            rho[inn][y1] = 1
                            rho[inn][y2] = 1
                            v[inn][y1] = mean_v_out
                            v[inn][y2] = mean_v_out
                            something_changed = True
                        else:
                            print('Failed to resolve junction!')
                            something_changed = False

                    propagate_downstream(rho,junctions_by_belt,n_belts,length)
                    propagate_upstream(rho,v,junctions_by_belt,n_belts,length)
                    if debug:
                        plt.figure()
                        plot_belts(rho,v,junctions)
                        print(rho[-1])
    # Check that total flux at each tile is the same
    total_flux = [ sum([rho[j][belt]*v[j][belt] for belt in range(n_belts)]) for j in range(length) ]
    #print total_flux
    try:
        for j in range(1,length):
            assert(abs(total_flux[j]-total_flux[0])<=10*tol)
    except:
        print('Failed flux check!')
        print(total_flux)
    return rho, v


def propagate_downstream(rho,junctions_by_belt,n_belts,length):
    # Fill in free-streaming tiles
    for belt in range(n_belts):
        for x in range(1,length+1):
            if x not in junctions_by_belt[belt]: # if no junction at left edge of tile
                if rho[x][belt] <= rho[x-1][belt]:
                    rho[x][belt] = rho[x-1][belt]


def propagate_upstream(rho,v,junctions_by_belt,n_belts,length):
    # Propagate jams upstream
    for belt in range(n_belts):
        for x in range(length-1,-1,-1):
            if (x+1) not in junctions_by_belt[belt]: # if no junction at right edge of tile
                if rho[x][belt] <= rho[x+1][belt]:
                    rho[x][belt] = rho[x+1][belt]
                if v[x][belt] > v[x+1][belt]:
                    v[x][belt] = v[x+1][belt]


def plot_belts(rho,v,junctions):
    """
        Plots the flow, using colors for velocity and printing out the density on each tile.
        Junctions are plotted as lines connecting tiles; these will not look correct if a junction
        joins two belts whose indices are not consecutive.

        In the plot, flow is left to right and belt number increases downward.
    """
    labels = np.array(rho)
    if labels.dtype is np.dtype(object):
        fmt = ''
    else:
        fmt = '.2g'
    n_belts = len(rho[0])
    length = len(rho)
    sb.heatmap(np.array(v).T.astype(float),annot=np.array(rho).T,vmin=0,vmax=1,
               linewidths=1,cmap="OrRd_r",fmt = fmt,cbar_kws={'label':'velocity'});

    junctions_x = [ [] for i in range(length+1)]
    for x, y1, y2 in junctions:
        assert(x>0)  # No junctions allowed at x=0
        if (y2,y1) not in junctions_x:
            junctions_x[x].append( (y1,y2) )

    for x, junclist in enumerate(junctions_x):
        for i, junction in enumerate(junclist):
            y1, y2 = junction
            plt.plot([x,x+0.05*(i+1),x+0.05*(i+1),x],[n_belts-y1-0.5,n_belts-y1-0.5,n_belts-y2-0.5,n_belts-y2-0.5],'-k',linewidth=5)

    return plt



import itertools

on_off = [0, 1]
for (x, y, z) in itertools.product(*itertools.repeat(on_off, 3)):
    junctions = [
        (1, 0, 1),
        (1, 2, 3),

        (2, 1, 2),
        (3, 0, 3),
    ]

    upstream_densities    = (1, 1, 1, 1)
    downstream_velocities = (1, 1, 1, 1)

    # Reset the "plot"
    plt.figure()

    rho, v = set_balancer_flow(junctions, upstream_densities, downstream_velocities)
    fig = plot_belts(rho, v, junctions)

    fig.savefig('output/velocity-{}-{}-{}.png'.format(x, y, z))









