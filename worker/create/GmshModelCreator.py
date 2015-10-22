from worker.create.ModelCreator import ModelCreator
from subprocess import call
import re, sys, numpy as np
import uuid

class GmshModelCreator(ModelCreator):
    """
        Class to create a gmsh model based on parameters.
    """
    def create_model(self, params):
        """
        Creates a gmsh model based on given parameters.
        :param model.ModelParameters.ModelParameters params: ModelParameters
        :return: void
        """
        xs = np.linspace(0.0, 1.0, params.num_nodes)
        x, y = self._naca4(params.naca4[0],
                           params.naca4[1],
                           params.naca4[2],
                           params.naca4[3], xs)

        xa, ya = self._rot(x, y, params.angle)

        geo_filename = "a" + str(params.angle) + ".geo"
        msh_filename = "a" + str(params.angle) + ".msh"
        self._dat2gmsh(xa, ya, open(geo_filename, "w+"))

        create_gmsh_command = "gmsh -v 0 -nopopup -2 -o " + msh_filename + " " + geo_filename
        refine_gmsh_command = "gmsh -refine -v 0 " + msh_filename
        call(create_gmsh_command.split())
        for i in xrange(0, params.refinement_level):
            call(refine_gmsh_command.split())
            
        return msh_filename

    def _rot(self, x, y, a):
        ar = -a*3.14159/180
        xa = x*np.cos(ar)-y*np.sin(ar)
        ya = y*np.cos(ar)+x*np.sin(ar)
        return xa, ya

    def _naca4(self, n0, n1, n2, n3, x):
        m = n0 / 100.0
        p = n1 / 10.0
        t = (10 * n2 + n3) / 100.0
        c = 1.0
        # Closed trailing edge, change -0.1036 to -0.1015 for original def
        yt = 5*t*c*(0.2969*np.sqrt(x/c)+(-0.1260)*x/c+(-0.3516)*pow(x/c,2)+0.2843*pow(x/c,3)+(-0.1036)*pow(x/c,4))
        yc = x.copy()
        i = 0
        for xx in x:
            if xx < p*c:
                yc[i]=m*xx/p/p*(2*p-xx/c)
            else:
                yc[i]=m*(c-xx)/pow(1-p,2)*(1+xx/c-2*p)
            i += 1
        upper = yt+yc
        lower = -yt+yc
        xreturn = np.append(x,x[x.size-2:0:-1])
        yreturn = np.append(upper,lower[lower.size-2:0:-1])
        return xreturn,yreturn

    def _dat2gmsh(self, x, y, output):
        lc1 = 0.01
        lc2 = 1.00
        i = 0
        while i < x.size:
            output.write("Point(" + str(i+1) + ") = {" + str(x[i]) + "," + str(y[i])+",0,"+str(lc1)+"};\n")
            i += 1 
        ntot = x.size
        i = 1
        while i < ntot:
            output.write("Line(" + str(i) + ")={" + str(i) + "," + str(i+1) +"};\n")
            i += 1
        output.write("Line(" + str(ntot) + ")={" + str(ntot) + "," + "1};\n")
        output.write("Line Loop(" + str(ntot+1) + ")={ ")
        i = 1
        while i < ntot:
            output.write(str(i)+", ")
            i += 1 
        output.write(str(ntot) + "};\n")
      
        # Outer domain boundary
        output.write("Point(100000) = {-10,0,0,"+str(lc2)+"};\n")
        output.write("Point(101000) = {0,10,0,"+str(lc2)+"};\n")
        output.write("Point(102000) = {10,0,0,"+str(lc2)+"};\n")
        output.write("Point(103000) = {0,-10,0,"+str(lc2)+"};\n")
        output.write("Point(104000) = {0,0,0,"+str(lc2)+"};\n")
        output.write("Circle(105000) = {100000,104000,101000};\n")
        output.write("Circle(106000) = {101000,104000,102000};\n")
        output.write("Circle(107000) = {102000,104000,103000};\n")
        output.write("Circle(108000) = {103000,104000,100000};\n")
        output.write("Line Loop(109000) = {105000,106000,107000,108000};\n")
        output.write("Plane Surface(110000) = {109000,"+str(ntot+1)+"};\n")
