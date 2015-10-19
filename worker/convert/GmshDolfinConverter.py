from worker.convert.Converter import Converter
from subprocess import call

class GmshDolfinConverter(Converter):
    """
        Class to convert from Gmsh format to dolfin xml format.
    """

    def convert(self, f):
        dotIndex = f.rindex(".msh") #will throw exception if .msh is not found
        xmlFileName = f[:dotIndex] + ".xml"
        command = "dolfin-convert " + f + " " + xmlFileName
        call(command.split())
        return xmlFileName
