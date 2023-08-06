# Copyright 2016, FBPIC contributors
# Authors: Remi Lehe, Manuel Kirchen, Kevin Peters
# License: 3-Clause-BSD-LBNL
"""
This file is part of the Fourier-Bessel Particle-In-Cell code (FB-PIC)
It defines particle utility methods.
"""
import numpy as np

# -----------------------
# Particle shapes utility
# -----------------------

def weights(x, invdx, offset, Nx, direction, shape_order):
    """
    Return the array of cell indices and corresponding shape factors
    for current/charge deposition and field gathering

    Parameters:
    -----------
    x : 1darray of floats (in meters)
        Array of particle positions along a given direction
        (one element per macroparticle)

    invdx : float (in meters^-1)
        Inverse of the grid step along the considered direction

    offset : float (in meters)
        Position of the edge of the simulation box,
        along the direction considered

    Nx : int
        Number of gridpoints along the considered direction

    direction : string
        Determines the boundary conditions. Either 'r' or 'z'

    shape_order : int
        Order of the shape factor.
        Either 1 or 3

    Returns:
    --------
    A tuple containing :

    i: 2darray of ints
        An array of shape (shape_order+1, Ntot)
        where Ntot is the number of macroparticles
        (i.e. the number of elements in the array x)
        This array contains the indices of the grid cells
        (along the axis specified by `direction`) where each macroparticle
        deposits charge/current and gathers field data.

    S: 2darray of floats
        An array of shape (shape_order+1, Ntot)
        where Ntot is the number of macroparticles
        (i.e. the number of elements in the array x)
        This array contains the shape factors (a.k.a. interpolation weights)
        that correspond to each of the indices in the array `i`.
    """
    # Positions of the particles, in the cell unit
    x_cell = invdx*(x - offset) - 0.5

    # Initialize empty arrays of the correct size
    i = np.empty( (shape_order+1, len(x)), dtype=np.int64)
    S = np.empty( (shape_order+1, len(x)), dtype=np.float64)

    # Indices and shapes
    if shape_order == 1:
        i[0,:] = np.floor(x_cell).astype('int')
        i[1,:] = i[0,:] + 1
        # Linear weight
        S[0,:] = i[1,:] - x_cell
        S[1,:] = x_cell - i[0,:]
    elif shape_order == 3:
        i[0,:] = np.floor(x_cell).astype('int') - 1
        i[1,:] = i[0,:] + 1
        i[2,:] = i[0,:] + 2
        i[3,:] = i[0,:] + 3
        # Cubic Weights
        S[0,:] = -1./6. * ((x_cell-i[0])-2)**3
        S[1,:] = 1./6. * (3*((x_cell-i[1])**3) - 6*((x_cell-i[1])**2)+4)
        S[2,:] = 1./6. * (3*((i[2]-x_cell)**3) - 6*((i[2]-x_cell)**2)+4)
        S[3,:] = -1./6. * ((i[3]-x_cell)-2)**3
    else:
        raise ValueError("shapes other than linear and cubic are not supported yet.")

    # Periodic boundary conditions in z
    if direction == 'z':
        # Lower Bound Periodic
        i = np.where( i < 0, i+Nx, i )
        # Upper Bound Periodic
        i = np.where( i > Nx-1, i-Nx, i )
    # Absorbing boundary condition at the upper r boundary
    elif direction == 'r':
        i = np.where(  i > Nx-1, Nx-1, i )
        # Note: The lower bound index shift for r is done in the gather
        # and deposit methods because the sign changes.
        # This avoids using specific guard cells.
    else:
        raise ValueError("Unrecognized `direction` : %s" % direction)

    # Return the result
    return( i, S )
