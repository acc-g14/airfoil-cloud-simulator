from worker.compute.Computation import Computation
from subprocess import call
import csv


class AirfoilComputation(Computation):
    """
        Performs airfoil calculations on an xml file using the airfoil binary
    """

    def perform_computation(self, params, file_name):
        #airfoil_command = "./airfoil 1 0.0001 10 1 a0.xml"
        #call(airfoil_command.split())
        call(["./airfoil", 
              str(params.num_samples), 
              str(params.viscosity),
              str(params.speed),
              str(params.time),
              file_name])
        tsv = self._read_tsv("results/drag_ligt.m")
        avr_lift = sum(tsv[1])/len(tsv[1])
        avr_drag = sum(tsv[2])/len(tsv[2])
        
        return {"lift": avr_lift, "drag": avr_drag}

    def _read_tsv(self, file_name):
        with open(file_name) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter = "\t")
            file_content = None
            for i, line in enumerate(tsvreader):
                if i == 0:
                    l = len(line)
                    file_content = [[] for x in range(l)]
                    continue
                for i, t in enumerate(line):
                    file_content[i].append(float(t))

            return file_content
                    
                
                    
