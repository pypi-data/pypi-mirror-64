"""Abstract base class for Simulator interfaces."""

import warnings
import numpy as np
import pandas as pd
import copy
import json as json
import pickle as pickle
from abc import ABC, abstractmethod

from .integrators import _IntegratorScipy

try:
    from .integrators import _IntegratorAssimulo
except ImportError:  # pragma: no cover
    ASSIMULO_SUPPORT_FLAG = False
    if not ASSIMULO_SUPPORT_FLAG:
        warnings.warn("Assimulo not found, disabling sundials support.")
else:
    ASSIMULO_SUPPORT_FLAG = True


class _BaseSimulator(ABC):
    def __init__(self, model, integrator_name, **kwargs):
        self.model = model
        self.integrator_name = integrator_name

        # For restoring purposes
        self.y0 = kwargs.get("y0")
        self.time = kwargs.get("time")
        self.results = kwargs.get("results")

        # Placeholders
        self.integrator = None
        self.default_integrator_kwargs = None

    def __reduce__(self):
        """Pickle this class."""
        return (
            self.__class__,
            (self.model, self.integrator_name,),
            (("y0", self.y0), ("time", self.time), ("results", self.results),),
        )

    def copy(self):
        """Return a deepcopy of this class."""
        new = copy.deepcopy(self)
        if new.results is not None:
            new._initialise_integrator(
                y0=new.results[-1], integrator_name=new.integrator_name
            )
        elif new.y0 is not None:
            new.initialise(y0=new.y0, test_run=False)
        return new

    def clear_results(self):
        """Clear simulation results."""
        self.time = None
        self.results = None
        self.integrator._reset()

    def _initialise_integrator(self, y0, integrator_name):
        """Initialise the integrator.

        Parameters
        ----------
        y0 : iterable(num)
        integrator_name : str
        """
        if self.integrator_name == "assimulo" and ASSIMULO_SUPPORT_FLAG:
            self.integrator = _IntegratorAssimulo(rhs=self.model._get_rhs, y0=y0)
            self.default_integrator_kwargs = {
                "atol": 1e-8,
                "rtol": 1e-8,
                "maxnef": 4,  # max error failures
                "maxncf": 1,  # max convergence failures
                "verbosity": 50,
            }
        else:
            self.integrator = _IntegratorScipy(rhs=self.model._get_rhs, y0=y0)
            self.default_integrator_kwargs = {
                "atol": 1e-8,
                "rtol": 1e-8,
            }

    @abstractmethod
    def _test_run(self):
        """Perform a test step of the simulation in Python to get proper error handling."""

    def initialise(self, y0, test_run=True):
        """Initialise the integrator.

        Parameters
        ----------
        y0 : Union(dict(str: num), iterable(num))
        test_run : bool
            Whether to perform a test_run to get proper error handling.
        """
        if self.results is not None:
            self.clear_results()
        if isinstance(y0, dict):
            self.y0 = [y0[compound] for compound in self.model.get_compounds()]
        else:
            self.y0 = list(y0)
        self._initialise_integrator(y0=self.y0, integrator_name=self.integrator_name)

        if test_run:
            self._test_run()

    def simulate(self, t_end=None, steps=None, time_points=None, **integrator_kwargs):
        """Simulate the model.

        Parameters
        ----------
        t_end : num
        steps : int
            Number of integration time steps to be returned
        time_points : iterable(num)
            Explicit time points which shall be returned
        integrator_kwargs : dict

        Returns
        -------
        t : numpy.array
        y : numpy.array
        """
        if self.y0 is None:
            raise AttributeError(
                "No initial values set. Initialise the simulator first."
            )
        int_kwargs = self.default_integrator_kwargs.copy()
        int_kwargs.update(integrator_kwargs)

        if steps is not None and time_points is not None:
            warnings.warn(
                """
            You can either specify the steps or the time return points.
            I will use the time return points"""
            )
            if t_end is None:
                t_end = time_points[-1]
            time, results = self.integrator._simulate(
                t_end=t_end, time_points=time_points, **int_kwargs,
            )
        elif time_points is not None:
            time, results = self.integrator._simulate(
                t_end=time_points[-1], time_points=time_points, **int_kwargs,
            )
        elif steps is not None:
            if t_end is None:
                raise ValueError("t_end must no be None")
            time, results = self.integrator._simulate(
                t_end=t_end, steps=steps, **int_kwargs,
            )
        else:
            time, results = self.integrator._simulate(t_end=t_end, **int_kwargs,)
        time = np.array(time)
        # Continuous simulation
        if self.time is None:
            self.time = time
            self.results = results
        else:
            self.time = np.append(self.time, time[1:], axis=0)
            self.results = np.append(self.results, results[1:, :], axis=0)
        return time, results

    def simulate_to_steady_state(
        self, tolerance=1e-8, simulation_kwargs=None, **integrator_kwargs
    ):
        """Simulate the model.

        Parameters
        ----------
        tolerance : float
        simulation_kwargs : dict
        integrator_kwargs : dict

        Returns
        -------
        t : numpy.array
        y : numpy.array
        """
        int_kwargs = self.default_integrator_kwargs.copy()
        int_kwargs.update(integrator_kwargs)
        if simulation_kwargs is None:
            simulation_kwargs = {}
        time, results = self.integrator._simulate_to_steady_state(
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            integrator_kwargs=int_kwargs,
        )
        time = np.array([time])
        results = np.array([results])
        if self.time is None:
            self.time = time
            self.results = results
        else:
            self.time = np.append(self.time, time, axis=0)
            self.results = np.append(self.results, results, axis=0)
        return time, results

    def get_time(self):
        """Get simulation time.

        Returns
        -------
        time : numpy.array
        """
        return self.time

    def get_results_array(self):
        """Get simulation results.

        Returns
        -------
        results : numpy.array
        """
        return self.results

    def get_results_dict(self):
        """Get simulation results.

        Returns
        -------
        results : dict
        """
        return {k: self.results[:, i] for i, k in enumerate(self.model.get_compounds())}

    def get_results_df(self):
        """Get simulation results.

        Returns
        -------
        results : pandas.DataFrame
        """
        return pd.DataFrame(
            data=self.results, index=self.time, columns=self.model.get_compounds()
        )

    def get_fluxes_array(self):
        """Get the model fluxes for the simulation.

        Returns
        -------
        results : numpy.array
        """
        return self.model.get_fluxes_array(
            y=self.get_results_array(), t=self.get_time()
        )

    def get_fluxes_dict(self):
        """Get the model fluxes for the simulation.

        Returns
        -------
        results : dict
        """
        return self.model.get_fluxes_dict(y=self.get_results_array(), t=self.get_time())

    def get_fluxes_df(self):
        """Get the model fluxes for the simulation.

        Returns
        -------
        results : pandas.DataFrame
        """
        return self.model.get_fluxes_df(y=self.get_results_array(), t=self.get_time())

    def store_results_to_file(self, filename, filetype="json"):
        """Store the simulation results into a json or pickle file.

        Parameters
        ----------
        filename : str
            The name of the pickle file
        filetype : str
            Output file type. Json or pickle.
        """
        res = self.get_results_dict()
        res["time"] = self.get_time()
        res = {k: v.tolist() for k, v in res.items()}
        if filetype == "json":
            if not filename.endswith(".json"):
                filename += ".json"
            with open(filename, "w") as f:
                json.dump(obj=res, fp=f)
        elif filetype == "pickle":
            if not filename.endswith(".p"):
                filename += ".p"
            with open(filename, "wb") as f:
                pickle.dump(obj=res, file=f)
        else:
            raise ValueError("Can only save to json or pickle")

    def load_results_from_file(self, filename, filetype="json"):
        """Load simulation results from a json or pickle file.

        Parameters
        ----------
        filename : str
            The name of the pickle file
        filetype : str
            Input file type. Json or pickle.
        """
        if filetype == "json":
            with open(filename, "r") as f:
                res = json.load(fp=f)
        elif filetype == "pickle":
            with open(filename, "rb") as f:
                res = pickle.load(file=f)
        else:
            raise ValueError("Can only save to json or pickle")
        res = {k: np.array(v) for k, v in res.items()}
        model_compounds = self.model.get_compounds()
        time = res.pop("time")
        self.time = time
        self.results = np.array(
            [v for k, v in res.items() if k in model_compounds]
        ).reshape((len(time), len(model_compounds)))
