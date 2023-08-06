import cvxpy as cp
from .functions import ZeroFunction


class StateSpaceModel(object):
    """
        State-Space model:

        min loss_v(v) + loss_w(w) + r_x(x) + r_o(o) + r_s(s)
        s.t.
            x[t+1] = f_t(x[t], w[t], s[t])
            y[t] = h_t(x[t], u[t], o[t])

        where (f_t, h_t) are described by the dynamical_system.
    """

    def __init__(
        self,
        dynamical_system,
        loss_v=ZeroFunction(),
        loss_w=ZeroFunction(),
        reg_x=ZeroFunction(),
        reg_o=ZeroFunction(),
        reg_s=ZeroFunction(),
    ):

        # Save system dynamics
        self.dynamical_system = dynamical_system
        # Save filter loss associated with measurement noise
        self.loss_v = loss_v
        # Save filter loss associated with state-transition noise
        self.loss_w = loss_w
        # Save regularizers
        self.reg_x, self.reg_o, self.reg_s = reg_x, reg_o, reg_s

    def fit(self, y):
        """
            Estimate/learn unknown parameters of the model TODO
        """

        # Observed signal
        self.y = y
        # Number of observations
        self.n = y.shape[1]

    def filter(self, y):

        # Number of observations
        n = y.shape[1]

        # Create decision variables
        # Measurement noise
        v = cp.Variable((self.dynamical_system.p, n))
        # Measurement outliers
        o = cp.Variable((self.dynamical_system.p, n))
        # State
        x = cp.Variable((self.dynamical_system.m, n + 1))
        # Structural break
        s = cp.Variable((self.dynamical_system.m, n))
        # State-tramsition noise
        w = cp.Variable((self.dynamical_system.q, n))

        # Objective function
        obj = cp.Minimize(
            self.loss_v.expression(v)
            + self.loss_w.expression(w)
            + self.reg_x.expression(x)
            + self.reg_s.expression(s)
            + self.reg_o.expression(o)
        )

        #
        self.constraints = []
        for t in range(n):
            self.constraints.append(
                x[:, t + 1] == self.dynamical_system.f(x[:, t], v[:, t], s[:, t], t)
            )
        for t in range(n):
            self.constraints.append(
                y[:, t] == self.dynamical_system.h(x[:, t], w[:, t], o[:, t], t)
            )

        prob = cp.Problem(obj, self.constraints)
        try:
            self.result = prob.solve(verbose=False, solver=cp.OSQP)
        except:
            self.result = prob.solve(verbose=False, solver=cp.SCS)

        self.s = s.value
        self.v = v.value
        self.x = x.value
        self.o = o.value
        self.w = w.value
