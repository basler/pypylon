// This file is used to wrap the Pylon SDK in a way that is compatible with Python.
#ifndef PYPYLON_NODEWRAPPER_DISABLE

%module pylon

%{
#include <pylon/PylonIncludes.h>
#include <pylon/Parameter.h>
#include <pylon/IntegerParameter.h>
#include <pylon/EnumParameter.h>
#include <pylon/BooleanParameter.h>
#include <pylon/CommandParameter.h>
#include <pylon/FloatParameter.h>
#include <pylon/StringParameter.h>
%}

// Use the Pylon SDK enums directly
using Pylon::EParameterInfo;
using Pylon::EIntegerValueCorrection;

#ifndef PYPYLON_PYLONDATAPROCESSING_MODULE
// Forward declarations for polymorphic handling
class PyParameterEx;
class PyIntegerEx;
class PyEnumerationEx;
class PyBooleanEx;
class PyCommandEx;
class PyFloatEx;
class PyStringEx;
#endif

// Enable polymorphic return types and mark factory as returning new objects
%newobject CreateParameterWrapperTyped;
%newobject CreateIntegerParameter;
%newobject CreateEnumerationParameter;
%newobject CreateBooleanParameter;
%newobject CreateCommandParameter;
%newobject CreateFloatParameter;
%newobject CreateStringParameter;

// Polymorphic return type handling for our wrapper classes
%typemap(out) PyParameterEx* CreateParameterWrapperTyped,
              PyParameterEx* CreateIntegerParameter,
              PyParameterEx* CreateEnumerationParameter,
              PyParameterEx* CreateBooleanParameter,
              PyParameterEx* CreateCommandParameter,
              PyParameterEx* CreateFloatParameter,
              PyParameterEx* CreateStringParameter
%{
    if (0 == $1)
    {
        $result = Py_None;
        Py_INCREF(Py_None);
    }
    else
    {
        // Determine the actual type and return the appropriate wrapper
        swig_type_info *outtype = 0;
        void * outptr = 0;
        
        // Check if it's one of our specific wrapper types
        if (dynamic_cast<PyIntegerEx*>($1))
        {
            outtype = $descriptor(PyIntegerEx*);
            outptr = dynamic_cast<PyIntegerEx*>($1);
        }
        else if (dynamic_cast<PyEnumerationEx*>($1))
        {
            outtype = $descriptor(PyEnumerationEx*);
            outptr = dynamic_cast<PyEnumerationEx*>($1);
        }
        else if (dynamic_cast<PyBooleanEx*>($1))
        {
            outtype = $descriptor(PyBooleanEx*);
            outptr = dynamic_cast<PyBooleanEx*>($1);
        }
        else if (dynamic_cast<PyCommandEx*>($1))
        {
            outtype = $descriptor(PyCommandEx*);
            outptr = dynamic_cast<PyCommandEx*>($1);
        }
        else if (dynamic_cast<PyFloatEx*>($1))
        {
            outtype = $descriptor(PyFloatEx*);
            outptr = dynamic_cast<PyFloatEx*>($1);
        }
        else if (dynamic_cast<PyStringEx*>($1))
        {
            outtype = $descriptor(PyStringEx*);
            outptr = dynamic_cast<PyStringEx*>($1);
        }
        else
        {
            // Fall back to base type
            outtype = $descriptor(PyParameterEx*);
            outptr = $1;
        }
        
        $result = SWIG_NewPointerObj(outptr, outtype, SWIG_POINTER_OWN);
    }
%}

#ifndef PYPYLON_PYLONDATAPROCESSING_MODULE
%inline %{

// Base wrapper class that delegates to actual Pylon parameter
class PyParameterEx {
private:
    GenApi::INode* node;
    std::string paramName;

public:
    PyParameterEx(GenApi::INode* n, const std::string& name) 
        : node(n), paramName(name) {}
    
    virtual ~PyParameterEx() {}
    
    bool IsWritable() {
        try {
            return GenApi::IsWritable(node);
        } catch (...) {
            return false;
        }
    }
    
    bool IsReadable() {
        try {
            return GenApi::IsReadable(node);
        } catch (...) {
            return false;
        }
    }
    
    bool IsValid() {
        try {
            return GenApi::IsAvailable(node);
        } catch (...) {
            return false;
        }
    }
    
    std::string GetParameterName() const { return paramName; }
    GenApi::INode* GetNode() { return node; }
};

// Integer parameter wrapper that creates and uses IIntegerEx
class PyIntegerEx : public PyParameterEx {
private:
    Pylon::CIntegerParameter pylonParam;

public:
    PyIntegerEx(GenApi::INode* n, const std::string& name) 
        : PyParameterEx(n, name), pylonParam(n) {}
    
    int64_t GetValue() {
        try {
            return pylonParam.GetValue();
        } catch (...) {
            throw std::runtime_error("Failed to get value for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetValue(int64_t value) {
        try {
            pylonParam.SetValue(value);
        } catch (...) {
            throw std::runtime_error("Failed to set value for parameter '" + GetParameterName() + "'");
        }
    }
    
    bool TrySetValue(int64_t value) {
        try {
            if (!IsWritable()) return false;
            pylonParam.TrySetValue(value);
            return true;
        } catch (...) {
            return false;
        }
    }
    
    bool TrySetValue(int64_t value, Pylon::EIntegerValueCorrection correction) {
        try {
            if (!IsWritable()) return false;
            pylonParam.TrySetValue(value, correction);
            return true;
        } catch (...) {
            return false;
        }
    }
    
    void SetValue(int64_t value, Pylon::EIntegerValueCorrection correction) {
        if (!TrySetValue(value, correction)) {
            throw std::runtime_error("Failed to set value " + std::to_string(value) + 
                                   " for parameter '" + GetParameterName() + "'");
        }
    }
    
    int64_t GetMin() {
        try {
            return pylonParam.GetMin();
        } catch (...) {
            throw std::runtime_error("Failed to get minimum value for parameter '" + GetParameterName() + "'");
        }
    }
    
    int64_t GetMax() {
        try {
            return pylonParam.GetMax();
        } catch (...) {
            throw std::runtime_error("Failed to get maximum value for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetToMinimum() {
        try {
            pylonParam.SetToMinimum();
        } catch (...) {
            throw std::runtime_error("Failed to set to minimum for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetToMaximum() {
        try {
            pylonParam.SetToMaximum();
        } catch (...) {
            throw std::runtime_error("Failed to set to maximum for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetValuePercentOfRange(double percent) {
        try {
            pylonParam.SetValuePercentOfRange(percent);
        } catch (...) {
            throw std::runtime_error("Failed to set percentage for parameter '" + GetParameterName() + "'");
        }
    }
    
    double GetValuePercentOfRange() {
        try {
            return pylonParam.GetValuePercentOfRange();
        } catch (...) {
            throw std::runtime_error("Failed to get percentage for parameter '" + GetParameterName() + "'");
        }
    }
};

// Enumeration parameter wrapper
class PyEnumerationEx : public PyParameterEx {
private:
    Pylon::CEnumParameter pylonParam;

public:
    PyEnumerationEx(GenApi::INode* n, const std::string& name) 
        : PyParameterEx(n, name), pylonParam(n) {}
    
    std::string GetValue() {
        try {
            return pylonParam.GetValue().c_str();
        } catch (...) {
            throw std::runtime_error("Failed to get value for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetValue(const std::string& value) {
        try {
            pylonParam.SetValue(value.c_str());
        } catch (...) {
            throw std::runtime_error("Failed to set value '" + value + "' for parameter '" + GetParameterName() + "'");
        }
    }
    
    bool CanSetValue(const std::string& value) {
        try {
            return pylonParam.CanSetValue(value.c_str());
        } catch (...) {
            return false;
        }
    }
    
    bool TrySetValue(const std::string& value) {
        try {
            return pylonParam.TrySetValue(value.c_str());
        } catch (...) {
            return false;
        }
    }
    
    std::string GetValueOrDefault(const std::string& defaultValue) {
        try {
            return pylonParam.GetValueOrDefault(defaultValue.c_str()).c_str();
        } catch (...) {
            return defaultValue;
        }
    }
};

// Boolean parameter wrapper
class PyBooleanEx : public PyParameterEx {
private:
    Pylon::CBooleanParameter pylonParam;

public:
    PyBooleanEx(GenApi::INode* n, const std::string& name) 
        : PyParameterEx(n, name), pylonParam(n) {}
    
    bool GetValue() {
        try {
            return pylonParam.GetValue();
        } catch (...) {
            throw std::runtime_error("Failed to get value for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetValue(bool value) {
        try {
            pylonParam.SetValue(value);
        } catch (...) {
            throw std::runtime_error("Failed to set value for parameter '" + GetParameterName() + "'");
        }
    }
    
    bool TrySetValue(bool value) {
        try {
            return pylonParam.TrySetValue(value);
        } catch (...) {
            return false;
        }
    }
    
    bool GetValueOrDefault(bool defaultValue) {
        try {
            return pylonParam.GetValueOrDefault(defaultValue);
        } catch (...) {
            return defaultValue;
        }
    }
};

// Command parameter wrapper
class PyCommandEx : public PyParameterEx {
private:
    Pylon::CCommandParameter pylonParam;

public:
    PyCommandEx(GenApi::INode* n, const std::string& name) 
        : PyParameterEx(n, name), pylonParam(n) {}
    
    void Execute() {
        try {
            pylonParam.Execute();
        } catch (...) {
            throw std::runtime_error("Failed to execute command '" + GetParameterName() + "'");
        }
    }
    
    bool TryExecute() {
        try {
            return pylonParam.TryExecute();
        } catch (...) {
            return false;
        }
    }
    
    bool IsDone() {
        try {
            return pylonParam.IsDone();
        } catch (...) {
            return false;
        }
    }
};

// Float parameter wrapper
class PyFloatEx : public PyParameterEx {
private:
    Pylon::CFloatParameter pylonParam;

public:
    PyFloatEx(GenApi::INode* n, const std::string& name) 
        : PyParameterEx(n, name), pylonParam(n) {}
    
    double GetValue() {
        try {
            return pylonParam.GetValue();
        } catch (...) {
            throw std::runtime_error("Failed to get value for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetValue(double value) {
        try {
            pylonParam.SetValue(value);
        } catch (...) {
            throw std::runtime_error("Failed to set value for parameter '" + GetParameterName() + "'");
        }
    }
    
    bool TrySetValue(double value) {
        try {
            return pylonParam.TrySetValue(value);
        } catch (...) {
            return false;
        }
    }
    
    double GetMin() {
        try {
            return pylonParam.GetMin();
        } catch (...) {
            throw std::runtime_error("Failed to get minimum value for parameter '" + GetParameterName() + "'");
        }
    }
    
    double GetMax() {
        try {
            return pylonParam.GetMax();
        } catch (...) {
            throw std::runtime_error("Failed to get maximum value for parameter '" + GetParameterName() + "'");
        }
    }
};

// String parameter wrapper
class PyStringEx : public PyParameterEx {
private:
    Pylon::CStringParameter pylonParam;

public:
    PyStringEx(GenApi::INode* n, const std::string& name) 
        : PyParameterEx(n, name), pylonParam(n) {}
    
    std::string GetValue() {
        try {
            return pylonParam.GetValue().c_str();
        } catch (...) {
            throw std::runtime_error("Failed to get value for parameter '" + GetParameterName() + "'");
        }
    }
    
    void SetValue(const std::string& value) {
        try {
            pylonParam.SetValue(value.c_str());
        } catch (...) {
            throw std::runtime_error("Failed to set value for parameter '" + GetParameterName() + "'");
        }
    }
    
    bool TrySetValue(const std::string& value) {
        try {
            return pylonParam.TrySetValue(value.c_str());
        } catch (...) {
            return false;
        }
    }
};

// Factory function to create appropriate parameter wrapper
PyParameterEx* CreateParameterWrapper(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) {
            return nullptr;
        }
        
        // Determine parameter type and create appropriate wrapper
        GenApi::EInterfaceType interfaceType = node->GetPrincipalInterfaceType();
        
        switch (interfaceType) {
            case GenApi::intfIInteger:
                return new PyIntegerEx(node, parameterName);
            case GenApi::intfIEnumeration:
                return new PyEnumerationEx(node, parameterName);
            case GenApi::intfIBoolean:
                return new PyBooleanEx(node, parameterName);
            case GenApi::intfICommand:
                return new PyCommandEx(node, parameterName);
            case GenApi::intfIFloat:
                return new PyFloatEx(node, parameterName);
            case GenApi::intfIString:
                return new PyStringEx(node, parameterName);
            default:
                return new PyParameterEx(node, parameterName);
        }
    } catch (...) {
        return nullptr;
    }
}

// Type-specific factory functions that SWIG can understand
PyIntegerEx* CreateIntegerParameter(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;   
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        return new PyIntegerEx(node, parameterName);
    } catch (...) {
        return nullptr;
    }
}

PyEnumerationEx* CreateEnumerationParameter(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        return new PyEnumerationEx(node, parameterName);
    } catch (...) {
        return nullptr;
    }
}

PyBooleanEx* CreateBooleanParameter(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        return new PyBooleanEx(node, parameterName);
    } catch (...) {
        return nullptr;
    }
}

PyCommandEx* CreateCommandParameter(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        return new PyCommandEx(node, parameterName);
    } catch (...) {
        return nullptr;
    }
}

PyFloatEx* CreateFloatParameter(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        return new PyFloatEx(node, parameterName);
    } catch (...) {
        return nullptr;
    }
}

PyStringEx* CreateStringParameter(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        return new PyStringEx(node, parameterName);
    } catch (...) {
        return nullptr;
    }
}

// Enhanced factory that returns the right type without casting
PyParameterEx* CreateParameterWrapperTyped(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        if (!nodemap) return nullptr;
        GenApi::INode* node = nodemap->GetNode(parameterName.c_str());
        if (!node) return nullptr;
        
        GenApi::EInterfaceType interfaceType = node->GetPrincipalInterfaceType();
        
        switch (interfaceType) {
            case GenApi::intfIInteger:
                return new PyIntegerEx(node, parameterName);
            case GenApi::intfIEnumeration:
                return new PyEnumerationEx(node, parameterName);
            case GenApi::intfIBoolean:
                return new PyBooleanEx(node, parameterName);
            case GenApi::intfICommand:
                return new PyCommandEx(node, parameterName);
            case GenApi::intfIFloat:
                return new PyFloatEx(node, parameterName);
            case GenApi::intfIString:
                return new PyStringEx(node, parameterName);
            default:
                return new PyParameterEx(node, parameterName);
        }
    } catch (...) {
        return nullptr;
    }
}

// Safe version that returns nullptr on failure
PyParameterEx* CreateParameterWrapperSafe(GenApi::INodeMap* nodemap, const std::string& parameterName) {
    try {
        return CreateParameterWrapperTyped(nodemap, parameterName);
    } catch (...) {
        return nullptr;
    }
}

%}
#endif // PYPYLON_PYLONDATAPROCESSING_MODULE

#endif // PYPYLON_NODEWRAPPER_DISABLE 