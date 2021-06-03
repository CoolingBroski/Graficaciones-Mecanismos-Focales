from mayavi import mlab
import numpy as np

#nj = 30j # control de numero de puntos
n = 30

# Theta angulo vertical a partir del eje Z
# Phi angulo horizontal a partir del eje X
#[phi,theta] = np.mgrid[0:2*np.pi:nj,0:np.pi:nj]
phi = np.linspace(0, 2*np.pi, n)
theta = np.linspace(0, np.pi, n)
r = 1 # Radio del mecanismo focal hipotetico

u = np.zeros((n,n))
pos1 = np.zeros((n,n))
pos2 = np.zeros((n,n))
pos3 = np.zeros((n,n))

x = np.zeros((n,n))
y = np.zeros((n,n))
z = np.zeros((n,n))


for i, t in enumerate(theta):
    for j, p in enumerate(phi):
        u[i,j] = np.sin(2*t)*np.cos(p)
        pos1[i,j] = r*np.sin(t)*np.cos(p)
        pos2[i,j] = r*np.sin(t)*np.sin(p)
        pos3[i,j] = r*np.cos(t)
        
        x[i,j] = u[i,j]*np.sin(t)*np.cos(p)
        y[i,j] = u[i,j]*np.sin(t)*np.sin(p)
        z[i,j] = u[i,j]*np.cos(t)
        
        
escala = 0.5

pos1_lineal = pos1.reshape(n*n)
pos2_lineal = pos2.reshape(n*n)
pos3_lineal = pos3.reshape(n*n)

x = x*escala
y = y*escala
z = z*escala

x = x.reshape(n*n)
y = y.reshape(n*n)
z = z.reshape(n*n)


mask = u <= 0
u = u.reshape(n*n)
mask_lineal = u < 0 # Mascara para valores de u negativos


fig = mlab.figure(size=(600,600))

# Tiene que recibir argumentos bidimensionales tales que cada renglon y columna
# corresponden a distintas combinaciones de theta y phi

# Las mascaras convencionales solo funcionan para arreglos unidimensionales

# Cuadrantes del mismo color diferenciados por signo de z

mask1 = (pos3 >= 0)*mask
mask2 = (pos3 <= 0)*mask
mask3 = (pos3 >= 0)*~mask
mask4 = (pos3 <= 0)*~mask

pos1col1_1, pos2col1_1, pos3col1_1, pos1col1_2, pos2col1_2, pos3col1_2, pos1col2_1, pos2col2_1, pos3col2_1, pos1col2_2, pos2col2_2, pos3col2_2 = (np.zeros((n,n)) for i in range(12))

pos1col1_1[mask1] = pos1[mask1]
pos2col1_1[mask1] = pos2[mask1]
pos3col1_1[mask1] = pos3[mask1]

pos1col1_2[mask2] = pos1[mask2]
pos2col1_2[mask2] = pos2[mask2]
pos3col1_2[mask2] = pos3[mask2]

pos1col2_1[mask3] = pos1[mask3]
pos2col2_1[mask3] = pos2[mask3]
pos3col2_1[mask3] = pos3[mask3]


pos1col2_2[mask4] = pos1[mask4]
pos2col2_2[mask4] = pos2[mask4]
pos3col2_2[mask4] = pos3[mask4]

# 4 mesh para cada cuadrante para no tener conexiones raras

mlab.mesh(pos1col1_1, pos2col1_1, pos3col1_1, color=(1,1,1))
mlab.mesh(pos1col1_2, pos2col1_2, pos3col1_2, color=(1,1,1))

mlab.mesh(pos1col2_1, pos2col2_1, pos3col2_1, color=(0.5,0.5,0.5))
mlab.mesh(pos1col2_2, pos2col2_2, pos3col2_2, color=(0.5,0.5,0.5))

pos1_lineal[mask_lineal]+=-x[mask_lineal]
pos2_lineal[mask_lineal]+=-y[mask_lineal]
pos3_lineal[mask_lineal]+=-z[mask_lineal]


# Por defecto, la libreria escala los vectores dependiendo del espaciado para que no haya sobreposicion
# asi que hay que especificar un scale_factor arbitrario para anular ese comportamiento

mlab.quiver3d(pos1_lineal, pos2_lineal, pos3_lineal, x, y, z, line_width=30, color=(0,0,0), scale_factor=1, figure=fig, mode='arrow')




mlab.show()