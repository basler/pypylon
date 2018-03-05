# -----------------------------------------------------------------------------
#  (c) 2005 by Basler Vision Technologies
#  Section: Vision Components
#  Project: GenApiTest
#    Author:
#  $Header:
# -----------------------------------------------------------------------------

from genicam import Register


class CallbackObject(object):
    def __init__(self):
        self.m_Count = 0

    def Reset(self):
        self.m_Count = 0

    def Count(self):
        return self.m_Count

    def Callback(self, Node):
        self.m_Count += 1


# ! Helper class to test callbacks
class CallbackTestTarget(object):
    def __init__(self, node):
        self.m_Count = 0
        self.cb = Register(node.Node, self.Callback)

    # Reset the callback counter
    def Reset(self):
        self.m_Count = 0

    # the callback function to be registers
    def Callback(self, node):
        self.m_Count += 1

    # true if the callback has fired exactly once
    # If true Reset() is called implicitely */
    def HasFiredOnce(self):
        if self.m_Count == 1:
            self.Reset()
            return True
        else:
            print("WARNING : CCallbackTestTarget::HasFiredOnce : Count = ", self.Count())
            return False

    # true if the callback has nof fired
    def HasNotFired(self):
        if self.m_Count == 0:
            return True
        else:
            print("WARNING : CCallbackTestTarget::HasNotFired : Count = ", self.Count())
            return False

    # Tells the number of callbacks,

    def Count(self):
        return self.m_Count
