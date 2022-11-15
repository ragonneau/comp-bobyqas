import numpy as np
import pdfo
import pybobyqa


class Minimizer:
    def __init__(self, problem, solver, max_eval, options, callback, *args, **kwargs):
        self.problem = problem
        self.solver = solver
        self.max_eval = max_eval
        self.options = dict(options)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if not self.validate():
            raise NotImplementedError

        # The following attributes store the objective function and maximum
        # constraint violation values obtained during a run.
        self.fun_history = None
        self.maxcv_history = None

    def __call__(self):
        self.fun_history = []
        self.maxcv_history = []

        x0 = self.problem.x0
        xl = self.problem.xl
        xu = self.problem.xu
        a_ineq = self.problem.a_ineq
        b_ineq = self.problem.b_ineq
        a_eq = self.problem.a_eq
        b_eq = self.problem.b_eq
        options = dict(self.options)
        if self.solver.lower() == 'bobyqa':
            bounds = pdfo.Bounds(xl, xu)
            constraints = []
            if self.problem.m_lin_ineq > 0:
                constraints.append(pdfo.LinearConstraint(a_ineq, -np.inf, b_ineq))
            if self.problem.m_lin_eq > 0:
                constraints.append(pdfo.LinearConstraint(a_eq, b_eq, b_eq))
            if self.problem.m_nonlin_ineq > 0:
                constraints.append(pdfo.NonlinearConstraint(self.problem.c_ineq, -np.inf, np.zeros(self.problem.m_nonlin_ineq)))
            if self.problem.m_nonlin_eq > 0:
                constraints.append(pdfo.NonlinearConstraint(self.problem.c_eq, np.zeros(self.problem.m_nonlin_eq), np.zeros(self.problem.m_nonlin_eq)))
            options['maxfev'] = self.max_eval
            res = pdfo.pdfo(self.eval, x0, method='bobyqa', bounds=bounds, constraints=constraints, options=options)
            success = res.success
        elif self.solver.lower() == 'py-bobyqa':
            rhobeg = 1.0
            rhobeg = min(rhobeg, 0.4999 * np.min(xu - xl))
            rhoend = min(rhobeg, 1e-6)
            try:
                res = pybobyqa.solve(self.eval, x0, bounds=(xl, xu), rhobeg=rhobeg, rhoend=rhoend, maxfun=self.max_eval, objfun_has_noise=options.get('objfun_has_noise', False), do_logging=False)
                success = res.flag == res.EXIT_SUCCESS
            except AssertionError:
                success = False
        else:
            raise NotImplementedError
        return success, np.array(self.fun_history, copy=True), np.array(self.maxcv_history, copy=True)

    def validate(self):
        valid_solvers = {}
        if self.problem.type not in 'quadratic other adjacency linear':
            valid_solvers = {'bobyqa', 'py-bobyqa'}
        return self.solver.lower() in valid_solvers

    def eval(self, x):
        f = self.problem.fun(x, self.callback, *self.args, **self.kwargs)
        if self.callback is not None:
            # If a noise function is supplied, the objective function returns
            # both the plain and the noisy function evaluations. We return the
            # noisy function evaluation, but we store the plain function
            # evaluation (used to build the performance and data profiles).
            self.fun_history.append(f[0])
            f = f[1]
        else:
            self.fun_history.append(f)
        self.maxcv_history.append(self.problem.maxcv(x))
        return f
