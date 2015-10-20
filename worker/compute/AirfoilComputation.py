from worker.compute.Computation import Computation
import csv


class AirfoilComputation(Computation):
    """
        Performs airfoil calculations on an xml file using the airfoil binary
    """

    def perform_computation(self, params, file_name):
        return self._read_tsv("../drag_ligt.m")[0]

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
                    file_content[i].append(t)

            return file_content
                    
                
                    
