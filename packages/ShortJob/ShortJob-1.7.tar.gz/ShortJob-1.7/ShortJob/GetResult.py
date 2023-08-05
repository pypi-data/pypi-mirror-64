from ROOT import TTree, TFile
from array import array


class GetResult:
    """
    Reqiure ROOT
    How:
        The program tries to find any pattern "name value" in the log file
        For example:
            alpha 0.321
        In this case, the "alpha" is assigned to be 0.021.
            beta 0.01 0.321 +/- 0.001
        In this case, the "beta" is assigned to be 0.321 +/- 0.001, while
        0.001 is the uncertainty
        * Warrn: the new value will overwrite the old one.
    Example:
        info = GetResult.("fit.log")
        fcn = info.FCN()
        tmpArgValue = info.GetVal("alpha")
    """
    def __init__(self, log="log0000"):
        self._log = log

    def SetLog(self, log):
        """Set the log file
        Args:
        log(str): the name of log file
        Returns:
          void
        """
        self._log = log

    def FCN(self):
        """obtain the FCN of likelihood fit, FCN = -log(L)
        Args:
          none
        Returns:
          FCN(double): the minimum -log(L)
        """
        for line in open(self._log):
            if "RooFitResult:" not in line:
                continue
            ll = line.split()
            ii = ll.index("value:")
            return float(ll[ii + 1].split(",")[0])

    def GetVal(self, var="sigma"):
        """ get the value of "var" from the log file
        Args:
           var(str): the name of variable
        Returns:
           value(double): the value of `var`
        """
        ll = []
        ll2 = []
        for line in open(self._log):
            if len(line.split()) == 0:
                continue
            if line.split()[0] == var and r"+/-" in line:
                # print line
                ll = line.split()
            if line.split()[0] == var and len(line.split()) == 2:
                ll2 = line.split()
                # break
        if len(ll) != 0:
            ii = ll.index(r"+/-")
            return float(ll[ii - 1])
        if len(ll2) != 0:
            return float(ll2[-1])
        return self.FF(var)
        return 0.0

    def GetError(self, var="sigma"):
        """ get the value of uncertainty of "var" from the log file
        Args:
           var(str): the name of variable
        Returns:
           value(double): the uncertainty of `var`
        """
        ll = []
        ll2 = []
        for line in open(self._log):
            if len(line.split()) == 0:
                continue
            if line.split()[0] == var and r"+/-" in line:
                # print line
                ll = line.split()
            if line.split()[0] == var and len(line.split()) == 2:
                ll2 = line.split()
                # break
        if len(ll) != 0:
            ii = ll.index(r"+/-")
            return float(ll[ii + 1])
        if len(ll2) != 0:
            return float(ll2[-1])
        return self.FF(var)
        return 0.0

    def WriteToFile(self, inputval=[], output="out.root"):
        """write a list to root file, the tree name is default as "sig",
         the branch is default as "val"
        Args:
            inputval(list): the input list, all element will convert into
              double
            output(str): the name of root file, the default value is "out.root"
        Returns:
            void
        """
        fout = TFile(output, "recreate")
        tout = TTree("sig", "")
        val = array("d", [0.0])
        tout.Branch("val", val, "val/D")
        for i in inputval:
            val[0] = i
            tout.Fill()
        tout.Write()
        fout.Close()
