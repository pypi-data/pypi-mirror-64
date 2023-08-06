5. Calibration of single-ended measurement with OLS
===================================================

A double ended calibration is performed with Ordinary Least Squares.
Over all timesteps simultaneous. :math:`\gamma` and :math:`\alpha`
remain constant, while :math:`C` varies over time. The weights are
considered equal here and no variance or confidence interval is
calculated.

Note that the internal reference section can not be used since there is
a connector between the internal and external fiber and therefore the
integrated differential attenuation cannot be considered to be linear
anymore.

.. code:: ipython3

    import os
    
    from dtscalibration import read_silixa_files
    import matplotlib.pyplot as plt
    
    %matplotlib inline


.. parsed-literal::

    /Users/bfdestombe/anaconda3/envs/dts/lib/python3.7/typing.py:845: FutureWarning: xarray subclass DataStore should explicitly define __slots__
      super().__init_subclass__(*args, **kwargs)


.. code:: ipython3

    filepath = os.path.join('..', '..', 'tests', 'data', 'single_ended')
    
    ds = read_silixa_files(
        directory=filepath,
        timezone_netcdf='UTC',
        file_ext='*.xml')
    
    ds100 = ds.sel(x=slice(-30, 101))  # only calibrate parts of the fiber, in meters
    sections = {
                'probe1Temperature':    [slice(20, 25.5)],  # warm bath
                'probe2Temperature':    [slice(5.5, 15.5)],  # cold bath
                }
    ds100.sections = sections


.. parsed-literal::

    3 files were found, each representing a single timestep
    4 recorded vars were found: LAF, ST, AST, TMP
    Recorded at 1461 points along the cable
    The measurement is single ended
    Reading the data from disk


.. code:: ipython3

    print(ds100.calibration_single_ended.__doc__)


.. parsed-literal::

    
    
            Parameters
            ----------
            store_p_cov : str
                Key to store the covariance matrix of the calibrated parameters
            store_p_val : str
                Key to store the values of the calibrated parameters
            p_val : array-like, optional
            p_var : array-like, optional
            p_cov : array-like, optional
            sections : dict, optional
            st_var : float, optional
                The variance of the measurement noise of the Stokes signals in
                the forward
                direction Required if method is wls.
            ast_var : float, optional
                The variance of the measurement noise of the anti-Stokes signals
                in the forward
                direction. Required if method is wls.
            store_c : str
                Label of where to store C
            store_gamma : str
                Label of where to store gamma
            store_dalpha : str
                Label of where to store dalpha; the spatial derivative  of alpha.
            store_alpha : str
                Label of where to store alpha; The integrated differential
                attenuation.
                alpha(x=0) = 0
            store_ta : str
                Label of where to store transient alpha's
            store_tmpf : str
                Label of where to store the calibrated temperature of the forward
                direction
            variance_suffix : str, optional
                String appended for storing the variance. Only used when method
                is wls.
            method : {'ols', 'wls'}
                Use 'ols' for ordinary least squares and 'wls' for weighted least
                squares
            solver : {'sparse', 'stats'}
                Either use the homemade weighted sparse solver or the weighted
                dense matrix solver of
                statsmodels
            matching_sections : List[Tuple[slice, slice, bool]]
                Provide a list of tuples. A tuple per matching section. Each tuple
                has three items. The first two items are the slices of the sections
                that are matched. The third item is a boolean and is True if the two
                sections have a reverse direction ("J-configuration").
            transient_att_x : iterable, optional
                Splices can cause jumps in differential attenuation. Normal single
                ended calibration assumes these are not present. An additional loss
                term is added in the 'shadow' of the splice. Each location
                introduces an additional nt parameters to solve for. Requiring
                either an additional calibration section or matching sections.
                If multiple locations are defined, the losses are added.
            fix_gamma : tuple
                A tuple containing two floats. The first float is the value of
                gamma, and the second item is the variance of the estimate of gamma.
                Covariances between gamma and other parameters are not accounted
                for.
            fix_dalpha : tuple
                A tuple containing two floats. The first float is the value of
                dalpha (Delta alpha in paper), and the second item is the
                variance of the estimate of dalpha.
                Covariances between alpha and other parameters are not accounted
                for.
    
            Returns
            -------
    
            


.. code:: ipython3

    ds100.calibration_single_ended(method='ols')


.. parsed-literal::

    /Users/bfdestombe/Projects/dts-calibration/python-dts-calibration-dev/.tox/docs/lib/python3.7/site-packages/dask/array/core.py:1361: FutureWarning: The `numpy.ndim` function is not implemented by Dask array. You may want to use the da.map_blocks function or something similar to silence this warning. Your code may stop working in a future release.
      FutureWarning,


Lets compare our calibrated values with the device calibration

.. code:: ipython3

    ds1 = ds100.isel(time=0)  # take only the first timestep
    
    ds1.tmpf.plot(linewidth=1, figsize=(12, 8), label='User calibrated')  # plot the temperature calibrated by us
    ds1.tmp.plot(linewidth=1, label='Device calibrated')  # plot the temperature calibrated by the device
    plt.title('Temperature at the first time step')
    plt.legend();



.. image:: 05Calibrate_single_ols.ipynb_files/05Calibrate_single_ols.ipynb_7_0.png


