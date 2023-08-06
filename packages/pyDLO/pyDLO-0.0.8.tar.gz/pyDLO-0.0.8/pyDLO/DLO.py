import numpy as np
import scipy.integrate
from pyDLO.b_spline import BSpline
from scipy.linalg import block_diag, pinv
from numpy.linalg import norm
class DLO:

    def __init__(self,L, D, E, v, rho, cptsMatrix, du, kv, nCpts, nt, dt, t0, tf):
        
        self.L = L;
        self.du = du;
        self.D = D;
        self.E = E;
        self.v = v;
        self.rho = rho;
        self.mu = rho*np.pi*D**2/4;
        self.kv = kv;
        #Calcolo della spline
        self.bSpline = BSpline(0,L,du,nCpts,cptsMatrix);
        self.Nsample = self.bSpline.nSample;
        #TODO: Controllare E G H
        #Calcolo di G
        self.G = E/(2*(1+self.v));
        #Calcolo della matrice di Hooke
        self.H = ((D**2 * np.pi)/4) * np.diag([E, (self.G*D**2)/8, (E*D**2)/16]);
        #Momento polare di inerzia
        self.I0 = np.pi*(D**4)/32;
        #Matrice di inerzia costante
        self.J = np.diag([self.mu, self.mu, self.mu, self.I0]);
        #Calcolo della matrice delle masse e la sua inversa
        [self.M, self.M_inv] = self.massMatrix();
        #Inizializzo C P T tau e i eb0 et0 che resteranno costanti
        #[self.C,self.P,self.T,self.tau,self.et0,self.eb0] = self.computeCPTtau;
        self.computeCPTtau();
        self.dr0 = self.bSpline.dq[:,0:3];#Prendo il valore iniziale di dr          
        self.normdr0 = norm(self.dr0, axis=1)           
        self.et0 = self.et; #All'inizio sono uguali            
        self.eb0 = self.eb; #All'inizio sono uguali            
        self.Fgrav = self.gravity(self.M)                     
        #Condizioni iniziali q0 dq0 ddq0       
        self.default_initial_condition()
        self.k_PT = (-np.pi*self.G*self.D**4)/32
        self.k_PT1 = self.k_PT/2
        self.k_PB = (-np.pi*self.E*self.D**4)/64
        self.kPS = -(np.pi * self.E * self.D**2)/4;              
        #Fill Bij            
        #self.computeBij();
        #Time spline
        #La matrice dei punti di controllo della spline temporale è
        #inizialmente uguale            
        #temp = self.bSpline.cptsMatrix.T;           
        #temp = temp(:);           
        #self.nt = nt;           
        #self.timeCpts = repmat(temp,1,nt);           
        #self.t0 = t0; self.tf = tf; self.dt = dt;          
        #self.tbSpline = b_spline1(t0, tf, dt, self.timeCpts, nt);
    def massMatrix(self):
        n = self.bSpline.ncpts;
        u = self.bSpline.u;
        M_temp = np.zeros([n,n]);
        for i in np.arange(0,n):
            for j in np.arange(0,n):
                M_temp[i][j] = np.trapz(self.bSpline.B[:,i] * self.bSpline.B[:,j], u);
        #Wv_temp = Dlo.kv * M_temp;
        #Dlo.Wv = blkdiag(Wv_temp,Wv_temp,Wv_temp,Wv_temp);
        Mr = self.mu * M_temp;
        Mtheta = self.I0 * M_temp;
        M = block_diag(Mr,Mr,Mr,Mtheta);
        M_inv = pinv(M);
        return M,M_inv
    
    def computeCPTtau(self):
        self.C = np.cross(self.bSpline.dq[:,0:3], self.bSpline.ddq[:,0:3])
        normC = norm(self.C,axis=1)
        normC_i = np.nan_to_num(1/normC, posinf=0.0, neginf=0.0)
        normdr = norm(self.bSpline.dq[:,0:3],axis=1)
        normdr_i = np.nan_to_num(1/normdr, posinf=0.0, neginf=0.0)
        
        C_normalized = self.C * normC_i[:,None]**2
        #Voglio una riga alla volta C[i].T@dddq[][i]
        #tau = np.zeros([2000])
        #for i in np.arange(0,2000):
        #    tau[i] = C_normalized[i]@self.bSpline.dddq[:,0:3][i]
        self.tau = np.einsum('ij,ij->i', C_normalized,self.bSpline.dddq[:,0:3])
        
        #et = theta' + tau
        self.et = self.bSpline.dq[:,3] + self.tau
        
        #eb = ||C||/||dr||^3
        #np.cross(c,t,axisa=0, axisb=0, axisc=1)
        self.eb = normC * normdr_i**3
        #dr_3D = np.tile(self.bSpline.dq[:,0:3],(self.bSpline.ncpts,1,1))
        #ddr_3D = np.tile(self.bSpline.ddq[:,0:3],(self.bSpline.ncpts,1,1))
        #dddr_3D = np.tile(self.bSpline.dddq[:,0:3],(self.bSpline.ncpts,1,1))
        dr = self.bSpline.dq[:,0:3]
        ddr = self.bSpline.ddq[:,0:3]
        dddr = self.bSpline.dddq[:,0:3]
        self.P = np.cross(dr[:,:,None], self.bSpline.ddrdri, axis=1) + np.cross(self.bSpline.drdri, ddr[:,:,None], axis=1)
        #self.P = np.cross(dr_3D,self.bSpline.ddrdri) + np.cross(self.bSpline.drdri, ddr_3D);
        #self.R = np.zeros_like(self.P)
        #for i in np.arange(0,self.bSpline.ncpts):
        #    self.R[i,:,:] = (self.C.T * self.bSpline.dddB[:,i]).T  - np.cross(self.P[i,:,:],dddr_3D[i,:,:]);
        self.R = self.C[:,:,None] * self.bSpline.dddB[:,None,:] - np.cross(self.P, dddr[:,:,None], axis=1)
        #self.Gi = np.cross(self.C, self.P);
        self.Gi = np.cross(self.C[:,:,None], self.P, axis=1)
        self.T = self.R - 2*self.tau[:,None,None]*self.Gi;
        #self.F = T .* normC_i - Dlo.bSpline.dq(4,:).*Dlo.bSpline.dq(1:3,:).*Dlo.bSpline.B3.*normdr.^2;
            
    def gravity(self, M):
        gvec = np.zeros([4*self.bSpline.ncpts])
        gvec[2*self.bSpline.ncpts :3*self.bSpline.ncpts -1] = -9.81
        return M@gvec
    def default_initial_condition(self):
        self.q0 = self.bSpline.cpts.flatten('F')
        self.qd0 = np.zeros_like(self.q0)
        self.qdd0 = np.zeros_like(self.q0)
        self.zita0 = np.concatenate((self.q0, self.qd0))
        
    def setL(self,L):
        self.nc = L.shape[0]
        self.L_matrix = L
        if self.nc<2:
            self.M_L = np.block([[self.M, L.T], [L, 0]])
        else:
             self.M_L = np.block([[self.M, L.T], [L, np.zeros([self.nc, self.nc])]])    
        #Calcolo l'inversa
        self.M_L_inv = pinv(self.M_L)
        #Per calcolare Ac ho bisogno di L * M_inv * L'
        self.LML_inv = pinv(L @ self.M_inv @ L.T);
        self.E_constraint = np.zeros(self.nc);    
        
    def Pot(self):
        
        ds = norm(self.bSpline.dq[:,0:3], axis=1)
        
        nc = norm(self.C,axis=1)
        nc_i = np.nan_to_num(1/nc, posinf=0.0, neginf=0.0)
        ndr = norm(self.bSpline.dq[:,0:3],axis=1)
        ndri = np.nan_to_num(1/ndr, posinf=0.0, neginf=0.0)
        #C = repmat(Dlo.C,1,1,Dlo.bSpline.nCpts);
        Ps_r = (self.kPS * (1 - self.normdr0 * ndri)[:,None] * self.bSpline.dq[:,0:3])[:,:,None] * self.bSpline.dB[:,None,:] * ds[:,None,None]
        
        Pt_r = (self.k_PT * (self.et - self.et0) * nc_i**2)[:,None,None] * self.T * ds[:,None,None];
        
        Pb_r = (self.k_PB * ((self.eb - self.eb0) * (ndr**2)))[:,None,None] * ( (ndri * nc_i)[:,None,None] * np.cross(self.C[:,:,None], self.P, axis=1) - 3 * self.eb[:,None,None] * self.bSpline.dB[:,None,:] * self.bSpline.dq[:,0:3][:,:,None]) * ds[:,None,None];

        Pt_t = self.k_PT1 * (self.et - self.et0)[:,None,None] * (self.bSpline.B[:,None,:] * ndri[:,None,None]) * ds[:,None,None]
        
        Pot = Ps_r + Pt_r + Pb_r
        Pot4 = np.block([[Pot], [Pt_t]])
        res = np.trapz(Pot4, self.bSpline.u, axis=0)
        
        return res.flatten()
    
    def setPositionConstant(self, cpts, coordinates):
        k=1
        nc = np.sum(coordinates) #out
        L = np.zeros([nc,4*self.bSpline.ncpts])#out
        for m in np.arange(0,np.size(cpts)):
            coordinate = coordinates[(m)*4:(m)*4  +4]
            for i in np.arange(0,4):
                if coordinate[i]>0:
                    L[k-1][cpts[m] + (i)*self.bSpline.ncpts] = coordinate[i]
                    k = k + 1
        return L, nc
              
    def qd_qdd(self, t, zita):
        m = 4*self.bSpline.ncpts
        q = zita[0:m]
        qd = zita[m:]
        #print(t)
        self.bSpline.updateSpline(q);
        self.computeCPTtau()
        #External forces
        #TODO: Add it
        RT = self.Pot() - self.kv * qd + self.Fgrav
        #Calcolo l'accelerazione senza l'effetto del vincolo
        At = self.M_inv @ RT
        #Calcolo lambda
        lm = self.LML_inv @ (self.E_constraint - self.L_matrix @ At);
        #Calcolo di Ac
        Ac = self.M_inv @ self.L_matrix.T @ lm;
        A = At + Ac;
        qd_qdd = np.concatenate((qd, A))
        return qd_qdd  

    def simulate(self, tvec, solver):
        t0 = tvec[0]
        tf = tvec[-1]
        t_span = np.array([t0,tf])
        res = scipy.integrate.solve_ivp(self.qd_qdd, t_span, self.zita0, method=solver, t_eval=tvec)   
        return res
           

            

        
            
            

        

            
            
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == "__main__":
    a = 0 
    b = 2
    nCpts = 9
    du = 0.001
    x = np.linspace(a,b,nCpts)
    cpts = np.zeros([nCpts,4])
    cpts[:,0] = x
    E = 1e5
    D = 4e-3
    v = 0.33
    rho = 1e3
    nt = 10
    dt = 0.01
    t0 = 0
    tf = 1
    kv = 0.1
    L = 2
    #Create the DLO object
    dlo = DLO(L, D, E, v, rho, cpts, du, kv, nCpts, nt, dt, t0, tf)
    [L, nc] = dlo.setPositionConstant(np.array([0]), np.array([1,0,0,0]))
    dlo.setL(L)
    tvec = np.arange(0,2,0.01)
    res = dlo.simulate(tvec, 'RK23')
    
    
    
    
    
    