#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


#####################################################
def uvmodelfit(xds, field=None, spw=None, timerange=None, uvrange=None, antenna=None, scan=None, niter=5, comptype='p', sourcepar=[1, 0, 0],
               varypar=[]):
    """
    .. todo::
        This function is not yet implemented

    Fit simple analytic source component models directly to visibility data

    Parameters
    ----------
    xds : xarray.core.dataset.Dataset
        input Visibility Dataset
    field : int
        field selection. If None, use all fields
    spw : int
        spw selection. If None, use all spws
    timerange : int
        time selection. If None, use all times
    uvrange : int
        uvrange selection. If None, use all uvranges
    antenna : int
        antenna selection. If None, use all antennas
    scan : int
        scan selection. If None, use all scans
    niter : int
        number of fitting iteractions to execute
    comptype : str
        component type (p=point source, g=ell. gauss. d=ell. disk)
    sourcepar : list
        starting fuess (flux, xoff, yoff, bmajaxrat, bpa)
    varypar : list
        parameters that may vary in the fit

    Returns
    -------
    xarray.core.dataset.Dataset
        New Visibility Dataset with updated data
    """
    return {}
