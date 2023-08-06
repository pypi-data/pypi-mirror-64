import unittest
import numpy as np
from modelbase.ode import Model, Simulator
from modelbase.ode import ratefunctions as rf


def GENERATE_MODEL():
    parameters = {"k_in": 1, "kf": 1, "kr": 1}
    m = Model(parameters=parameters)
    m.add_compounds(["a", "b", "c1", "c2", "d1", "d2", "rate_time"])

    # Vanilla algebraic module
    m.add_algebraic_module(
        module_name="vanilla_module",
        function=lambda a: (a, 2 * a),
        compounds=["a"],
        derived_compounds=["a1", "a2"],
        modifiers=None,
        parameters=None,
    )

    # Time-dependent algebraic module
    m.add_algebraic_module(
        module_name="time_dependent_module",
        function=lambda time: (time,),
        compounds=None,
        derived_compounds=["derived_time"],
        modifiers=["time"],
        parameters=None,
    )

    # Singleton reaction
    m.add_reaction(
        rate_name="singleton_reaction",
        function=lambda k_in: k_in,
        stoichiometry={"b": 1},
        modifiers=None,
        parameters=["k_in"],
        reversible=False,
    )

    # Time-dependent reaction
    m.add_reaction(
        rate_name="time_dependent_reaction",
        function=lambda time: time,
        stoichiometry={"rate_time": 1},
        modifiers=["time"],
        parameters=None,
        reversible=False,
    )
    # Vanilla reaction
    m.add_reaction(
        rate_name="vanilla_reaction",
        function=rf.mass_action_1,
        stoichiometry={"c1": -1, "c2": 1},
        modifiers=None,
        parameters=["kf"],
        reversible=False,
    )
    # Reversible reaction
    m.add_reaction(
        rate_name="reversible_reaction",
        function=rf.reversible_mass_action_1_1,
        stoichiometry={"d1": -1, "d2": 1},
        modifiers=None,
        parameters=["kf", "kr"],
        reversible=True,
    )
    y0 = {
        "a": 1,
        "b": 1,
        "c1": 1,
        "c2": 0,
        "d1": 1,
        "d2": 0,
        "rate_time": 1,
    }
    return m, y0


def GENERATE_RESULTS(model, y0):
    s = Simulator(model,)
    s.initialise(y0=y0)
    t, y = s.simulate(t_end=10, steps=10)
    return s.copy()


MODEL, Y0 = GENERATE_MODEL()
SIM = GENERATE_RESULTS(model=MODEL, y0=Y0)


class SimulatorBaseTests(unittest.TestCase):
    def test_init(self):
        m = Model()
        s = Simulator(m)
        self.assertEqual(s.time, None)
        self.assertEqual(s.results, None)
        self.assertEqual(s.full_results, None)

    def test_update_parameters(self):
        m = Model(parameters={"k1": 1})
        s = Simulator(m)
        s.update_parameters(parameters={"k1": 2})
        self.assertEqual(s.model.parameters["k1"], 2)


class SimulationTests(unittest.TestCase):
    def test_simulate(self):
        parameters = {"alpha": 3}
        m = Model(parameters=parameters)
        m.add_derived_parameter(
            parameter_name="beta",
            function=lambda alpha: 3 - alpha,
            parameters=["alpha"],
        )
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=lambda x, alpha: alpha * x,
            stoichiometry={"x": 1},
            modifiers=["x"],
            parameters=["beta"],
            reversible=False,
        )
        y0 = {"x": 1}
        s = Simulator(model=m,)
        s.update_parameter(parameter_name="alpha", parameter_value=2)
        s.initialise(
            y0=y0, test_run=False,
        )
        t, y = s.simulate(t_end=10)
        self.assertTrue(np.isclose(y[-1][0], np.exp(10)))
        self.assertEqual(s.full_results, None)

    def test_simulate_to_steady_state(self):
        m = Model(parameters={"kf_base": 3})
        m.add_derived_parameter(
            parameter_name="kf",
            function=lambda kf_base: 3 - kf_base,
            parameters=["kf_base"],
        )
        m.add_compounds(compounds=["x", "y"])
        m.add_reaction(
            rate_name="v1",
            function=lambda x, kf: kf * x,
            stoichiometry={"x": -1, "y": 1},
            parameters=["kf"],
        )
        y0 = {"x": 1, "y": 0}
        s = Simulator(model=m,)
        s.update_parameter(parameter_name="kf_base", parameter_value=2)
        s.initialise(y0=y0, test_run=False)
        t, y = s.simulate_to_steady_state()
        np.testing.assert_array_almost_equal(y[0], [0, 1])
        self.assertEqual(s.full_results, None)

    def test_parameter_scan(self):
        parameters = {"kf": 1, "kr": 1}
        m = Model(parameters=parameters)
        m.add_compounds(compounds=["x", "y"])
        m.add_reaction(
            rate_name="v1",
            function=rf.reversible_mass_action_1_1,
            stoichiometry={"x": -1, "y": 1},
            parameters=["kf", "kr"],
            reversible=True,
        )
        y0 = {"x": 1, "y": 0}
        s = Simulator(model=m,)
        s.initialise(y0=y0, test_run=True)
        res = s.parameter_scan(
            parameter_name="kf",
            parameter_values=(1, 3, 4, 7, 9, 15),
            tolerance=1e-6,
            multiprocessing=False,
        )
        np.testing.assert_allclose(
            res["x"], [0.5, 0.25, 0.2, 0.125, 0.1, 0.0625], rtol=1e-6
        )
        np.testing.assert_allclose(
            res["y"], [0.5, 0.75, 0.8, 0.875, 0.9, 0.9375], rtol=1e-6
        )

    def test_parameter_scan_multiprocessing(self):
        parameters = {"kf": 1, "kr": 1}
        m = Model(parameters=parameters)
        m.add_compounds(compounds=["x", "y"])
        m.add_reaction(
            rate_name="v1",
            function=rf.reversible_mass_action_1_1,
            stoichiometry={"x": -1, "y": 1},
            parameters=["kf", "kr"],
            reversible=True,
        )
        y0 = {"x": 1, "y": 0}
        s = Simulator(model=m,)
        s.initialise(y0=y0, test_run=True)
        res = s.parameter_scan(
            parameter_name="kf",
            parameter_values=(1, 3, 4, 7, 9, 15),
            tolerance=1e-6,
            multiprocessing=True,
        )

        np.testing.assert_allclose(
            res["x"], [0.5, 0.25, 0.2, 0.125, 0.1, 0.0625], rtol=1e-6
        )
        np.testing.assert_allclose(
            res["y"], [0.5, 0.75, 0.8, 0.875, 0.9, 0.9375], rtol=1e-6
        )

    def test_get_full_results_dict_shape(self):
        s = SIM.copy()
        res = s.get_full_results_dict()
        self.assertEqual(res["a"].shape, (11,))
        self.assertEqual(res["b"].shape, (11,))
        self.assertEqual(res["c1"].shape, (11,))
        self.assertEqual(res["c2"].shape, (11,))
        self.assertEqual(res["d1"].shape, (11,))
        self.assertEqual(res["d2"].shape, (11,))
        self.assertEqual(res["rate_time"].shape, (11,))
        self.assertEqual(res["a1"].shape, (11,))
        self.assertEqual(res["a2"].shape, (11,))
        self.assertEqual(res["derived_time"].shape, (11,))

    def test_get_full_results_array_shape(self):
        s = SIM.copy()
        self.assertEqual(s.get_full_results_array().shape, (11, 10))

    def test_get_full_results_df_shape(self):
        s = SIM.copy()
        res = s.get_full_results_df()
        self.assertEqual(res.values.shape, (11, 10))
        self.assertEqual(
            res.index.values.tolist(),
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )
        self.assertEqual(
            res.columns.values.tolist(),
            ["a", "b", "c1", "c2", "d1", "d2", "rate_time", "a1", "a2", "derived_time"],
        )

    def test_get_variable_shape(self):
        s = SIM.copy()
        self.assertEqual(s.get_variable(variable="a").shape, (11,))

    def test_get_variables_shape(self):
        s = SIM.copy()
        y = s.get_variables(variables=["a", "b"])
        self.assertEqual(y.shape, (11, 2))
