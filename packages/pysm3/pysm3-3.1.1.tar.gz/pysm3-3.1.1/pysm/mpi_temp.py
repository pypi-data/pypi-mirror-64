def distribute_rings(nside, rank, n_mpi_processes):
    """Create a libsharp map distribution based on rings
    Build a libsharp grid object to distribute a HEALPix map
    balancing North and South distribution of rings to achieve
    the best performance on Harmonic Transforms
    Returns the grid object and the pixel indices array in RING ordering
    Parameters
    ---------
    nside : int
        HEALPix NSIDE parameter of the distributed map
    rank, n_mpi_processes, ints
        rank of the current MPI process and total number of processes
    Returns
    -------
    grid : libsharp.healpix_grid
        libsharp object that includes metadata about HEALPix distributed rings
    local_pix : np.ndarray
        integer array of local pixel indices in the current MPI process in RING
        ordering
    """
    nrings = 4 * nside - 1  # four missing pixels

    # ring indices are 1-based
    ring_indices_emisphere = np.arange(2 * nside, dtype=np.int32) + 1

    local_ring_indices = ring_indices_emisphere[rank::n_mpi_processes]

    # to improve performance, symmetric rings north/south need to be in the same rank
    # therefore we use symmetry to create the full ring indexing

    if local_ring_indices[-1] == 2 * nside:
        # has equator ring
        local_ring_indices = np.concatenate(
            [local_ring_indices[:-1], nrings - local_ring_indices[::-1] + 1]
        )
    else:
        # does not have equator ring
        local_ring_indices = np.concatenate(
            [local_ring_indices, nrings - local_ring_indices[::-1] + 1]
        )

    if libsharp is None:
        grid = None
    else:
        grid = libsharp.healpix_grid(nside, rings=local_ring_indices)
    return local_ring_indices, grid
