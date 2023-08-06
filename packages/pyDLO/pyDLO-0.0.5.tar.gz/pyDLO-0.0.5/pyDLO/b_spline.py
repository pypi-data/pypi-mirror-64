import bspline
import bspline.splinelab as splinelab
import matplotlib.pyplot as plt
import matplotlib as mpl
#from mpl_toolkits.mplot3d import Axes3D
import numpy
class BSpline:
    def __init__(self, a, b, du, ncpts, cpts):
        self.a = a
        self.b = b
        self.du = du
        self.ncpts = ncpts
        self.cpts = cpts
        self.u = numpy.arange(a, b, du)
        self.nSample = self.u.size
        self.degree = 3
        self.order = self.degree + 1
        self.nSegments = self.ncpts - 3
        self.nIntervals = self.nSegments + 1
        self.breaks = numpy.linspace(a, b, self.nIntervals)
        self.knots = splinelab.augknt(self.breaks, self.degree)
        self.bs = bspline.Bspline(self.knots, self.degree)
        self.B = self.bs.collmat(self.u)
        self.dB = self.bs.collmat(self.u, 1)
        self.ddB = self.bs.collmat(self.u, 2)
        self.dddB = self.bs.collmat(self.u, 3)
        self.updateSpline(cpts)
        #self.drdri = numpy.zeros([self.ncpts, self.nSample, 3])
        #self.ddrdri = numpy.zeros([self.ncpts, self.nSample, 3])
        self.drdri = numpy.zeros([self.nSample, 3, self.ncpts])
        self.ddrdri = numpy.zeros([self.nSample, 3, self.ncpts])
        for i in numpy.arange(0, self.ncpts):
            self.drdri[:,:,i] = numpy.tile(self.dB[:,i],[3,1]).T
            self.ddrdri[:,:,i] = numpy.tile(self.ddB[:,i],[3,1]).T
            #self.drdri[i, :, :] = numpy.tile(self.dB[:, i], [3, 1]).T
            #self.ddrdri[i, :, :] = numpy.tile(self.ddB[:, i], [3, 1]).T
    def updateSpline(self, cpts):
        if cpts.shape[0] == 4*self.ncpts:
            cpts = cpts.reshape((9,4), order='F')
        self.q = self.B@cpts
        self.dq = self.dB@cpts
        self.ddq = self.ddB@cpts
        self.dddq = self.dddB@cpts

    def plotr(self):
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(self.q[:, 0], self.q[:, 1], self.q[:, 2], label='r(u)')
        ax.plot(self.cpts[:, 0], self.cpts[:, 1], self.cpts[:, 2], 'rx', label='Control points')
        ax.set_xlabel('x-axis Position [m]')
        ax.set_ylabel('y-axis Position [m]')
        ax.set_zlabel('z-axis Position [m]')
        ax.legend()
        plt.show()

if __name__ == "__main__":
    a = 0
    b = 2
    nCpts = 9
    du = 0.001
    x = numpy.linspace(a, b, nCpts)
    cpts = numpy.zeros([nCpts, 4])
    cpts[:, 0] = x
    #Create the spline object
    bs = BSpline(a, b, du, nCpts, cpts)
    bs.plotr()
    