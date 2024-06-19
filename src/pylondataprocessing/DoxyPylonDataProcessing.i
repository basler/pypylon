
// File: index.xml

// File: struct_pylon_1_1_data_processing_1_1_array_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::ArrayParameterName "

Defines an array parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::ArrayParameterName::ArrayParameterName "
Pylon::DataProcessing::ArrayParameterName::ArrayParameterName";

// File: struct_pylon_1_1_data_processing_1_1_boolean_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::BooleanParameterName "

Defines a Boolean parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::BooleanParameterName::BooleanParameterName "
Pylon::DataProcessing::BooleanParameterName::BooleanParameterName";

// File: class_pylon_1_1_data_processing_1_1_c_builders_recipe.xml


%feature("docstring") Pylon::DataProcessing::CBuildersRecipe "

This class can be used to build recipes programmatically and run them.  

C++ includes: BuildersRecipe.h
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::CBuildersRecipe "
Pylon::DataProcessing::CBuildersRecipe::CBuildersRecipe
Creates a `CBuildersRecipe` object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::~CBuildersRecipe "
Pylon::DataProcessing::CBuildersRecipe::~CBuildersRecipe
Destroys a `CBuildersRecipe` object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetAvailableVToolTypeIDs "
Pylon::DataProcessing::CBuildersRecipe::GetAvailableVToolTypeIDs
Retrieves a list of type IDs of all available vTool types and returns the number
of available types.  

Parameters
----------
* `vToolTypeIDs` :  
    A string list to store the available vTools' type IDs in.  

post:  

    *   `vToolTypeIDs` contains the type IDs of the available vTool types in
        alphabetical order.  

\\error Doesn't throw C++ exceptions, except when memory allocation fails.  

Returns
-------
The number of available type IDs.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetVToolDisplayNameForTypeID "
Pylon::DataProcessing::CBuildersRecipe::GetVToolDisplayNameForTypeID
Retrieves the display name of the vTool type identified by the given type ID.  

Parameters
----------
* `vToolTypeID` :  
    The type ID of the vTool type whose display name is retrieved.  

pre:  

    *   `vToolTypeID` refers to an available vTool type (use
        `GetAvailableVToolTypeIDs()` to get a list of all available vTool type
        IDs).  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
The display name of the vTool type identified by `vToolTypeID`.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddVTool "
Pylon::DataProcessing::CBuildersRecipe::AddVTool
Creates a vTool of a specific type and adds it to the recipe with the given
identifier.  

Parameters
----------
* `identifier` :  
    Identifier for the vTool instance that can be used to identify the vTool
    instance in the recipe.  
* `vToolTypeID` :  
    Type ID specifying the vTool type of the vTool to be added.  

pre:  

    *   `identifier` is a valid C++ identifier and must not start with an
        underscore.  
    *   No vTool with the same `identifier` already exists in the recipe.  
    *   `vToolTypeID` refers to an available vTool type (use
        `GetAvailableVToolTypeIDs()` to get a list of all available vTool type
        IDs).  
    *   Your license allows instantiating the requested vTool type from the Data
        Processing SDK.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   A new vTool of the type identified by `vToolTypeID` has been added to
        the recipe with the identifier `identifier`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddVTool "
Pylon::DataProcessing::CBuildersRecipe::AddVTool
Creates a vTool of a specific type and adds it to the recipe with an
automatically generated identifier.  

Parameters
----------
* `vToolTypeID` :  
    Type ID specifying the vTool type of the vTool to be added.  

pre:  

    *   `vToolTypeID` refers to an available vTool type (use
        `GetAvailableVToolTypeIDs()` to get a list of all available vTool type
        IDs).  
    *   Your license allows instantiating the requested vTool type from the Data
        Processing SDK.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   A new vTool of the type identified by `vToolTypeID` has been added to
        the recipe with a unique identifier.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
Returns the identifier of the newly created vTool instance.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetVToolIdentifiers "
Pylon::DataProcessing::CBuildersRecipe::GetVToolIdentifiers
Retrieves a list of the identifiers of all vTools that exist in the recipe and
returns the total number of vTools.  

Parameters
----------
* `identifiers` :  
    A string list to store the vTool identifiers in.  

post:  

    *   `identifiers` contains the identifiers of all vTools in the recipe in
        alphabetical order.  

\\error Doesn't throw C++ exceptions, except when memory allocation fails.  

Returns
-------
The number of vTools contained in the recipe.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetVToolTypeID "
Pylon::DataProcessing::CBuildersRecipe::GetVToolTypeID
Returns the type ID of the vTool instance with the given identifier.  

Parameters
----------
* `identifier` :  
    Identifier of the vTool whose type ID is retrieved.  

pre:  

    *   The recipe contains a vTool with the identifier `identifier`.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
The type ID of the vTool instance with the identifier `identifier`.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::HasVTool "
Pylon::DataProcessing::CBuildersRecipe::HasVTool
Checks whether the recipe contains a vTool with a specific identifier.  

Parameters
----------
* `identifier` :  
    Identifier of the vTool.  

\\error Doesn't throw C++ exceptions.  

Returns
-------
Returns true if the recipe contains a vTool with the identifier `identifier`,
otherwise false.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RenameVTool "
Pylon::DataProcessing::CBuildersRecipe::RenameVTool
Assigns a new identifier to an existing vTool instance.  

Parameters
----------
* `oldIdentifier` :  
    The identifier of the vTool to be renamed.  
* `newIdentifier` :  
    The new identifier of the vTool.  

pre:  

    *   The recipe contains a vTool with the identifier `oldIdentifier`.  
    *   `newIdentifier` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe doesn't contain a vTool with the identifier `newIdentifier`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The vTool with the identifier `oldIdentifier` has been renamed to
        `newIdentifier`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RemoveVTool "
Pylon::DataProcessing::CBuildersRecipe::RemoveVTool
Removes an existing vTool instance. Any connections attached to any of the
vTool's pins will be removed as well.  

Parameters
----------
* `identifier` :  
    The identifier of the vTool to be removed.  

pre:  

    *   The recipe contains a vTool with the identifier `identifier`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The vTool with the identifier `identifier` has been removed from the
        recipe.  
    *   Any connections attached to any of the vTool's pins have been removed
        from the recipe.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddInput "
Pylon::DataProcessing::CBuildersRecipe::AddInput
Adds an input of a specific type to the recipe with a given identifier.  

Parameters
----------
* `inputFullName` :  
    The identifier of the new input.  
* `inputDataType` :  
    Data type of the new input.  
* `inputContainerType` :  
    Container type of the new input.  

pre:  

    *   `inputFullName` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe doesn't contain an input with the identifier `inputFullName`.  
    *   `inputDataType` refers to an actual data type and is not equal to
        `VariantDataType_Composite`, `VariantDataType_None`, or
        `VariantDataType_Unsupported`.  
    *   `inputContainerType` refers to an actual container type and is not equal
        to `VariantContainerType_Unsupported`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   An input with the type identified by `inputDataType` and
        `inputContainerType` has been added to the recipe with the identifier
        `inputFullName`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddInput "
Pylon::DataProcessing::CBuildersRecipe::AddInput
Adds an input of a specific type to the recipe with an automatically generated
identifier.  

Parameters
----------
* `inputDataType` :  
    Data type of the new input.  
* `inputContainerType` :  
    Container type of the new input.  

pre:  

    *   `inputDataType` refers to an actual data type and is not equal to
        `VariantDataType_Composite`, `VariantDataType_None`, or
        `VariantDataType_Unsupported`.  
    *   `inputContainerType` refers to an actual container type and is not equal
        to `VariantContainerType_Unsupported`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   An input with the type identified by `inputDataType` and
        `inputContainerType` has been added to the recipe.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
Returns the automatically generated identifier of the newly created input.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RenameInput "
Pylon::DataProcessing::CBuildersRecipe::RenameInput
Assigns a new identifier to an existing input.  

Parameters
----------
* `oldInputFullName` :  
    The identifier of the input to be renamed.  
* `newInputFullName` :  
    The new identifier of the input.  

pre:  

    *   The recipe contains an input with the identifier `oldInputFullName`.  
    *   `newInputFullName` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe doesn't contain an input with the identifier
        `newInputFullName`.  
    *   The input with the given identifier isn't connected.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The input with the identifier `oldInputFullName` has been renamed to
        `newInputFullName`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetInputNames "
Pylon::DataProcessing::CBuildersRecipe::GetInputNames
Retrieves a list of the identifiers of all inputs that exist in the recipe and
returns the total number of inputs.  

Parameters
----------
* `inputFullNames` :  
    A string list to store the input identifiers in.  

post:  

    *   `inputFullNames` contains the identifiers of all inputs of the recipe in
        the order that they have been added.  

\\error Doesn't throw C++ exceptions, except when memory allocation fails.  

Returns
-------
The number of inputs that the recipe currently has.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RemoveInput "
Pylon::DataProcessing::CBuildersRecipe::RemoveInput
Removes an input from the recipe. If any connections are attached to this input,
they will be removed as well.  

Parameters
----------
* `inputFullName` :  
    The identifiers of the input to be removed.  

pre:  

    *   The recipe has an input with the identifier `inputFullName`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The input with the identifier `inputFullName` has been removed from the
        recipe.  
    *   Any connections attached to the removed input have been removed.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddOutput "
Pylon::DataProcessing::CBuildersRecipe::AddOutput
Adds an output of a specific type to the recipe with a given identifier.  

Parameters
----------
* `outputFullName` :  
    The identifier of the new output.  
* `outputDataType` :  
    Data type of the new output.  
* `outputContainerType` :  
    Container type of the new output.  

pre:  

    *   `outputFullName` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe doesn't contain an output with the identifier
        `outputFullName`.  
    *   `outputDataType` refers to an actual data type and is not equal to
        `VariantDataType_Composite`, `VariantDataType_None`, or
        `VariantDataType_Unsupported`.  
    *   `outputContainerType` refers to an actual container type and is not
        equal to `VariantContainerType_Unsupported`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   An output with the type identified by `outputDataType` and
        `outputContainerType` has been added to the recipe with the identifier
        `outputFullName`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddOutput "
Pylon::DataProcessing::CBuildersRecipe::AddOutput
Adds an output of a specific type to the recipe with an automatically generated
identifier.  

Parameters
----------
* `outputDataType` :  
    Data type of the new output.  
* `outputContainerType` :  
    Container type of the new output.  

pre:  

    *   `outputDataType` refers to an actual data type and is not equal to
        `VariantDataType_Composite`, `VariantDataType_None`, or
        `VariantDataType_Unsupported`.  
    *   `outputContainerType` refers to an actual container type and is not
        equal to `VariantContainerType_Unsupported`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   An output with the type identified by `outputDataType` and
        `outputContainerType` has been added to the recipe.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
Returns the automatically generated identifier of the newly created output.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RenameOutput "
Pylon::DataProcessing::CBuildersRecipe::RenameOutput
Assigns a new identifier to an existing output.  

Parameters
----------
* `oldOutputFullName` :  
    The identifier of the output to be renamed.  
* `newOutputFullName` :  
    The new identifier of the output.  

pre:  

    *   The recipe contains an output with the identifier `oldOutputFullName`.  
    *   `newOutputFullName` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe doesn't contain an output with the identifier
        `newOutputFullName`.  
    *   The output with the given identifier isn't connected.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The output with the identifier `oldOutputFullName` has been renamed to
        `newOutputFullName`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RemoveOutput "
Pylon::DataProcessing::CBuildersRecipe::RemoveOutput
Removes an output from the recipe. If a connection is attached to this output,
it will be removed as well.  

Parameters
----------
* `outputFullName` :  
    The identifier of the output to be removed.  

pre:  

    *   The recipe contains an output with the identifier `outputFullName`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The output with the identifier `outputFullName` has been removed from
        the recipe.  
    *   If a connection was attached to this output, it has been removed from
        the recipe.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddConnection "
Pylon::DataProcessing::CBuildersRecipe::AddConnection
Creates a connection between vTool pins and/or recipe inputs or outputs with a
given identifier.  

Parameters
----------
* `identifier` :  
    Identifier to uniquely identify the connection in the recipe.  
* `sourceFullName` :  
    Full name of the source of the connection in the form
    \"[vToolIdentifier].[vToolOutputIdentifier]\" (e.g., \"Camera.Image\" or
    \"myVTool.Point\"). To create a connection from a recipe input, use
    <RecipeInput> as the vToolIdentifier (e.g., \"\\<RecipeInput\\>.Image\").  
* `destinationFullName` :  
    Full name of the destination of the connection
    \"[vToolIdentifier].[vToolInputIdentifier]\" (e.g.,
    \"ImageFormatConverter.Image\" or \"myVTool.Point\"). To create a connection
    to a recipe output, use <RecipeOutput> as the vToolIdentifier (e.g.,
    \"\\<RecipeOutput\\>.Image\").  
* `queueMode` :  
    The queue mode for the connection queue (see `EQueueMode` for all available
    queue modes). The default value is QueueMode_Blocking.  
* `maxQueueSize` :  
    The initial maximum size of the connection queue. The default value is 1. If
    `queueMode` is `QueueMode_Unlimited`, this has no effect.  

pre:  

    *   `identifier` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe must not contain a connection with the same `identifier`.  
    *   `sourceFullName` must specify the full name of an existing vTool output
        pin or an existing recipe input.  
    *   `destinationFullName` must specify the full name of an existing vTool
        input pin or an existing recipe output.  
    *   `sourceFullName` and `destinationFullName` must have compatible data
        types.  
    *   `maxQueueSize` must be greater than 0 and lower than the maximum value
        of size_t.  
    *   The destination must not be connected.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   A new connection with the identifier `identifier` has been created in
        the recipe connecting `sourceFullName` to `destinationFullName`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::AddConnection "
Pylon::DataProcessing::CBuildersRecipe::AddConnection
Creates a connection between vTool pins and/or recipe inputs or outputs with an
automatically generated identifier.  

Parameters
----------
* `sourceFullName` :  
    Full name of the source of the connection in the form
    \"[vToolIdentifier].[vToolOutputIdentifier]\" (e.g., \"Camera.Image\" or
    \"myVTool.Point\"). To create a connection from a recipe input, use
    <RecipeInput> as the vToolIdentifier (e.g., \"\\<RecipeInput\\>.Image\").  
* `destinationFullName` :  
    Full name of the destination of the connection
    \"[vToolIdentifier].[vToolInputIdentifier]\" (e.g.,
    \"ImageFormatConverter.Image\" or \"myVTool.Point\"). To create a connection
    to a recipe output, use <RecipeOutput> as the vToolIdentifier (e.g.,
    \"\\<RecipeOutput\\>.Image\").  
* `queueMode` :  
    The queue mode for the connection queue (see `EQueueMode` for all available
    queue modes). The default value is QueueMode_Blocking.  
* `maxQueueSize` :  
    The initial maximum size of the connection queue. The default value is 1. If
    `queueMode` is `QueueMode_Unlimited`, this has no effect.  

pre:  

    *   `sourceFullName` must specify the full name of an existing vTool output
        pin or an existing recipe input.  
    *   `destinationFullName` must specify the full name of an existing vTool
        input pin or an existing recipe output.  
    *   `sourceFullName` and `destinationFullName` must have compatible data
        types.  
    *   `maxQueueSize` must be greater than 0 and lower than the maximum value
        of size_t.  
    *   The destination must not be connected.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   A new connection has been created in the recipe connecting
        `sourceFullName` to `destinationFullName`.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
Returns the identifier of the newly created connection.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetConnectionMaxQueueSize "
Pylon::DataProcessing::CBuildersRecipe::GetConnectionMaxQueueSize
Gets the current maximum queue size for a connection identified by its
identifier.  

Parameters
----------
* `identifier` :  
    Identifier of the connection whose maximum queue size is retrieved.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
The maximum queue size of the connection with the identifier `identifier`.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetConnectionSource "
Pylon::DataProcessing::CBuildersRecipe::GetConnectionSource
Gets the full name of a connection's source.  

Parameters
----------
* `identifier` :  
    Identifier of the connection.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
The full name of the connection's source.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetConnectionDestination "
Pylon::DataProcessing::CBuildersRecipe::GetConnectionDestination
Gets the full name of a connection's destination.  

Parameters
----------
* `identifier` :  
    Identifier of the connection.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
The full name of the connection's destination.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetConnectionQueueMode "
Pylon::DataProcessing::CBuildersRecipe::GetConnectionQueueMode
Gets the current queue mode for a connection identified by its identifier.  

Parameters
----------
* `identifier` :  
    Identifier of the connection whose queue mode is retrieved.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  

\\error Throws an exception if the preconditions aren't met.  

Returns
-------
The queue mode of the connection with the identifier `identifier`.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::HasConnection "
Pylon::DataProcessing::CBuildersRecipe::HasConnection
Checks whether the recipe contains a connection with a specific identifier.  

Parameters
----------
* `identifier` :  
    Identifier of the connection.  

\\error Doesn't throw C++ exceptions.  

Returns
-------
Returns true if the recipe contains a connection with the identifier
`identifier`, otherwise false.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::GetConnectionIdentifiers "
Pylon::DataProcessing::CBuildersRecipe::GetConnectionIdentifiers
Retrieves a list of the identifiers of all connections that exist in the recipe
and returns the total number of connections.  

Parameters
----------
* `identifiers` :  
    A string list to store the connection identifiers in.  

post:  

    *   `identifiers` contains the identifiers of all connections in the recipe
        in alphabetical order.  

\\error Doesn't throw C++ exceptions, except when memory allocation fails.  

Returns
-------
The number of connections contained in the recipe.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RenameConnection "
Pylon::DataProcessing::CBuildersRecipe::RenameConnection
Assigns a new identifier to an existing connection.  

Parameters
----------
* `oldIdentifier` :  
    The identifier of the connection to be renamed.  
* `newIdentifier` :  
    The new identifier of the connection.  

pre:  

    *   The recipe contains a connection with the identifier `oldIdentifier`.  
    *   `newIdentifier` is a valid C++ identifier and must not start with an
        underscore.  
    *   The recipe doesn't contain a connection with the identifier
        `newIdentifier`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The connection with the identifier `oldIdentifier` has been renamed to
        `newIdentifier`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::SetConnectionSettings "
Pylon::DataProcessing::CBuildersRecipe::SetConnectionSettings
Modifies the settings of an existing connection.  

Parameters
----------
* `identifier` :  
    The identifier of the connection to be modified.  
* `queueMode` :  
    The new queue mode of the connection.  
* `maxQueueSize` :  
    The new maximum queue size of the connection.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  
    *   `maxQueueSize` must be greater than 0 and lower than the maximum value
        of size_t.  

post:  

    *   The connection's queue mode has been set to `queueMode`.  
    *   The connection's maximum queue size has been set to `maxQueueSize`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::SetConnectionQueueMode "
Pylon::DataProcessing::CBuildersRecipe::SetConnectionQueueMode
Modifies the queue mode of an existing connection.  

Parameters
----------
* `identifier` :  
    The identifier of the connection to be modified.  
* `queueMode` :  
    The new queue mode of the connection.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The connection's queue mode has been set to `queueMode`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::SetConnectionMaxQueueSize "
Pylon::DataProcessing::CBuildersRecipe::SetConnectionMaxQueueSize
Modifies the maximum queue size of an existing connection.  

Parameters
----------
* `identifier` :  
    The identifier of the connection to be modified.  
* `maxQueueSize` :  
    The new maximum queue size of the connection.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  
    *   `maxQueueSize` must be greater than 0 and lower than the maximum value
        of size_t.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The connection's maximum queue size has been set to `maxQueueSize`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::RemoveConnection "
Pylon::DataProcessing::CBuildersRecipe::RemoveConnection
Removes an existing connection.  

Parameters
----------
* `identifier` :  
    The identifier of the connection to be removed.  

pre:  

    *   The recipe contains a connection with the identifier `identifier`.  
    *   The recipe hasn't been started (i.e., IsStarted() must return false).  

post:  

    *   The connection with the identifier `identifier` has been removed from
        the recipe.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::Save "
Pylon::DataProcessing::CBuildersRecipe::Save
Writes the recipe to a recipe file.  

Parameters
----------
* `fileName` :  
    Path to the file to store the recipe in. This can be an absolute or a
    relative path. If it is relative, the file will be saved relative to your
    current working directory.  

pre:  

    *   `fileName` is a writable file path and a valid file path for your
        platform.  

post:  

    *   The recipe has been written to the specified file path and can be loaded
        using the `CRecipe` API.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CBuildersRecipe::ResetToEmpty "
Pylon::DataProcessing::CBuildersRecipe::ResetToEmpty
Resets the recipe by removing all vTools, inputs, outputs, connections, and
observers. Stop() is called implicitly with an infinite timeout if the recipe
has been started.  

post:  

    *   The recipe is empty, i.e., all vTools, inputs, outputs, connections, and
        observers have been removed.  
    *   `IsStarted()` returns false.  
    *   `IsLoaded()` returns true.  
    *   The recipe can be modified.  

\\error Throws an exception if the preconditions aren't met.  
";

// File: class_pylon_1_1_data_processing_1_1_c_callable_event_observer.xml


%feature("docstring") Pylon::DataProcessing::CCallableEventObserver "

A class that wraps a callable (function pointer or functor) to be used as an
event observer of a `CRecipe`.  

\\threading The observer, and therefore the callable, is called from multiple
internal threads of the `CRecipe`.  

C++ includes: CallableEventObserver.h
";

%feature("docstring") Pylon::DataProcessing::CCallableEventObserver::CCallableEventObserver "
Pylon::DataProcessing::CCallableEventObserver::CCallableEventObserver
Constructs an event observer with a given callable.  

The callable must be invocable with the following signature: void (CRecipe&
recipe, const CEventData* pEvents, size_t numEvents)  

Example:  

Parameters
----------
* `callable` :  
    The callable to invoke.  
* `autoDelete` :  
    If true, the object will be deleted automatically when it is unregistered
    from the recipe.  

pre:  

    *   The callable must be valid (e.g., not a nullptr)  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CCallableEventObserver::~CCallableEventObserver "
Pylon::DataProcessing::CCallableEventObserver::~CCallableEventObserver";

%feature("docstring") Pylon::DataProcessing::CCallableEventObserver::OnEventSignaled "
Pylon::DataProcessing::CCallableEventObserver::OnEventSignaled
This method is called when the graph of the `CRecipe` detects an event, e.g., an
error change of a vtool.  

Parameters
----------
* `recipe` :  
    The recipe that produced the output.  
* `pEvents` :  
    List of event infos as plain C array.  
* `numEvents` :  
    Number of entries in that list.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

%feature("docstring") Pylon::DataProcessing::CCallableEventObserver::OnDeregistered "
Pylon::DataProcessing::CCallableEventObserver::OnDeregistered
This method is called when the event observer is deregistered from the recipe.
It can be used to delete the event observer by overloading the method. The
default implementation of this method does nothing.  

Parameters
----------
* `recipe` :  
    The recipe that the observer is deregistered from.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

// File: class_pylon_1_1_data_processing_1_1_c_callable_output_observer.xml


%feature("docstring") Pylon::DataProcessing::CCallableOutputObserver "

A class that wraps a callable (function pointer or functor) to be used as an
output observer of a `CRecipe`.  

\\threading The observer, and therefore the callable, is called from multiple
internal threads of the `CRecipe`.  

C++ includes: CallableOutputObserver.h
";

%feature("docstring") Pylon::DataProcessing::CCallableOutputObserver::CCallableOutputObserver "
Pylon::DataProcessing::CCallableOutputObserver::CCallableOutputObserver
Constructs an output observer with a given callable.  

The callable must be invocable with the following signature: void (CRecipe&
recipe, CVariantContainer value, const CUpdate& update, intptr_t userProvidedId)  

Example:  

Parameters
----------
* `callable` :  
    The callable to invoke.  
* `autoDelete` :  
    If true, the object will be deleted automatically when it is unregistered
    from the recipe.  

pre:  

    *   The callable must be valid (e.g., not a nullptr)  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CCallableOutputObserver::~CCallableOutputObserver "
Pylon::DataProcessing::CCallableOutputObserver::~CCallableOutputObserver";

%feature("docstring") Pylon::DataProcessing::CCallableOutputObserver::OutputDataPush "
Pylon::DataProcessing::CCallableOutputObserver::OutputDataPush
This method is called when an output of the `CRecipe` pushes data out.  

Parameters
----------
* `recipe` :  
    The recipe that produced the output.  
* `value` :  
    A variant container containing the output data.  
* `update` :  
    The corresponding update.  
* `userProvidedId` :  
    This ID is passed to distinguish between different events. This ID has been
    passed when calling `CRecipe::RegisterOutputObserver()`.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

%feature("docstring") Pylon::DataProcessing::CCallableOutputObserver::OnDeregistered "
Pylon::DataProcessing::CCallableOutputObserver::OnDeregistered
This method is called when the output observer is deregistered from the recipe.
It can be used to delete the output observer by overloading the method. The
default implementation of this method does nothing.  

Parameters
----------
* `recipe` :  
    The recipe that the observer is deregistered from.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

// File: class_pylon_1_1_data_processing_1_1_c_callable_update_observer.xml


%feature("docstring") Pylon::DataProcessing::CCallableUpdateObserver "

A class that wraps a callable (function pointer or functor) to be used as an
update observer in a `CRecipe`.  

\\threading The observer, and therefore the callable, is called from multiple
internal threads of the `CRecipe`.  

C++ includes: CallableUpdateObserver.h
";

%feature("docstring") Pylon::DataProcessing::CCallableUpdateObserver::CCallableUpdateObserver "
Pylon::DataProcessing::CCallableUpdateObserver::CCallableUpdateObserver
Constructs an update observer with a given callable.  

The callable must be invocable with the following signature: void (CRecipe&
recipe, const CUpdate& update, intptr_t userProvidedId)  

Example:  

Parameters
----------
* `callable` :  
    The callable to invoke.  
* `autoDelete` :  
    If true, the object will be deleted automatically after the callable has
    been invoked.  

pre:  

    *   The callable must be valid (e.g., not a nullptr)  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CCallableUpdateObserver::~CCallableUpdateObserver "
Pylon::DataProcessing::CCallableUpdateObserver::~CCallableUpdateObserver";

%feature("docstring") Pylon::DataProcessing::CCallableUpdateObserver::UpdateDone "
Pylon::DataProcessing::CCallableUpdateObserver::UpdateDone
This method is called when an update of a `Pylon::DataProcessing::CRecipe` has
been processed completely.  

note: If this update has triggered further updates, depending on the vTools used
    in a recipe, the output data may not be available yet.  

Parameters
----------
* `recipe` :  
    The recipe that processed the update.  
* `update` :  
    The update that was processed completely.  
* `userProvidedId` :  
    This ID is passed to distinguish between different events. This ID has been
    passed when calling `CRecipe::TriggerUpdateAsync()` or
    `CRecipe:TriggerUpdate()`.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

// File: struct_pylon_1_1_data_processing_1_1_c_event_data.xml


%feature("docstring") Pylon::DataProcessing::CEventData "

Data associated with an event inside the recipe. Currently, only errors are
supported.  

C++ includes: IEventObserver.h
";

// File: class_pylon_1_1_data_processing_1_1_c_generic_output_observer.xml


%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver "

A simple Recipe Output Observer that collects recipe outputs in a queue.  

C++ includes: GenericOutputObserver.h
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::CGenericOutputObserver "
Pylon::DataProcessing::CGenericOutputObserver::CGenericOutputObserver
Creates a `CGenericOutputObserver` object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::~CGenericOutputObserver "
Pylon::DataProcessing::CGenericOutputObserver::~CGenericOutputObserver
Destroys a `CGenericOutputObserver` object and resets the wait object provided
by GetWaitObject().  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::GetWaitObject "
Pylon::DataProcessing::CGenericOutputObserver::GetWaitObject
Returns a WaitObject that is in Signaled state if the queue is not empty and in
Reset state if it is empty.  

Returns
-------
`WaitObject` of the GenericOutputObserver.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is thread safe.  
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::RetrieveResult "
Pylon::DataProcessing::CGenericOutputObserver::RetrieveResult
Retrieves the oldest CVariantContainer from the recipe output in the queue. The
SGenericOutputObserverResult containing the CVariantContainer will be removed
from the queue.  

Returns
-------
`The` oldest CVariantContainer in the queue or an empty variant container if the
queue is empty.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is thread safe.  
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::RetrieveFullResult "
Pylon::DataProcessing::CGenericOutputObserver::RetrieveFullResult
Retrieves the oldest SGenericOutputObserverResult from the recipe output in the
queue. The SGenericOutputObserverResult will be removed from the queue.  

Returns
-------
`The` oldest SGenericOutputObserverResult in the queue or an
SGenericOutputObserverResult with an invalid update and empty CVariantContainer
if the queue is empty.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is thread safe.  
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::GetNumResults "
Pylon::DataProcessing::CGenericOutputObserver::GetNumResults
Gets the number of SGenericOutputObserverResults in the queue.  

Returns
-------
`The` number of elements in the queue.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is thread safe.  
";

%feature("docstring") Pylon::DataProcessing::CGenericOutputObserver::Clear "
Pylon::DataProcessing::CGenericOutputObserver::Clear
Removes all CVariantContainers from the queue.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is thread safe.  
";

// File: struct_pylon_1_1_data_processing_1_1_command_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::CommandParameterName "

Defines a command parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::CommandParameterName::CommandParameterName "
Pylon::DataProcessing::CommandParameterName::CommandParameterName";

// File: class_pylon_1_1_data_processing_1_1_c_recipe.xml


%feature("docstring") Pylon::DataProcessing::CRecipe "

Provides convenient access to a data processing design described by a recipe
file.  

C++ includes: Recipe.h
";

%feature("docstring") Pylon::DataProcessing::CRecipe::CRecipe "
Pylon::DataProcessing::CRecipe::CRecipe
Creates a `CRecipe` object with no recipe loaded.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::~CRecipe "
Pylon::DataProcessing::CRecipe::~CRecipe
Destroys a `CRecipe` object.  

Calls `Unload()` for cleaning up if any recipe is currently loaded.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::Load "
Pylon::DataProcessing::CRecipe::Load
Loads a recipe from disk and creates the objects of the design described by the
recipe. Relative paths, i.e., relative to the directory the recipe file is
located in, are used for loading external recipe components, e.g., images.  

Parameters
----------
* `filename` :  
    The name and path of the recipe.  

pre:  

    *   The given file name must be a valid file path of an existing file
        containing valid recipe data.  

post:  

    *   A recipe is loaded. You can use `IsLoaded()` to check whether a recipe
        is loaded. Implicitly calls `Unload()` and unregisters all observers
        already connected.  

\\error Throws an exception if the recipe can't be loaded. No recipe is loaded
if an error occurred.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::LoadFromBinary "
Pylon::DataProcessing::CRecipe::LoadFromBinary
Loads a recipe from binary buffer and creates the objects of the design
described by the recipe. Relative paths, i.e., relative to the current
directory, are used for loading external recipe components, e.g., images.  

Parameters
----------
* `pBuffer` :  
    Buffer pointer to binary recipe.  
* `bufferSize` :  
    Buffer size for binary recipe buffer in bytes.  

pre:  

    *   The buffer specified by pBuffer and bufferSize must contain valid recipe
        data.  

post:  

    *   A recipe is loaded. You can use `IsLoaded()` to check whether a recipe
        is loaded. Implicitly calls `Unload()` and unregisters all observers
        already connected.  

\\error Throws an exception if the recipe can't be loaded. No recipe is loaded
if an error occurred.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::LoadFromBinary "
Pylon::DataProcessing::CRecipe::LoadFromBinary
Loads a recipe from binary buffer and creates the objects of the design
described by the recipe.  

Parameters
----------
* `pBuffer` :  
    Buffer pointer to binary recipe.  
* `bufferSize` :  
    Buffer size for binary recipe buffer in bytes.  
* `directory` :  
    External recipe components, e.g., images, will be loaded relative to this
    directory.  

pre:  

    *   The buffer specified by pBuffer and bufferSize must contain valid recipe
        data.  

post:  

    *   A recipe is loaded. You can use `IsLoaded()` to check whether a recipe
        is loaded. Implicitly calls `Unload()` and unregisters all observers
        already connected.  

\\error Throws an exception if the recipe can't be loaded. No recipe is loaded
if an error occurred.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::IsLoaded "
Pylon::DataProcessing::CRecipe::IsLoaded
Checks whether a recipe is loaded.  

Returns
-------
`true` if a recipe is loaded.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::PreAllocateResources "
Pylon::DataProcessing::CRecipe::PreAllocateResources
Optional method to pre-allocate resources.  

All resources that could be allocated successfully stay allocated until a call
to `DeallocateResources()`.  

pre:  

    *   A recipe is loaded.  
    *   The recipe must not be started.  

post:  

    *   All resources are allocated.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The resources couldn't be allocated.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::Start "
Pylon::DataProcessing::CRecipe::Start
Prepares the data processing and allocates resources required by the design. All
Camera and Image Loading vTools keep their individual acquisition modes and the
recipe is started like that (this corresponds to
`Start(AcquisitionMode_Unchanged)`).  

pre:  

    *   A recipe is loaded.  

\\error The recipe is not started if an error occurred. Throws an exception if
the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::Start "
Pylon::DataProcessing::CRecipe::Start
Prepares the data processing and allocates resources required by the design. In
addition, the acquisition mode for all Camera and Image Loading vTools can be
specified (see `EAcquisitionMode` for more details).  

Parameters
----------
* `acquisitionMode` :  
    The acquisition mode used to start the recipe (see `EAcquisitionMode` for
    more details).  

pre:  

    *   A recipe has been loaded.  

\\error The recipe is not started if an error occurred. Throws an exception if
the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::IsStarted "
Pylon::DataProcessing::CRecipe::IsStarted
Returns information about the recipe being started.  

Returns
-------
`true` if the recipe has been started.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::Stop "
Pylon::DataProcessing::CRecipe::Stop
Finishes the data processing and deallocates all resources allocated at start.  

Updates may accumulate at some places in the design, e.g., when updates are
triggered more frequently than can be processed and the queue mode of the
connections is not set properly. `timeoutMs` describes the time these
accumulated updates are tolerated before they will be cleared. Updates that are
already being processed by a vTool will not be aborted when the timeout expires.  

Parameters
----------
* `timeoutMs` :  
    Time to wait for updates not yet started to be processed.  

\\error Doesn't throw C++ exceptions.  

post:  

    *   The recipe is stopped.  
    *   Resources allocated when calling `Start()` are deallocated.  
    *   Resources allocated when calling `PreAllocateResources()` are still
        allocated.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::DeallocateResources "
Pylon::DataProcessing::CRecipe::DeallocateResources
Deallocates all resources used by the recipe.  

Calls `Stop()` if the design described by the recipe has been started.  

post:  

    *   No resources are allocated.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::Unload "
Pylon::DataProcessing::CRecipe::Unload
Unloads the recipe currently loaded.  

Calls `DeallocateResources()` if the design described by the recipe has
allocated resources. Unregisters all observers that have been connected.  

pre:  

    *   Data received via `IOutputObserver::OutputDataPush` must be freed.  

post:  

    *   No recipe is loaded.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetParameters "
Pylon::DataProcessing::CRecipe::GetParameters
Returns a parameter collection to access the parameters of the recipe.  

note: The `IParameterCollection` returns objects based on `CParameter` that can
    be used while a recipe is loaded. Before unloading a recipe, the parameter
    objects must be cleared by calling `CParameter::Release()`. For parameters
    that become available only when resources are allocated, e.g., a camera,
    `CParameter::Release()` must be called before deallocating a resource.  

Returns
-------
A reference to the `IParameterCollection`.  

pre:  

    *   A recipe is loaded.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::SetRecipeContext "
Pylon::DataProcessing::CRecipe::SetRecipeContext
Sets a context.  

This is useful when handling multiple recipes.  

You can access the context using `GetRecipeContext()`, e.g., in
`IOutputObserver::OutputDataPush()`, when receiving data from multiple recipes.  

Parameters
----------
* `context` :  
    The user-defined context.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using an internal lock for the recipe
context.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetRecipeContext "
Pylon::DataProcessing::CRecipe::GetRecipeContext
Returns the context.  

This is useful when handling multiple recipes.  

You can access the context using `GetRecipeContext()`, e.g., in
`IOutputObserver::OutputDataPush()`, when receiving data from multiple recipes.  

Returns
-------
The context.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using an internal lock for the recipe
context.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::HasInput "
Pylon::DataProcessing::CRecipe::HasInput
Checks whether an input pin is available.  

Parameters
----------
* `inputFullName` :  
    The identifier of the input pin.  

Returns
-------
`true` if the input pin is available.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::HasOutput "
Pylon::DataProcessing::CRecipe::HasOutput
Checks whether an output pin is available.  

Parameters
----------
* `outputFullName` :  
    The identifier of the output pin.  

Returns
-------
`true` if the output pin is available.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetInputType "
Pylon::DataProcessing::CRecipe::GetInputType
Returns the variant data type of the input pin.  

Parameters
----------
* `inputFullName` :  
    The identifier of the input pin.  

Returns
-------
The variant data type of the input pin.  

pre:  

    *   An input pin with the name `inputFullName` must exist.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetInputContainerType "
Pylon::DataProcessing::CRecipe::GetInputContainerType
Returns the variant container type of the input pin.  

Parameters
----------
* `inputFullName` :  
    The identifier of the input pin.  

Returns
-------
The variant container type of the input pin.  

pre:  

    *   An input pin with the name `inputFullName` must exist.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetOutputType "
Pylon::DataProcessing::CRecipe::GetOutputType
Returns the variant data type of the output pin.  

Parameters
----------
* `outputFullName` :  
    The identifier of the output pin.  

Returns
-------
The variant data type of the output pin.  

pre:  

    *   An output pin with the name `outputFullName` must exist.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetOutputContainerType "
Pylon::DataProcessing::CRecipe::GetOutputContainerType
Returns the variant container type of the output pin.  

Parameters
----------
* `outputFullName` :  
    The identifier of the output pin.  

Returns
-------
The variant container type of the output pin.  

pre:  

    *   An output pin with the name `outputFullName` must exist.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::CanTriggerUpdate "
Pylon::DataProcessing::CRecipe::CanTriggerUpdate
Checks whether triggering an update is possible.  

An update can't be triggered if the recipe is not started or at least one
connection connected to the input terminal has its queue mode set to blocking
and there is no space available.  

Returns
-------
`true` if an update can be triggered, `false` otherwise.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::TriggerUpdateAsync "
Pylon::DataProcessing::CRecipe::TriggerUpdateAsync
Starts an update asynchronously for a single input pin.  

Parameters
----------
* `inputFullName` :  
    The name of the input pin.  
* `value` :  
    The value to feed the input pin with.  
* `pObserver` :  
    Optionally, the observer to notify when the update has been processed
    completely. This doesn't include subsequent updates triggered by this
    update. This depends on the vTools used in the recipe.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

Returns
-------
The update object that has been produced by this call.  

pre:  

    *   The recipe is started.  
    *   The input pin exists.  
    *   The type of the `value` is compatible with the input data type.  
    *   `CanTriggerUpdate()` must return `true`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::TriggerUpdateAsync "
Pylon::DataProcessing::CRecipe::TriggerUpdateAsync
Starts an update asynchronously for a number of input pins.  

Parameters
----------
* `inputCollection` :  
    Provides the input names and the values.  
* `pObserver` :  
    An optional observer to notify when the update has been processed
    completely. This doesn't include subsequent updates triggered by this
    update. This depends on the vTools used in the recipe.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

Returns
-------
The update object that has been produced by this call.  

pre:  

    *   The recipe is started.  
    *   The `inputCollection` argument is not empty.  
    *   The input pins exist.  
    *   The types of the values in `inputCollection` are compatible with the
        input data types.  
    *   `CanTriggerUpdate()` must return `true`.  

\\error Throws an exception if the preconditions aren't met.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::TriggerUpdate "
Pylon::DataProcessing::CRecipe::TriggerUpdate
Starts an update in a blocking call for a single input pin.  

Parameters
----------
* `inputFullName` :  
    The name of the input pin.  
* `value` :  
    The value to feed the input pin with.  
* `timeoutMs` :  
    The timeout for the update to finish completely.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  
* `pObserver` :  
    An optional observer to notify when the update has been processed
    completely. This doesn't include subsequent updates triggered by this
    update. This depends on the vTools used in the recipe.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

Returns
-------
The update object that has been produced by this call.  

pre:  

    *   The recipe is started.  
    *   The input pin exists.  
    *   The type of the `value` is compatible with the input data type.  
    *   `CanTriggerUpdate()` must return `true`.  

\\error Throws an exception if the preconditions aren't met. Throws an exception
if the update couldn't be processed in the time specified by `timeoutMs` and
`timeoutHandling` == TimeoutHandling_ThrowException.  

\\threading This method is synchronized using the lock provided by `GetLock()`
while not waiting for the update to finish completely.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::TriggerUpdate "
Pylon::DataProcessing::CRecipe::TriggerUpdate
Starts an update in a blocking call for a number of input pins.  

Parameters
----------
* `inputCollection` :  
    Provides the input names and the values.  
* `timeoutMs` :  
    The timeout for the update to finish completely.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  
* `pObserver` :  
    An optional observer to notify when the update has been processed
    completely. This doesn't include subsequent updates triggered by this
    update. This depends on the vTools used in the recipe.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

Returns
-------
The update object that has been produced by this call.  

pre:  

    *   The recipe is started.  
    *   The `inputCollection` argument is not empty.  
    *   The input pins exist.  
    *   The types of the values in `inputCollection` are compatible with the
        input data types.  
    *   `CanTriggerUpdate()` must return `true`.  

\\error Throws an exception if the preconditions aren't met. Throws an exception
if the update couldn't be processed in the time specified by `timeoutMs` and
`timeoutHandling` == TimeoutHandling_ThrowException.  

\\threading This method is synchronized using the lock provided by `GetLock()`
while not waiting for the update to finish completely.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::TriggerUpdateWithReturn "
Pylon::DataProcessing::CRecipe::TriggerUpdateWithReturn
Starts an update in a blocking call for a number of input pins. After the update
has been processed, a variant container containing the recipe output is
returned. This method is only intended for cases where the input triggers
exactly one result.  

Parameters
----------
* `inputCollection` :  
    Provides the input names and the values.  
* `timeoutMs` :  
    The timeout for the update to finish completely.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
The variant container that has been output by the recipe.  

pre:  

    *   The recipe is started.  
    *   The `inputCollection` argument is not empty.  
    *   The input pins exist.  
    *   The types of the values in `inputCollection` are compatible with the
        input data types.  
    *   `CanTriggerUpdate()` must return `true`.  

\\error Throws an exception if the preconditions aren't met. Throws an exception
if the update couldn't be processed in the time specified by `timeoutMs` and
`timeoutHandling` == TimeoutHandling_ThrowException.  

\\threading This method is synchronized using the lock provided by `GetLock()`
while not waiting for the update to finish completely.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetOutputNames "
Pylon::DataProcessing::CRecipe::GetOutputNames
Returns the count and the list of names of all output pins.  

Parameters
----------
* `result` :  
    The list of output pin names of the recipe.  

Returns
-------
Number of output pin names of the recipe.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::RegisterOutputObserver "
Pylon::DataProcessing::CRecipe::RegisterOutputObserver
Adds an output observer to the list of registered output observers.  

If mode equals `RegistrationMode_ReplaceAll`, the list of registered observes is
cleared.  

note:  

    *   The observer must not be deleted before the `CRecipe` is destroyed while
        it is registered.  
    *   If the `IOutputObserver` and the `CRecipe` are created on the stack in
        the same scope, the observer must be created prior to the `CRecipe` it
        is registered to because the objects are destroyed in reverse order.  

Parameters
----------
* `outputFullName` :  
    The name of the output pin.  
* `pObserver` :  
    The receiver of events.  
* `mode` :  
    Indicates how to register the new observer.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

pre:  

    *   A recipe is loaded.  
    *   The output pin exists.  
    *   `pObserver` is not nullptr.  

post:  

    *   The observer is registered and called when output data is available.  

\\error Throws an exception if the preconditions aren't met. If an exception is
thrown, the observer is not registered and its `OnDeregistered` method will not
be called.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::RegisterOutputObserver "
Pylon::DataProcessing::CRecipe::RegisterOutputObserver
Adds an output observer to the list of registered output observers.  

If `mode` equals `RegistrationMode_ReplaceAll`, the list of registered observes
is cleared.  

note:  

    *   The observer must not be deleted before the `CRecipe` is destroyed while
        it is registered.  
    *   If the `IOutputObserver` and the `CRecipe` are created on the stack in
        the same scope, the observer must be created prior to the `CRecipe` it
        is registered to because the objects are destroyed in reverse order.  

Parameters
----------
* `outputFullNames` :  
    A list of names of the observed output pins.  
* `pObserver` :  
    The receiver of events.  
* `mode` :  
    Indicates how to register the new observer.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

pre:  

    *   A recipe is loaded.  
    *   The output pins exist.  
    *   `pObserver` is not nullptr.  

post:  

    *   The observer is registered and called when output data is available.  

\\error Throws an exception if the preconditions aren't met. If an exception is
thrown, the observer is not registered and its `OnDeregistered` method will not
be called.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::RegisterAllOutputsObserver "
Pylon::DataProcessing::CRecipe::RegisterAllOutputsObserver
Adds an output observer to the list of registered output observers.  

If `mode` equals `RegistrationMode_ReplaceAll`, the list of registered observes
is cleared.  

note:  

    *   The observer must not be deleted before the `CRecipe` is destroyed while
        it is registered.  
    *   If the `IOutputObserver` and the `CRecipe` are created on the stack in
        the same scope, the observer must be created prior to the `CRecipe` it
        is registered to because the objects are destroyed in reverse order.  

Parameters
----------
* `pObserver` :  
    The receiver of events.  
* `mode` :  
    Indicates how to register the new observer.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. This ID
    is provided to `IUpdateObserver::UpdateDone`.  

pre:  

    *   A recipe is loaded.  
    *   `pObserver` is not nullptr.  

post:  

    *   The observer is registered and called when any output data is available.  

\\error Throws an exception if the preconditions aren't met. If an exception is
thrown, the observer is not registered and its `OnDeregistered` method will not
be called.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::UnregisterOutputObserver "
Pylon::DataProcessing::CRecipe::UnregisterOutputObserver
Removes an output observer from the list of registered output observers and
calls the observer's `OnDeregistered` method.  

If the output pin or the observer with `userProvidedId` is not found, nothing is
done.  

note: The last registered observer with `userProvidedId` is unregistered first
    if the same observer with `userProvidedId` has been registered multiple
    times.  

Parameters
----------
* `outputFullName` :  
    The name of the output pin.  
* `pObserver` :  
    The receiver of events.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. If an
    observer has been registered multiple times, the observer with the matching
    user id is deregistered.  

Returns
-------
`true` if the output pin and the observer were found and the observer has been
unregistered.  

post:  

    *   If the output pin and the observer were found, the observer is
        unregistered.  
    *   If an observer has been registered multiple times, the observer with the
        matching user ID is deregistered.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::UnregisterOutputObserver "
Pylon::DataProcessing::CRecipe::UnregisterOutputObserver
Removes an output observer from the list of registered output observers for all
output pins and calls the observer's `OnDeregistered` method.  

If the observer with `userProvidedId` is not found, nothing is done.  

note: The last registered observer with `userProvidedId` is unregistered first
    if the same observer with `userProvidedId` has been registered multiple
    times.  

Parameters
----------
* `pObserver` :  
    The receiver of events.  
* `userProvidedId` :  
    This optional ID is passed to distinguish between different events. If an
    observer has been registered multiple times, the observer with the matching
    user ID is deregistered.  

Returns
-------
`true` if the output pin and the observer were found and the observer has been
unregistered.  

post:  

    *   If the output pin and the observer were found, the observer is
        unregistered.  
    *   If an observer has been registered multiple times, the observer with the
        matching user ID is deregistered.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using the lock provided by `GetLock()`.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::RegisterEventObserver "
Pylon::DataProcessing::CRecipe::RegisterEventObserver
Registers an event observer to the recipe. Only one single observer per recipe
is supported. Registering a new one automatically unregisters the old one.
Registered observers must be unregistered before destruction.  

Parameters
----------
* `pObserver` :  
    The receiver of events.  

pre:  

    *   `pObserver` is not nullptr.  

post:  

    *   The observer is registered and called when events occur, e.g., an error
        is detected by a vTool.  

\\error Throws an exception if the preconditions aren't met. If an exception is
thrown, the observer is not registered and its `OnDeregistered` method will not
be called.  

\\threading This method is synchronized using an internal lock for event
observer handling.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::UnregisterEventObserver "
Pylon::DataProcessing::CRecipe::UnregisterEventObserver
Removes any registered event observer from the recipe and calls the observer's
`OnDeregistered` method.  

If an observer is not found, nothing is done.  

\\error Doesn't throw C++ exceptions.  

\\threading This method is synchronized using an internal lock for event
observer handling.  
";

%feature("docstring") Pylon::DataProcessing::CRecipe::GetLock "
Pylon::DataProcessing::CRecipe::GetLock
Provides access to the lock used for synchronizing the access to the recipe.  

This lock can be used when extending the Recipe class.  

Example:  

\\error Doesn't throw C++ exceptions.  
";

// File: class_pylon_1_1_data_processing_1_1_c_region.xml


%feature("docstring") Pylon::DataProcessing::CRegion "

Describes a region and takes care of the buffer handling and lifetime.  

*   Automatically handles size and lifetime of the region buffer.  
*   Allows you to connect user buffers or buffers provided by third-party
    software packages.  

par: Buffer Handling:
    The buffer that is automatically created by the CRegion class or is replaced
    by a larger buffer if Reset() is called (only if required). The size of the
    allocated buffer is never decreased. Referenced user buffers are never
    automatically replaced by a larger buffer. See the Reset() method for more
    details. The Release() method can be used to detach a user buffer or to free
    an allocated buffer.  

\\threading The CRegion class isn't thread-safe.  

C++ includes: Region.h
";

%feature("docstring") Pylon::DataProcessing::CRegion::CRegion "
Pylon::DataProcessing::CRegion::CRegion
Creates an invalid region.  

See Release() for the properties of an invalid region.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::CRegion "
Pylon::DataProcessing::CRegion::CRegion
Creates a region and allocates a buffer for it.  

Parameters
----------
* `regionType` :  
    The type of the new region.  
* `dataSize` :  
    The size of the region in bytes. For run-length encoded formats, the size in
    bytes defines the number of entries, e.g., 24 bytes result in 2 RLE32
    entries for RegionType_RLE32.  
* `referenceWidth` :  
    The width of the source of the region if available, 0 otherwise.  
* `referenceHeight` :  
    The height of the source of the region if available, 0 otherwise.  
* `boundingBoxTopLeftX` :  
    The smallest horizontal pixel position of the region if available, 0
    otherwise.  
* `boundingBoxTopLeftY` :  
    The smallest vertical pixel position of the region if available, 0
    otherwise.  
* `boundingBoxWidth` :  
    The width of the bounding box of the region if available, 0 otherwise.  
* `boundingBoxHeight` :  
    The height of the bounding box of the region if available, 0 otherwise.  

pre:  

    *   The region type must be valid.  
    *   Either all bounding box values are 0, or `boundingBoxWidth` and
        `boundingBoxHeight` are both greater than 0.  

\\error Throws an exception if the parameters are invalid. Throws an exception
if no buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::CRegion "
Pylon::DataProcessing::CRegion::CRegion
Copies the region properties and creates a reference to the buffer of the source
region.  

Parameters
----------
* `source` :  
    The source region.  

post:  

    *   Another reference to the source region buffer is created.  
    *   Creates an invalid region if the source region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::~CRegion "
Pylon::DataProcessing::CRegion::~CRegion
Destroys a pylon region object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::CopyRegion "
Pylon::DataProcessing::CRegion::CopyRegion
Copies the region data from a different region.  

This method is used for making a full copy of a region. Calls the Reset() method
to set the same region properties as the source region and copies the region
data.  

Parameters
----------
* `region` :  
    The source region.  

pre: The preconditions of the Reset() method must be met.  

post:  

    *   The region contains a copy of the source region's region data.  
    *   Creates an invalid region if the source region is invalid.  

\\error Throws an exception if no buffer with the required size could be
allocated. Throws an exception if the preconditions of the Reset() method aren't
met.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::CopyRegion "
Pylon::DataProcessing::CRegion::CopyRegion
Copies the region data from a buffer provided.  

This method is used for making a full copy of a region. Calls the Reset() method
to set the same region properties as the source region and copies the region
data.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source region.  
* `dataSize` :  
    The size of the region in bytes. For run-length encoded formats, the size in
    bytes defines the number of entries, e.g., 24 bytes result in 2 RLE32
    entries for RegionType_RLE32.  
* `regionType` :  
    The type of the new region.  
* `referenceWidth` :  
    The width of the source of the region if available, 0 otherwise.  
* `referenceHeight` :  
    The height of the source of the region if available, 0 otherwise.  
* `boundingBoxTopLeftX` :  
    The smallest horizontal pixel position of the region if available, 0
    otherwise.  
* `boundingBoxTopLeftY` :  
    The smallest vertical pixel position of the region if available, 0
    otherwise.  
* `boundingBoxWidth` :  
    The width of the bounding box of the region if available, 0 otherwise.  
* `boundingBoxHeight` :  
    The height of the bounding box of the region if available, 0 otherwise.  

pre:  

    *   The region type must be valid.  
    *   `pBuffer` must not be NULL.  
    *   The preconditions of the Reset() method must be met.  
    *   Either all bounding box values are 0, or `boundingBoxWidth` and
        `boundingBoxHeight` are both greater than 0.  

post: A copy of the source region buffer's region is made.  

\\error Throws an exception if no buffer with the required size could be
allocated. Throws an exception if the preconditions of the Reset() method aren't
met.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::AttachUserBuffer "
Pylon::DataProcessing::CRegion::AttachUserBuffer
Attaches a user buffer.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source region. CRegion will never free any
    user buffers.  
* `bufferSize` :  
    The size of the attached buffer.  
* `dataSize` :  
    The size of the region in bytes. For run-length encoded formats, the size in
    bytes defines the number of entries, e.g., 24 bytes result in 2 RLE32
    entries for RegionType_RLE32.  
* `regionType` :  
    The type of the new region.  
* `referenceWidth` :  
    The width of the source of the region if available, 0 otherwise.  
* `referenceHeight` :  
    The height of the source of the region if available, 0 otherwise.  
* `boundingBoxTopLeftX` :  
    The smallest horizontal pixel position of the region if available, 0
    otherwise.  
* `boundingBoxTopLeftY` :  
    The smallest vertical pixel position of the region if available, 0
    otherwise.  
* `boundingBoxWidth` :  
    The width of the bounding box of the region if available, 0 otherwise.  
* `boundingBoxHeight` :  
    The height of the bounding box of the region if available, 0 otherwise.  
* `pEventHandler` :  
    A pointer to an optional CRegionUserBufferEventHandler-derived object called
    when the user-supplied buffer isn't used anymore. You can use this to free
    the user-supplied buffer. In case the function throws an exception, the
    handler will not be called.  

When attaching a user buffer and passing a pEventHandler, the user is
responsible for ensuring the object is valid until
CRegionUserBufferEventHandler::OnRegionUserBufferDetached() has been called. The
user is also responsible for freeing the handler object after
CRegionUserBufferEventHandler::OnRegionUserBufferDetached() has been called.
After the function has returned, CRegion won't access the object anymore. See
`CRegionUserBufferEventHandler::OnRegionUserBufferDetached()` for a sample.  

pre:  

    *   The region type must be valid.  
    *   `pBuffer` must not be NULL.  
    *   The buffer passed in `pBuffer` must not be currently attached.  
    *   Either all bounding box values are 0, or `boundingBoxWidth` and
        `boundingBoxHeight` are both greater than 0.  

post:  

    *   The region properties are taken from the parameters passed.  
    *   The user buffer is used by the region class.  
    *   The user buffer must not be freed while being attached.  

\\error Throws an exception if the preconditions aren't met. In this case, the
optional handler passed in \\ pEventHandler won't be called.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::AttachUserBuffer "
Pylon::DataProcessing::CRegion::AttachUserBuffer
Attaches a user buffer.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source region. CRegion will never free any
    user buffers.  
* `bufferSize` :  
    The size of the attached buffer.  
* `dataSize` :  
    The size of the region in bytes. For run-length encoded formats, the size in
    bytes defines the number of entries, e.g., 24 bytes result in 2 RLE32
    entries for RegionType_RLE32.  
* `regionType` :  
    The type of the new region.  
* `referenceWidth` :  
    The width of the source of the region if available, 0 otherwise.  
* `referenceHeight` :  
    The height of the source of the region if available, 0 otherwise.  
* `boundingBoxTopLeftX` :  
    The smallest horizontal pixel position of the region if available, 0
    otherwise.  
* `boundingBoxTopLeftY` :  
    The smallest vertical pixel position of the region if available, 0
    otherwise.  
* `boundingBoxWidth` :  
    The width of the bounding box of the region if available, 0 otherwise.  
* `boundingBoxHeight` :  
    The height of the bounding box of the region if available, 0 otherwise.  
* `pEventHandler` :  
    A pointer to an optional CRegionUserBufferEventHandler-derived object called
    when the user-supplied buffer isn't used anymore. You can use this to free
    the user-supplied buffer. In case the function throws an exception, the
    handler will not be called.  

When attaching a user buffer and passing a pEventHandler, the user is
responsible for ensuring the object is valid until
CRegionUserBufferEventHandler::OnRegionUserBufferDetached() has been called. The
user is also responsible for freeing the handler object after
CRegionUserBufferEventHandler::OnRegionUserBufferDetached() has been called.
After the function has returned, CRegion won't access the object anymore. See
`CRegionUserBufferEventHandler::OnRegionUserBufferDetached()` for a sample.  

pre:  

    *   The region type must be valid.  
    *   `pBuffer` must not be NULL.  
    *   The buffer passed in `pBuffer` must not be currently attached.  
    *   Either all bounding box values are 0, or `boundingBoxWidth` and
        `boundingBoxHeight` are both greater than 0.  

post:  

    *   The region properties are taken from the parameters passed.  
    *   The user buffer is used by the region class.  
    *   The user buffer must not be freed while being attached.  

\\error Throws an exception if the preconditions aren't met. In this case, the
optional handler passed in \\ pEventHandler won't be called. This overload can
be used for read-only buffers.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::IsValid "
Pylon::DataProcessing::CRegion::IsValid
Can be used to check whether a region is valid.  

Returns
-------
Returns false if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::IsReadOnly "
Pylon::DataProcessing::CRegion::IsReadOnly
Can be used to check whether a region data buffer is read-only.  

Returns
-------
Returns true if the region data buffer is read-only or the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetRegionType "
Pylon::DataProcessing::CRegion::GetRegionType
Get the current region type.  

Returns
-------
Returns the Region type or RegionType_Undefined if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::IsUserBufferAttached "
Pylon::DataProcessing::CRegion::IsUserBufferAttached
Indicates whether a user buffer is attached.  

Returns
-------
Returns true if a user buffer is attached. Returns false if the region is
invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetAllocatedBufferSize "
Pylon::DataProcessing::CRegion::GetAllocatedBufferSize
Returns the size of the buffer used.  

This method is useful when working with so-called user buffers.  

Returns
-------
Returns the size of the buffer used in bytes or 0 if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetDataSize "
Pylon::DataProcessing::CRegion::GetDataSize
Get the size of the region in bytes.  

Returns
-------
Returns the size of the region in bytes or 0 if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::IsUnique "
Pylon::DataProcessing::CRegion::IsUnique
Indicates whether the referenced buffer is only referenced by this region.  

Returns
-------
Returns true if the referenced buffer is only referenced by this region. Returns
false if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::HasReferenceSize "
Pylon::DataProcessing::CRegion::HasReferenceSize
Indicates whether reference size information is available.  

Returns
-------
Returns true if reference width or height aren't equal to zero. Returns false if
the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetReferenceWidth "
Pylon::DataProcessing::CRegion::GetReferenceWidth
Get the reference width in pixels.  

Returns
-------
Returns the reference width or 0 if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetReferenceHeight "
Pylon::DataProcessing::CRegion::GetReferenceHeight
Get the reference height in pixels.  

Returns
-------
Returns the reference height or 0 if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::HasBoundingBox "
Pylon::DataProcessing::CRegion::HasBoundingBox
Indicates whether bounding box information is available.  

Returns
-------
Returns true if boundingBoxWidth and boundingBoxHeight aren't equal to zero.
Returns false if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBoundingBoxTopLeftX "
Pylon::DataProcessing::CRegion::GetBoundingBoxTopLeftX
Use this method to get the smallest horizontal pixel position of the region.
\\error Doesn't throw C++ exceptions.  

Returns
-------
Returns the smallest horizontal pixel position of the region. Returns 0 if the
region is invalid.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBoundingBoxTopLeftY "
Pylon::DataProcessing::CRegion::GetBoundingBoxTopLeftY
Use this method to get the smallest vertical pixel position of the region.
\\error Doesn't throw C++ exceptions.  

Returns
-------
Returns the smallest vertical pixel position of the region. Returns 0 if the
region is invalid.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBoundingBoxWidth "
Pylon::DataProcessing::CRegion::GetBoundingBoxWidth
Use this method to get the width of the region's bounding box. \\error Doesn't
throw C++ exceptions.  

Returns
-------
Returns the width of the region's bounding box. Returns 0 if the region is
invalid.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBoundingBoxHeight "
Pylon::DataProcessing::CRegion::GetBoundingBoxHeight
Use this method to get the height of the region's bounding box. \\error Doesn't
throw C++ exceptions.  

Returns
-------
Returns the height of the region's bounding box. Returns 0 if the region is
invalid.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBuffer "
Pylon::DataProcessing::CRegion::GetBuffer
Get the pointer to the buffer.  

Returns
-------
Returns the pointer to the buffer used or NULL if the region is invalid.  

pre: The region's buffer is not read-only. Use, e.g., GetBufferConst() in this
    case.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBuffer "
Pylon::DataProcessing::CRegion::GetBuffer
Get the pointer to the buffer containing the region.  

The buffer is at least as large as the value returned by GetDataSize().  

Returns
-------
Returns the pointer to the buffer used or NULL if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::GetBufferConst "
Pylon::DataProcessing::CRegion::GetBufferConst
Get the pointer to the buffer containing the region.  

The buffer is at least as large as the value returned by GetDataSize().  

Returns
-------
Returns the pointer to the buffer used or NULL if the region is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::Reset "
Pylon::DataProcessing::CRegion::Reset
Resets the region properties and allocates a new buffer if required.  

Parameters
----------
* `regionType` :  
    The type of the new region.  
* `dataSize` :  
    The size of the region in bytes. For run-length encoded formats, the size in
    bytes defines the number of entries, e.g., 24 bytes result in 2 RLE32
    entries for RegionType_RLE32.  
* `referenceWidth` :  
    The width of the source of the region if available, 0 otherwise.  
* `referenceHeight` :  
    The height of the source of the region if available, 0 otherwise.  
* `boundingBoxTopLeftX` :  
    The smallest horizontal pixel position of the region if available, 0
    otherwise.  
* `boundingBoxTopLeftY` :  
    The smallest vertical pixel position of the region if available, 0
    otherwise.  
* `boundingBoxWidth` :  
    The width of the bounding box of the region if available, 0 otherwise.  
* `boundingBoxHeight` :  
    The height of the bounding box of the region if available, 0 otherwise.  

pre:  

    *   The region type must be valid.  
    *   If a user buffer is referenced, this buffer must not be referenced by
        another pylon region. See the IsUnique() and IsUserBufferAttached()
        methods.  
    *   If a user buffer is referenced, this buffer must be large enough to hold
        the destination region. See the GetAllocatedBufferSize() and
        IsUserBufferAttached() methods.  
    *   Either all bounding box values are 0, or `boundingBoxWidth` and
        `boundingBoxHeight` are both greater than 0.  

post:  

    *   If the previously referenced buffer is also referenced by another pylon
        region, a new buffer has been allocated.  
    *   If the previously referenced buffer isn't large enough to hold a region
        with the specified properties, a new buffer has been allocated.  
    *   If no buffer has been allocated before, a buffer has been allocated.  

\\error Throws an exception if the preconditions aren't met. Throws an exception
if no buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::Resize "
Pylon::DataProcessing::CRegion::Resize
Resizes the region.  

Parameters
----------
* `dataSize` :  
    The size of the region in bytes. For run-length encoded formats, the size in
    bytes defines the number of entries, e.g., 24 bytes result in 2 RLE32
    entries for RegionType_RLE32.  

pre:  

    *   The region must be valid.  
    *   If a user buffer is referenced, this buffer must not be referenced by
        another pylon region. See the IsUnique() and IsUserBufferAttached()
        methods.  
    *   If a user buffer is referenced, this buffer must be large enough to hold
        the new data size. See the GetAllocatedBufferSize() and
        IsUserBufferAttached() methods.  

post:  

    *   If the previously referenced buffer is also referenced by another pylon
        region, a new buffer has been allocated.  
    *   A new buffer is allocated if necessary.  
    *   If a new buffer is allocated, the old data (old data size bytes) is
        copied to the new buffer.  
    *   The data size is changed.  
";

%feature("docstring") Pylon::DataProcessing::CRegion::Release "
Pylon::DataProcessing::CRegion::Release
Releases the region buffer and resets to an invalid region.  

post:  

    *   RegionType = RegionType_Undefined.  
    *   DataSize=0.  
    *   ReferenceWidth = 0.  
    *   ReferenceHeight = 0.  
    *   boundingBoxTopLeftX = 0.  
    *   boundingBoxTopLeftY = 0.  
    *   boundingBoxWidth = 0.  
    *   boundingBoxHeight = 0.  
    *   No buffer is allocated.  

\\error Doesn't throw C++ exceptions.  
";

// File: class_pylon_1_1_data_processing_1_1_c_region_user_buffer_event_handler.xml


%feature("docstring") Pylon::DataProcessing::CRegionUserBufferEventHandler "

The CRegion user buffer event handler base class.  

You have the option of passing an object derived from this class when calling
CRegion::AttachUserBuffer(). When the CRegion doesn't need the user buffer
anymore, it will call the
CRegionUserBufferEventHandler::OnRegionUserBufferDetached() method. You can
override this function to execute your custom code when the user buffer has been
detached implicitly.  

The user is responsible for ensuring the object is valid until
CRegionUserBufferEventHandler::OnRegionUserBufferDetached() has been called.  

C++ includes: RegionUserBufferEventHandler.h
";

%feature("docstring") Pylon::DataProcessing::CRegionUserBufferEventHandler::OnRegionUserBufferDetached "
Pylon::DataProcessing::CRegionUserBufferEventHandler::OnRegionUserBufferDetached
This method is called after the region class has released its user buffer.  

This method is called after the region class releases its region buffer. If a
user buffer has been attached using CRegion::AttachUserBuffer(), you can use
this to free your user buffer.  

If you created the event handler on the heap using `new`, you can call `delete
this` at the end of the function.  


The default implementation does nothing. You can override this function to
execute custom code.  

Parameters
----------
* `pUserBuffer` :  
    Pointer to the user buffer passed if the user buffer was attached using
    CRegion::AttachUserBuffer().  
* `bufferSizeBytes` :  
    Size of the user buffer passed if the user buffer was attached using
    CRegion::AttachUserBuffer().  

\\error This method must not throw any exceptions.  
";

// File: class_pylon_1_1_data_processing_1_1_c_transformation_data.xml


%feature("docstring") Pylon::DataProcessing::CTransformationData "

Describes a transformation data class that represents a mathematical matrix with
a specific number of columns and rows.  

\\threading The CTransformationData class isn't thread-safe.  

C++ includes: TransformationData.h
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::CTransformationData "
Pylon::DataProcessing::CTransformationData::CTransformationData
Creates invalid transformation data.  

post:  

    *   IsValid() will return false.  
    *   GetColumnCount() will return 0.  
    *   GetRowCount() will return 0.  
    *   GetEntry(size_t column, size_t row) will throw an exception.  
    *   SetEntry(size_t column, size_t row, size_t value) will throw an
        exception.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::CTransformationData "
Pylon::DataProcessing::CTransformationData::CTransformationData
Creates valid transformation data with the specified number of columns and rows.  

Parameters
----------
* `columns` :  
    The number of columns that the new transformation data should have (must be
    higher than 0).  
* `rows` :  
    The number of rows that the new transformation data should have (must be
    higher than 0).  

pre:  

    *   Argument columns must be higher than 0.  
    *   Argument rows must be higher than 0.  

post:  

    *   IsValid() will return true.  
    *   All entries will be reset to 0.0.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::CTransformationData "
Pylon::DataProcessing::CTransformationData::CTransformationData
Copies the transformation data properties and values from the source
transformation data.  

Parameters
----------
* `source` :  
    The source transformation data.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::CTransformationData "
Pylon::DataProcessing::CTransformationData::CTransformationData
Move constructs the transformation data properties and values from the source
transformation data.  

Parameters
----------
* `source` :  
    The source transformation data (will be invalid after the call).  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::~CTransformationData "
Pylon::DataProcessing::CTransformationData::~CTransformationData
Destroys a transformation data object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::Reset "
Pylon::DataProcessing::CTransformationData::Reset
Resets the transformation data using the specified number of columns and rows.  

Parameters
----------
* `columns` :  
    The number of columns that the transformation data should have (must be
    higher than 0).  
* `rows` :  
    The number of rows that the transformation data should have (must be higher
    than 0).  

pre:  

    *   Argument columns must be higher than 0.  
    *   Argument rows must be higher than 0.  

post:  

    *   IsValid() will return true.  
    *   All entries will be reset to 0.0.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::IsValid "
Pylon::DataProcessing::CTransformationData::IsValid
Can be used to check whether the transformation data is valid.  

Returns
-------
Returns false if the transformation data is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::GetColumnCount "
Pylon::DataProcessing::CTransformationData::GetColumnCount
Get the number of columns of the transformation data.  

Returns
-------
Returns the number of columns or 0 if the transformation data is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::GetRowCount "
Pylon::DataProcessing::CTransformationData::GetRowCount
Get the number of rows of the transformation data.  

Returns
-------
Returns the number of rows or 0 if the transformation data is invalid.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::GetEntry "
Pylon::DataProcessing::CTransformationData::GetEntry
Get an entry at a specific position of the transformation data.  

Parameters
----------
* `column` :  
    The column of the entry to retrieve (must be lower than number of columns).  
* `row` :  
    The row of the entry to retrieve (must be lower than number of rows).  

pre:  

    *   Transformation data must be valid.  
    *   Argument column must be lower than number of columns.  
    *   Argument row must be lower than number of rows.  

Returns
-------
Returns the entry retrieved at the specified position.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CTransformationData::SetEntry "
Pylon::DataProcessing::CTransformationData::SetEntry
Set an entry at a specific position in the transformation data.  

Parameters
----------
* `column` :  
    The column of the entry to set (must be lower than number of columns).  
* `row` :  
    The row of the entry to set (must be lower than number of rows).  
* `value` :  
    The new value to set the entry to.  

pre:  

    *   Transformation data must be valid.  
    *   Argument column must be lower than number of columns.  
    *   Argument row must be lower than number of rows.  

\\error Throws an exception if the preconditions aren't met.  
";

// File: class_pylon_1_1_data_processing_1_1_c_update.xml


%feature("docstring") Pylon::DataProcessing::CUpdate "

The `CUpdate` class can be used to check which output data has been generated by
which `CRecipe` data update operation and what the corresponding input data is.  

The pylon recipe uses the concept of updates. An update can consist of the
synchronized processing of a defined set of data by one or more vTools at the
same time. Some vTools can trigger updates on their own, e.g., when triggered by
a preceding update. This causes a chain of updates.  

\\threading The CUpdate class isn't thread-safe.  

C++ includes: Update.h
";

%feature("docstring") Pylon::DataProcessing::CUpdate::CUpdate "
Pylon::DataProcessing::CUpdate::CUpdate
Creates a `CUpdate` that can be used as placeholder for assigning a different
`CUpdate` object later.  

post:  

    *   No data is held.  
    *   `IsValid()` returns `false`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CUpdate::CUpdate "
Pylon::DataProcessing::CUpdate::CUpdate
Copies a `CUpdate` object.  

Parameters
----------
* `rhs` :  
    The update to copy.  

post:  

    *   The update data has been copied.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CUpdate::~CUpdate "
Pylon::DataProcessing::CUpdate::~CUpdate
Destroys a `CUpdate` object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CUpdate::GetNumPrecedingUpdates "
Pylon::DataProcessing::CUpdate::GetNumPrecedingUpdates
Get the number of updates that directly caused this update.  

Returns
-------
The number of updates that caused this update.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CUpdate::GetPrecedingUpdate "
Pylon::DataProcessing::CUpdate::GetPrecedingUpdate
Returns the preceding update at the corresponding index.  

Parameters
----------
* `index` :  
    The index.  

Returns
-------
The preceding update at the corresponding `index`.  

pre:  

    *   `GetNumPrecedingUpdates()` returns a value larger than zero.  
    *   The `index` passed is smaller than the value returned by
        `GetNumPrecedingUpdates()`.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CUpdate::HasBeenTriggeredBy "
Pylon::DataProcessing::CUpdate::HasBeenTriggeredBy
Checks whether the update passed has triggered this update.  

Parameters
----------
* `rhs` :  
    The update to compare to.  

Returns
-------
`true` if this update is equal to `rhs`. True if `rhs` is contained in the list
of preceding updates.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CUpdate::IsValid "
Pylon::DataProcessing::CUpdate::IsValid
Checks whether the update is valid.  

Returns
-------
`true` if this update is valid.  

\\error Doesn't throw C++ exceptions.  
";

// File: class_pylon_1_1_data_processing_1_1_c_variant.xml


%feature("docstring") Pylon::DataProcessing::CVariant "

A variant class that can be used to represent any data type processed by a
`CRecipe`.  

\\threading The `CVariant` class isn't thread-safe.  

C++ includes: Variant.h
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_None`.  

post:  

    *   No data is held.  
    *   `GetDataType()` returns `VariantDataType_None`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `dataType`.  

This constructor is useful if you want to create a variant for a corresponding
type and set the value later using a From method.  

Parameters
----------
* `dataType` :  
    The data type of the variant to create.  

pre: `dataType` is not VariantDataType_None or VariantDataType_Composite.  

post:  

    *   The value is the defined default value. See EVariantDataType for more
        information.  
    *   `GetDataType()` returns `dataType`.  
    *   You can use a From method to set a value later.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates an array of type `dataType`.  

Parameters
----------
* `dataType` :  
    The data type of the variant array to create.  
* `arraySize` :  
    The size of the variant array to create.  

pre: `dataType` is not VariantDataType_None or VariantDataType_Composite.  

post:  

    *   The array items' values have the defined default value. See
        EVariantDataType for more information.  
    *   `GetDataType()` returns `dataType`.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_Boolean`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_Boolean`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_Int64`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_Int64`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a CVariant of type VariantDataType_UInt64.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_UInt64`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_Float`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_Float`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_String`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_String`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_String`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_String`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` array of type `VariantDataType_String` with
`VariantDataType_String` as elements.  

Parameters
----------
* `valueList` :  
    The list of values to assign. Empty list is allowed.  

post:  

    *   The `valueList` passed is copied and held by the `CVariant` created .  
    *   `GetDataType()` returns `VariantDataType_String`.  
    *   `IsArray()` returns `true`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_PylonImage`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is shallow-copied (see `CPylonImage` copy constructor
        for more information) and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_PylonImage`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_Region`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is shallow-copied (see `CRegion` copy constructor for
        more information) and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_Region`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_TransformationData`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_TransformationData`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_PointF2D`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_PointF2D`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_LineF2D`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_LineF2D`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_RectangleF`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_RectangleF`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_CircleF`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_CircleF`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Creates a `CVariant` of type `VariantDataType_EllipseF`.  

Parameters
----------
* `value` :  
    The value to assign.  

post:  

    *   The `value` passed is copied and held by the `CVariant` created.  
    *   `GetDataType()` returns `VariantDataType_EllipseF`.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Copies a variant.  

Parameters
----------
* `other` :  
    The variant to copy.  

post:  

    *   The `rhs` variant passed is shallow-copied.  
    *   If the value of one of the two variant objects is changed, a copy of the
        variant object is created with copy-on-write and the value is assigned.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CVariant "
Pylon::DataProcessing::CVariant::CVariant
Move constructs a variant.  

Parameters
----------
* `other` :  
    The variant to move the content from.  

post:  

    *   The content of the `other` variant passed will be moved to the new
        instance without any copy.  
    *   The `other` variant will be reset to its initial state afterwards.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::IsEqualInstance "
Pylon::DataProcessing::CVariant::IsEqualInstance
Compares a variant object.  

Parameters
----------
* `rhs` :  
    The variant to compare to.  

Returns
-------
`true` if the same data in variant objects is referenced.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::Copy "
Pylon::DataProcessing::CVariant::Copy
Returns a deep copy of the variant object.  

Returns
-------
A deep copy of the variant object.  

post:  

    *   The value the variant references to is copied.  
    *   If the current variant references a subvalue of a composite type, only
        the subtype of the composite type is copied.  
    *   The deep copy is held by the variant returned.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::~CVariant "
Pylon::DataProcessing::CVariant::~CVariant
Destroys a variant object.  

note: Any C++ exception thrown internally while destroying the variant will be
    caught and ignored.  

post:  

    *   Any data held is released or deleted depending on the data type held.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetDataType "
Pylon::DataProcessing::CVariant::GetDataType
Returns the data type of the variant.  

Returns
-------
The data type of the data held.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetContainerType "
Pylon::DataProcessing::CVariant::GetContainerType
Returns the container type of the variant.  

Returns
-------
The container type of the data held.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetNumSubValues "
Pylon::DataProcessing::CVariant::GetNumSubValues
Returns the number of subvalues.  

Returns
-------
The number of subvalues. For example, returns 2 for a PointF{double X, double
Y}.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetSubValueName "
Pylon::DataProcessing::CVariant::GetSubValueName
Returns the name of a subvalue of the value referenced by the variant.  

note: The position of a subvalue is not fixed and can change for different
    versions of pylon.  

Parameters
----------
* `index` :  
    The index.  

Returns
-------
The name of a subvalue of the value referenced by the variant. For example,
returns \"X\" for a PointF{double X, double Y} if 0 is passed as `index`. For
example, returns \"Y\" for a PointF{double X, double Y} if 1 is passed as
`index`.  

pre:  

    *   `GetNumSubValues()` returns a value larger than zero.  
    *   The `index` passed is smaller than the value returned by
        `GetNumSubValues()`.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::HasSubValue "
Pylon::DataProcessing::CVariant::HasSubValue
Returns `true` if a sub alue of the value referenced by the variant with the
name passed exists.  

Parameters
----------
* `subValueName` :  
    The name of the subvalue.  

Returns
-------
`true` if a subvalue of the value referenced by the variant with the name passed
exists. For example, returns `true` for a PointF{double X, double Y} if \"X\" is
passed. For example, returns `false` for a PointF{double X, double Y} if \"Z\"
is passed.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetSubValue "
Pylon::DataProcessing::CVariant::GetSubValue
Returns a variant object referencing the subvalue.  

Parameters
----------
* `subValueName` :  
    The name of the subvalue.  

Returns
-------
A variant object referencing the subvalue with name `subValueName`.  

pre:  

    *   A subvalue of the value referenced by the variant with the
        `subValueName` passed exists.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::SetSubValue "
Pylon::DataProcessing::CVariant::SetSubValue
Changes the value of a subvalue of the value referenced by this variant.  

Parameters
----------
* `subValueName` :  
    The name of the subvalue.  
* `newValue` :  
    The new value for the subvalue.  

pre:  

    *   A subvalue with the `subValueName` passed exists in the value referenced
        by the variant.  
    *   `newValue` must be compatible in type with the subvalue to change.  

post:  

    *   The subvalue has been changed to the new value.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetValueName "
Pylon::DataProcessing::CVariant::GetValueName
Returns the name of the value referenced by the variant.  

Parameters
----------
* `pOptionalRootValueName` :  
    The name of the root value that can optionally be provided by the user. The
    name of root value depends on the context the variant is used in. For
    example, \"lineStartPoint\" can be used for a PointF{double X, double Y}.  

Returns
-------
The name of the value referenced by the variant if it references a subvalue.
`pOptionalRootValueName` or an empty string if it doesn't reference a subvalue.
The name of the value with index in square brackets, e.g., `line`[2], referenced
by the variant if it references an array item.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::IsArray "
Pylon::DataProcessing::CVariant::IsArray
Returns `true` if the value referenced is an array.  

Returns
-------
`true` if the value referenced is an array.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetNumArrayValues "
Pylon::DataProcessing::CVariant::GetNumArrayValues
Returns the number of values in an array.  

Returns
-------
The number of values in an array. Returns 0 if the value is not an array.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetArrayValue "
Pylon::DataProcessing::CVariant::GetArrayValue
Returns a variant object referencing the array item value.  

Parameters
----------
* `index` :  
    The index.  

Returns
-------
A variant object referencing the array item value.  

pre:  

    *   `GetNumArrayValues()` returns a value larger than zero.  
    *   The `index` passed is smaller than the value returned by
        `GetNumArrayValues()`.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ChangeArraySize "
Pylon::DataProcessing::CVariant::ChangeArraySize
Changes the size of an array so that it contains `size` items.  

If `size` is smaller than the current array size, the array size is reduced to
its first `size` elements, removing those beyond.  

If `size` is greater than the current array size, the array size is increased by
inserting as many elements as needed at the end to reach a size of `size`.  

Inserted elements will be of type `VariantDataType_None`.  

Parameters
----------
* `size` :  
    The new size.  

pre:  

    *   `IsArray()` returns `true`.  

post:  

    *   The array size has changed.  
    *   Any old values inside the array are preserved if the new `size` is
        greater or equal than the previous array size.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   Memory allocation fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::SetArrayItemValue "
Pylon::DataProcessing::CVariant::SetArrayItemValue
Changes the value of an array item of the value referenced by this variant.  

Parameters
----------
* `index` :  
    The index.  
* `newValue` :  
    The new value for the array item.  

pre:  

    *   `IsArray()` returns `true`.  
    *   `GetNumArrayValues()` is greater than `index`.  
    *   The `newValue` must be compatible in type with the array item to change.  

post:  

    *   The entry in the array at the given index has been changed to the new
        value.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetArrayDataValues "
Pylon::DataProcessing::CVariant::GetArrayDataValues
Copies Array data values to a buffer.  

Parameters
----------
* `pBuffer` :  
    The target buffer.  
* `bufferSize` :  
    The size of the target buffer.  

pre:  

    *   `IsArray()` returns `true`.  
    *   `GetDataType()` is not VariantDataType_None or
        VariantDataType_Composite.  
    *   The buffer is large enough to hold GetNumArrayValues() of the
        corresponding C++ data type. See EVariantDataType for more information.  
    *   For VariantDataType_PylonImage, VariantDataType_String,
        VariantDataType_Region, or VariantDataType_TransformationData, `pBuffer`
        contains an array of GetNumArrayValues() objects of the corresponding
        C++ data type. If this isn't the case, the call will result in undefined
        behavior.  
    *   For VariantDataType_Boolean, the array item must have a size of 1 byte.
        Basler recommends using the type bool8_t.  
    *   HasError() returns false.  

post:  

    *   `pBuffer` contains the array data values<./li>  
    *   The array size in array items is GetNumArrayValues().  

Returns
-------
Returns the number of array items transferred.  

\\error Throws an exception if the preconditions aren't met. Throws an exception
if the array or any array item is in an error state.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::SetArrayDataValues "
Pylon::DataProcessing::CVariant::SetArrayDataValues
Sets Array data values from a buffer.  

Parameters
----------
* `pBuffer` :  
    The source buffer.  
* `bufferSize` :  
    The size of the source buffer.  

pre:  

    *   `IsArray()` returns `true`.  
    *   `GetDataType()` is not VariantDataType_None or
        VariantDataType_Composite.  
    *   The array size provided in array items is GetNumArrayValues().  
    *   For VariantDataType_PylonImage, VariantDataType_String,
        VariantDataType_Region, or VariantDataType_TransformationData, `pBuffer`
        contains an array of GetNumArrayValues() number of objects of the
        corresponding C++ data type. If this isn't the case, the call will
        result in undefined behavior.  
    *   For VariantDataType_Boolean, the array item must have the size of 1
        byte. Basler recommends using the type bool8_t.  

post:  

    *   `pBuffer` contains the array data values. The array size in array items
        is GetNumArrayValues().  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::CanConvert "
Pylon::DataProcessing::CVariant::CanConvert
Checks whether the value can be converted to target type.  

Parameters
----------
* `targetType` :  
    The target variant data type for conversion.  

Returns
-------
`true` if the value can be converted to target type.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::Convert "
Pylon::DataProcessing::CVariant::Convert
Converts value to target type.  

`CanConvert()` can be used to check whether this `CVariant` can be converted to
`targetType`.  

Parameters
----------
* `targetType` :  
    The target variant data type for conversion.  

Returns
-------
A variant object referencing the converted item value.  

pre:  

    *   `CanConvert()` returns `true`.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToBool "
Pylon::DataProcessing::CVariant::ToBool
Returns the value of the variant for a basic type as bool.  

note: Conversions exist for `VariantDataType_Boolean`, `VariantDataType_Int64`,
    `VariantDataType_UInt64`, `VariantDataType_Float`, and
    `VariantDataType_String`. Can be checked with
    `CanConvert(VariantDataType_Boolean)`.  

Returns
-------
The value of the variant as `bool`.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  
    *   `CanConvert(VariantDataType_Boolean)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToInt64 "
Pylon::DataProcessing::CVariant::ToInt64
Returns the value of the variant for a basic type as int64_t.  

note: The value is undefined if a conversion exceeds the range of the target
    value.  

Conversions exist for `VariantDataType_Boolean`, `VariantDataType_Int64`,
`VariantDataType_UInt64`, `VariantDataType_Float`, and `VariantDataType_String`.
Can be checked with `CanConvert(VariantDataType_Int64)`.  

Returns
-------
Returns the value of the variant as int64_t.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  
    *   `CanConvert(VariantDataType_Int64)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToUInt64 "
Pylon::DataProcessing::CVariant::ToUInt64
Returns the value of the variant for a basic type as uint64_t.  

note: The value is undefined if a conversion exceeds the range of the target
    value.  

Conversions exist for `VariantDataType_Boolean`, `VariantDataType_Int64`,
`VariantDataType_UInt64`, `VariantDataType_Float`, or `VariantDataType_String`.
Can be checked with `CanConvert(VariantDataType_UInt64)`.  

Returns
-------
Returns the value of the variant as uint64_t.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  
    *   `CanConvert(VariantDataType_UInt64)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToDouble "
Pylon::DataProcessing::CVariant::ToDouble
Returns the value of the variant for a basic type as double.  

note: Conversions exist for `VariantDataType_Boolean`, `VariantDataType_Int64`,
    `VariantDataType_UInt64`, `VariantDataType_Float`, or
    `VariantDataType_String`. Can be checked with
    `CanConvert(VariantDataType_Float)`.  

Returns
-------
Returns the value of the variant as double.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  
    *   `CanConvert(VariantDataType_Float)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToString "
Pylon::DataProcessing::CVariant::ToString
Returns the value of the variant for a basic type as string.  

note: The string conversion always uses a dot for decimals.  

Conversions exist for `VariantDataType_Boolean`, `VariantDataType_Int64`,
`VariantDataType_UInt64`, `VariantDataType_Float`, or `VariantDataType_String`.
Can be checked with `CanConvert(VariantDataType_String)`.  

Returns
-------
Returns the value of the variant as string.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, `VariantDataType_String` or
        `VariantDataType_Composite`  
    *   `CanConvert(VariantDataType_String)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToImage "
Pylon::DataProcessing::CVariant::ToImage
Returns the value of the variant for a basic type as CPylonImage.  

Returns
-------
Returns the value of the variant as CPylonImage.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_PylonImage`.  
    *   `CanConvert(VariantDataType_PylonImage)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToRegion "
Pylon::DataProcessing::CVariant::ToRegion
Returns the value of the variant for a basic type as CRegion.  

Returns
-------
Returns the value of the variant as CRegion.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Region`.  
    *   `CanConvert(VariantDataType_Region)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToTransformationData "
Pylon::DataProcessing::CVariant::ToTransformationData
Returns the value of the variant for a basic type as CTransformationData.  

Returns
-------
Returns the value of the variant as CTransformationData.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_TransformationData`.  
    *   `CanConvert(VariantDataType_TransformationData)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToPointF2D "
Pylon::DataProcessing::CVariant::ToPointF2D
Returns the value of the variant as SPointF2D.  

Returns
-------
Returns the value of the variant as SPointF2D.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_PointF2D`.  
    *   `CanConvert(VariantDataType_PointF2D)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToLineF2D "
Pylon::DataProcessing::CVariant::ToLineF2D
Returns the value of the variant as SLineF2D.  

Returns
-------
Returns the value of the variant as SLineF2D.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_LineF2D`.  
    *   `CanConvert(VariantDataType_LineF2D)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToRectangleF "
Pylon::DataProcessing::CVariant::ToRectangleF
Returns the value of the variant as SRectangleF.  

Returns
-------
Returns the value of the variant as SRectangleF.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_RectangleF`.  
    *   `CanConvert(VariantDataType_RectangleF)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToCircleF "
Pylon::DataProcessing::CVariant::ToCircleF
Returns the value of the variant as SCircleF.  

Returns
-------
Returns the value of the variant as SCircleF.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_CircleF`.  
    *   `CanConvert(VariantDataType_CircleF)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::ToEllipseF "
Pylon::DataProcessing::CVariant::ToEllipseF
Returns the value of the variant as SEllipseF.  

Returns
-------
Returns the value of the variant as SEllipseF.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_EllipseF`.  
    *   `CanConvert(VariantDataType_EllipseF)` returns `true`.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromBool "
Pylon::DataProcessing::CVariant::FromBool
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromInt64 "
Pylon::DataProcessing::CVariant::FromInt64
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The variant data type is able to represent the value.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromUInt64 "
Pylon::DataProcessing::CVariant::FromUInt64
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The variant data type is able to represent the value.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromDouble "
Pylon::DataProcessing::CVariant::FromDouble
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The variant data type is able to represent the value.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  

attention: If data type is an integer data type, the value is NOT rounded in a
    mathematical way. It is truncated equivalent to static_cast<int64_t>.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromString "
Pylon::DataProcessing::CVariant::FromString
Changes the value referenced by the variant.  

note: This method will fail if the content of `newValue` is not convertible to
    the type of this `CVariant`.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The variant data type is able to represent the value.  
    *   The type of this `CVariant` is `VariantDataType_Boolean`,
        `VariantDataType_Int64`, `VariantDataType_UInt64`,
        `VariantDataType_Float`, or `VariantDataType_String`.  

post:  

    *   The referenced value has been changed to the value of `newValue` if the
        conversion succeeded.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if:  

*   The preconditions aren't met.  
*   The conversion fails.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromImage "
Pylon::DataProcessing::CVariant::FromImage
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `newValue` must be a valid image.  
    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_PylonImage`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromRegion "
Pylon::DataProcessing::CVariant::FromRegion
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `newValue` must be a valid region.  
    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_Region`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromTransformationData "
Pylon::DataProcessing::CVariant::FromTransformationData
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `newValue` must be valid transformation data.  
    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_TransformationData`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromPointF2D "
Pylon::DataProcessing::CVariant::FromPointF2D
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_PointF2D`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromLineF2D "
Pylon::DataProcessing::CVariant::FromLineF2D
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_LineF2D`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromRectangleF "
Pylon::DataProcessing::CVariant::FromRectangleF
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_RectangleF`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromCircleF "
Pylon::DataProcessing::CVariant::FromCircleF
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_CircleF`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::FromEllipseF "
Pylon::DataProcessing::CVariant::FromEllipseF
Changes the value referenced by the variant.  

Parameters
----------
* `newValue` :  
    The new value for the referenced value.  

pre:  

    *   `IsArray()` returns `false`.  
    *   The type of this `CVariant` is `VariantDataType_EllipseF`.  

post:  

    *   The referenced value has been changed to the value of `newValue`.  
    *   The data type returned by `GetDataType()` hasn't changed.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::GetErrorDescription "
Pylon::DataProcessing::CVariant::GetErrorDescription
Use this method to get the error description of the value.  

Parameters
----------
* `checkSubValues` :  
    Optionally, also check the subvalues.  

Returns
-------
Error description if the value is in error state, an empty string otherwise.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::HasError "
Pylon::DataProcessing::CVariant::HasError
Use this method to check the error state of the value.  

Parameters
----------
* `checkSubValues` :  
    Optionally, check also the subvalues.  

Returns
-------
`true` if the value is in error state.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariant::SetError "
Pylon::DataProcessing::CVariant::SetError
Sets an invalid data error.  

This method is mainly intended for testing how invalid data are handled by a
recipe when a variant is provided as input value.  

Parameters
----------
* `message` :  
    The error message text.  

pre: The data type is not VariantDataType_None.  

post:  

    *   An invalid data error with the message text provided has been added to
        the value.  

\\error Throws an exception if the preconditions aren't met.  
";

// File: class_pylon_1_1_data_processing_1_1_c_variant_container.xml


%feature("docstring") Pylon::DataProcessing::CVariantContainer "

`CVariantContainer` is a map-like container providing an interface like a C++
standard library.  

Values can be processed like this:  

\\threading The `CVariantContainer` class isn't thread-safe.  

C++ includes: VariantContainer.h
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::CVariantContainer "
Pylon::DataProcessing::CVariantContainer::CVariantContainer
Creates an empty variant container object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::CVariantContainer "
Pylon::DataProcessing::CVariantContainer::CVariantContainer
Copies a variant container object.  

Parameters
----------
* `rhs` :  
    The variant container to copy.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::CVariantContainer "
Pylon::DataProcessing::CVariantContainer::CVariantContainer
Move constructs a variant container object.  

Parameters
----------
* `rhs` :  
    The variant container to move the data from.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::~CVariantContainer "
Pylon::DataProcessing::CVariantContainer::~CVariantContainer
Destroys a variant container object.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::begin "
Pylon::DataProcessing::CVariantContainer::begin
Gets the `iterator` to the first element.  

Returns
-------
`iterator` to the first element.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::end "
Pylon::DataProcessing::CVariantContainer::end
Gets the `iterator` to the element after the last element.  

Returns
-------
`iterator` to the element after the last element.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::find "
Pylon::DataProcessing::CVariantContainer::find
Finds an element.  

Parameters
----------
* `key` :  
    The key as string value, typically the name of an input or an output.  

Returns
-------
`iterator` to an element or `end()` if not found.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::count "
Pylon::DataProcessing::CVariantContainer::count
Number of elements with key.  

Parameters
----------
* `key` :  
    The key as string value, typically the name of an input or an output.  

Returns
-------
The number of elements with key, which is either 1 or 0.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::clear "
Pylon::DataProcessing::CVariantContainer::clear
Clears all elements.  

post:  

    *   The `CVariantContainer` has no elements.<
        -   >  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::empty "
Pylon::DataProcessing::CVariantContainer::empty
Checks `CVariantContainer` has no elements.  

Returns
-------
`true` if empty, `false` otherwise.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::size "
Pylon::DataProcessing::CVariantContainer::size
Returns the number of elements.  

Returns
-------
The number of elements.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::erase "
Pylon::DataProcessing::CVariantContainer::erase
Erases an element.  

Returns
-------
`iterator` to next element or `end()` if there is no successor.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::erase "
Pylon::DataProcessing::CVariantContainer::erase
Erases an element by key.  

Parameters
----------
* `key` :  
    The key as string value, typically the name of an input or an output.  

Returns
-------
The number of deletions, which is either 0 or 1.  

\\error Doesn't throw C++ exceptions.  
";

// File: struct_pylon_1_1_data_processing_1_1_enum_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::EnumParameterName "

Defines an enum parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::EnumParameterName::EnumParameterName "
Pylon::DataProcessing::EnumParameterName::EnumParameterName";

// File: struct_pylon_1_1_data_processing_1_1_float_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::FloatParameterName "

Defines a float parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::FloatParameterName::FloatParameterName "
Pylon::DataProcessing::FloatParameterName::FloatParameterName";

// File: class_pylon_1_1_data_processing_1_1_i_event_observer.xml


%feature("docstring") Pylon::DataProcessing::IEventObserver "

An interface that can be used to receive event data from a `CRecipe`.  

\\threading This interface is called from multiple internal threads of the
`CRecipe`.  

C++ includes: IEventObserver.h
";

%feature("docstring") Pylon::DataProcessing::IEventObserver::~IEventObserver "
Pylon::DataProcessing::IEventObserver::~IEventObserver";

%feature("docstring") Pylon::DataProcessing::IEventObserver::OnEventSignaled "
Pylon::DataProcessing::IEventObserver::OnEventSignaled
This method is called when the graph of the `CRecipe` detects an event, e.g., an
error change of a vtool.  

Parameters
----------
* `recipe` :  
    The recipe that produced the output.  
* `pEvents` :  
    List of event infos as plain C array.  
* `numEvents` :  
    Number of entries in that list.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

%feature("docstring") Pylon::DataProcessing::IEventObserver::OnDeregistered "
Pylon::DataProcessing::IEventObserver::OnDeregistered
This method is called when the event observer is deregistered from the recipe.
It can be used to delete the event observer by overloading the method. The
default implementation of this method does nothing.  

Parameters
----------
* `recipe` :  
    The recipe that the observer is deregistered from.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

// File: struct_pylon_1_1_data_processing_1_1_integer_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::IntegerParameterName "

Defines an integer parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::IntegerParameterName::IntegerParameterName "
Pylon::DataProcessing::IntegerParameterName::IntegerParameterName";

// File: class_pylon_1_1_data_processing_1_1_i_output_observer.xml


%feature("docstring") Pylon::DataProcessing::IOutputObserver "

An interface that can be used to receive output data from a `CRecipe`.  

\\threading This interface is called from multiple internal threads of the
`CRecipe`.  

C++ includes: IOutputObserver.h
";

%feature("docstring") Pylon::DataProcessing::IOutputObserver::~IOutputObserver "
Pylon::DataProcessing::IOutputObserver::~IOutputObserver";

%feature("docstring") Pylon::DataProcessing::IOutputObserver::OutputDataPush "
Pylon::DataProcessing::IOutputObserver::OutputDataPush
This method is called when an output of the `CRecipe` pushes data out.  

Parameters
----------
* `recipe` :  
    The recipe that produced the output.  
* `value` :  
    A variant container containing the output data.  
* `update` :  
    The corresponding update.  
* `userProvidedId` :  
    This ID is passed to distinguish between different events. This ID has been
    passed when calling `CRecipe::RegisterOutputObserver()`.  

\\error C++ exceptions thrown by this method are caught and ignored.  
";

%feature("docstring") Pylon::DataProcessing::IOutputObserver::OnDeregistered "
Pylon::DataProcessing::IOutputObserver::OnDeregistered
This method is called when the output observer is deregistered from the recipe.
It can be used to delete the output observer by overloading the method.  

Parameters
----------
* `recipe` :  
    The recipe that the observer is deregistered from.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

// File: struct_pylon_1_1_data_processing_1_1_c_variant_container_1_1iterator.xml


%feature("docstring") Pylon::DataProcessing::CVariantContainer::iterator "

Iterator interface.  

C++ includes: VariantContainer.h
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::iterator::iterator "
Pylon::DataProcessing::CVariantContainer::iterator::iterator
Creates an empty variant container iterator object.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::iterator::iterator "
Pylon::DataProcessing::CVariantContainer::iterator::iterator
Copies a variant container iterator object.  

Parameters
----------
* `rhs` :  
    The variant container iterator to copy.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::iterator::iterator "
Pylon::DataProcessing::CVariantContainer::iterator::iterator
Move constructs a variant container iterator object.  

Parameters
----------
* `rhs` :  
    The variant container iterator to move the data from.  
";

%feature("docstring") Pylon::DataProcessing::CVariantContainer::iterator::~iterator "
Pylon::DataProcessing::CVariantContainer::iterator::~iterator
Destroys a variant container iterator object.  
";

// File: class_pylon_1_1_data_processing_1_1_i_update_observer.xml


%feature("docstring") Pylon::DataProcessing::IUpdateObserver "

An interface that can be used to get notified about the processing of updates.  

\\threading This interface is called from multiple internal threads of the
`Pylon::DataProcessing::CRecipe`.  

C++ includes: IUpdateObserver.h
";

%feature("docstring") Pylon::DataProcessing::IUpdateObserver::~IUpdateObserver "
Pylon::DataProcessing::IUpdateObserver::~IUpdateObserver";

%feature("docstring") Pylon::DataProcessing::IUpdateObserver::UpdateDone "
Pylon::DataProcessing::IUpdateObserver::UpdateDone
This method is called when an update of a `Pylon::DataProcessing::CRecipe` has
been processed completely.  

note: If this update has triggered further updates, depending on the vTools used
    in an recipe, the output data may not be available yet.  

Parameters
----------
* `recipe` :  
    The recipe that processed the update.  
* `update` :  
    The update that was processed completely.  
* `userProvidedId` :  
    This ID is passed to distinguish between different events. This ID has been
    passed when calling `CRecipe::TriggerUpdateAsync()` or
    `CRecipe:TriggerUpdate()`.  

\\error C++ Exceptions thrown by this method are caught and ignored.  
";

// File: struct_pylon_1_1_data_processing_1_1_c_variant_container_1_1keyvalue__pair.xml


%feature("docstring") Pylon::DataProcessing::CVariantContainer::keyvalue_pair "

Key value pair used by the iterator.  

C++ includes: VariantContainer.h
";

// File: struct_pylon_1_1_data_processing_1_1_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::ParameterName "

Defines a generic parameter name.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::ParameterName::ParameterName "
Pylon::DataProcessing::ParameterName::ParameterName";

// File: struct_pylon_1_1_data_processing_1_1_s_circle_f.xml


%feature("docstring") Pylon::DataProcessing::SCircleF "

The data of a CVariant object with the VariantDataType_CircleF data type.  

C++ includes: CircleF.h
";

%feature("docstring") Pylon::DataProcessing::SCircleF::SCircleF "
Pylon::DataProcessing::SCircleF::SCircleF
Creates a circle and initializes it with 0.  
";

%feature("docstring") Pylon::DataProcessing::SCircleF::SCircleF "
Pylon::DataProcessing::SCircleF::SCircleF
Creates a circle and initializes it.  

Parameters
----------
* `centerX` :  
    The x coordinate of the center of the circle.  
* `centerY` :  
    The y coordinate of the center of the circle.  
* `radius` :  
    The radius of the circle.  
";

%feature("docstring") Pylon::DataProcessing::SCircleF::SCircleF "
Pylon::DataProcessing::SCircleF::SCircleF
Creates a circle and initializes it.  

Parameters
----------
* `center` :  
    The center of the circle.  
* `radius` :  
    The radius of the circle.  
";

// File: struct_pylon_1_1_data_processing_1_1_s_ellipse_f.xml


%feature("docstring") Pylon::DataProcessing::SEllipseF "

The data of a CVariant object with the VariantDataType_EllipseF data type.  

C++ includes: EllipseF.h
";

%feature("docstring") Pylon::DataProcessing::SEllipseF::SEllipseF "
Pylon::DataProcessing::SEllipseF::SEllipseF
Creates an ellipse and initializes it with 0.  
";

%feature("docstring") Pylon::DataProcessing::SEllipseF::SEllipseF "
Pylon::DataProcessing::SEllipseF::SEllipseF
Creates an ellipse and initializes it.  

Parameters
----------
* `centerX` :  
    The x coordinate of the center of the ellipse.  
* `centerY` :  
    The y coordinate of the center of the ellipse.  
* `radius1` :  
    The radius of the ellipse that is parallel to the x axis when the ellipse is
    in its original state, i.e., it hasn't been rotated.  
* `radius2` :  
    The radius of the ellipse that is parallel to the y axis when the ellipse is
    in its original state, i.e., it hasn't been rotated.  
* `rotation` :  
    The rotation of the ellipse in radiant.  
";

%feature("docstring") Pylon::DataProcessing::SEllipseF::SEllipseF "
Pylon::DataProcessing::SEllipseF::SEllipseF
Creates an ellipse and initializes it.  

Parameters
----------
* `center` :  
    The center of the ellipse.  
* `radius1` :  
    The radius of the ellipse that is parallel to the x axis when the ellipse is
    in its original state, i.e., it hasn't been rotated.  
* `radius2` :  
    The radius of the ellipse that is parallel to the y axis when the ellipse is
    in its original state, i.e., it hasn't been rotated.  
* `rotation` :  
    The rotation of the ellipse in radiant.  
";

// File: struct_pylon_1_1_data_processing_1_1_s_generic_output_observer_result.xml


%feature("docstring") Pylon::DataProcessing::SGenericOutputObserverResult "

A container for recipe output data.  

C++ includes: GenericOutputObserver.h
";

// File: struct_pylon_1_1_data_processing_1_1_s_line_f2_d.xml


%feature("docstring") Pylon::DataProcessing::SLineF2D "

The data of a CVariant object with the VariantDataType_LineF2D data type.  

C++ includes: LineF2D.h
";

%feature("docstring") Pylon::DataProcessing::SLineF2D::SLineF2D "
Pylon::DataProcessing::SLineF2D::SLineF2D
Creates a line and initializes it with 0.  
";

%feature("docstring") Pylon::DataProcessing::SLineF2D::SLineF2D "
Pylon::DataProcessing::SLineF2D::SLineF2D
Creates a line and initializes it.  

Parameters
----------
* `pointAX` :  
    The x coordinate of point A of the line.  
* `pointAY` :  
    The y coordinate of point A of the line.  
* `pointBX` :  
    The x coordinate of point B of the line.  
* `pointBY` :  
    The y coordinate of point B of the line.  
";

%feature("docstring") Pylon::DataProcessing::SLineF2D::SLineF2D "
Pylon::DataProcessing::SLineF2D::SLineF2D
Creates a line and initializes it.  

Parameters
----------
* `pointA` :  
    Point A of the line.  
* `pointB` :  
    Point B of the line.  
";

// File: struct_pylon_1_1_data_processing_1_1_s_point_f2_d.xml


%feature("docstring") Pylon::DataProcessing::SPointF2D "

The data of a CVariant object with the VariantDataType_PointF2D data type.
PointF2D can provide image coordinates in pixels and world coordinates in
meters. The origin (0,0) of image coordinates defined by a PointF2D is the
center of the top left image pixel.  

C++ includes: PointF2D.h
";

%feature("docstring") Pylon::DataProcessing::SPointF2D::SPointF2D "
Pylon::DataProcessing::SPointF2D::SPointF2D
Creates a point and initializes it with (0,0).  
";

%feature("docstring") Pylon::DataProcessing::SPointF2D::SPointF2D "
Pylon::DataProcessing::SPointF2D::SPointF2D
Creates a point and initializes it with (x,y).  
";

// File: struct_pylon_1_1_data_processing_1_1_s_rectangle_f.xml


%feature("docstring") Pylon::DataProcessing::SRectangleF "

The data of a CVariant object with the VariantDataType_RectangleF data type.  

C++ includes: RectangleF.h
";

%feature("docstring") Pylon::DataProcessing::SRectangleF::SRectangleF "
Pylon::DataProcessing::SRectangleF::SRectangleF
Creates a rectangle and initializes it with 0.  
";

%feature("docstring") Pylon::DataProcessing::SRectangleF::SRectangleF "
Pylon::DataProcessing::SRectangleF::SRectangleF
Creates a rectangle and initializes it.  

Parameters
----------
* `centerX` :  
    The x coordinate of the center of the rectangle.  
* `centerY` :  
    The y coordinate of the center of the rectangle.  
* `width` :  
    The width of the rectangle.  
* `height` :  
    The height of the rectangle.  
* `rotation` :  
    The rotation of the rectangle in radiant.  
";

%feature("docstring") Pylon::DataProcessing::SRectangleF::SRectangleF "
Pylon::DataProcessing::SRectangleF::SRectangleF
Creates a rectangle and initializes it.  

Parameters
----------
* `center` :  
    The center of the rectangle.  
* `width` :  
    The width of the rectangle.  
* `height` :  
    The height of the rectangle.  
* `rotation` :  
    The rotation of the rectangle in radiant.  
";

// File: struct_pylon_1_1_data_processing_1_1_s_region_entry_r_l_e32.xml


%feature("docstring") Pylon::DataProcessing::SRegionEntryRLE32 "

Entry for the run-length encoded pixels of a region. Region entries must be
sorted line-wise starting with line 0 and then column-wise starting with column
0.  

C++ includes: RegionEntry.h
";

// File: struct_pylon_1_1_data_processing_1_1_string_parameter_name.xml


%feature("docstring") Pylon::DataProcessing::StringParameterName "

Defines a string parameter name by combining the parameter name string and the
parameter type information.  

C++ includes: ParameterNames.h
";

%feature("docstring") Pylon::DataProcessing::StringParameterName::StringParameterName "
Pylon::DataProcessing::StringParameterName::StringParameterName";

// File: namespace_pylon.xml

// File: namespace_pylon_1_1_data_processing.xml

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CParameter` from the `parameterName` passed or an empty
Pylon::CParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CParameter` from the `parameterName` passed or an empty
Pylon::CParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CIntegerParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CIntegerParameter` from the `parameterName` passed or an empty
Pylon::CIntegerParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CFloatParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CFloatParameter` from the `parameterName` passed or an empty
Pylon::CFloatParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CStringParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CStringParameter` from the `parameterName` passed or an empty
Pylon::CStringParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CBooleanParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CBooleanParameter` from the `parameterName` passed or an empty
Pylon::CBooleanParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CArrayParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CArrayParameter` from the `parameterName` passed or an empty
Pylon::CArrayParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CCommandParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CCommandParameter` from the `parameterName` passed or an empty
Pylon::CCommandParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Get "
Pylon::DataProcessing::Get
Returns a `Pylon::CEnumParameter` from the requested parameter name.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`Pylon::CEnumParameter` from the `parameterName` passed or an empty
Pylon::CEnumParameter if `parameterName` is not contained.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the parameter is contained in the parameter collection.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the parameter is contained in the parameter collection.  

Parameters
----------
* `parameterName` :  
    The name of the parameter.  

Returns
-------
`true`, if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the integer parameter is contained in the parameter
collection.  

Parameters
----------
* `parameterName` :  
    The name of the integer parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the boolean parameter is contained in the parameter
collection.  

Parameters
----------
* `parameterName` :  
    The name of the boolean parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the enum parameter is contained in the parameter collection.  

Parameters
----------
* `parameterName` :  
    The name of the enum parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the string parameter is contained in the parameter collection.  

Parameters
----------
* `parameterName` :  
    The name of the string parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the float parameter is contained in the parameter collection.  

Parameters
----------
* `parameterName` :  
    The name of the float parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the array parameter is contained in the parameter collection.  

Parameters
----------
* `parameterName` :  
    The name of the port parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::Contains "
Pylon::DataProcessing::Contains
Indicates whether the command parameter is contained in the parameter
collection.  

Parameters
----------
* `parameterName` :  
    The name of the command parameter.  

Returns
-------
`true` if a parameter with the `parameterName` passed is contained in the
parameter collection, false otherwise.  

Exceptions
----------
* `Doesn't` :  
    throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::GetAllParameterNames "
Pylon::DataProcessing::GetAllParameterNames
Gets a `StringList_t` with the names of all parameters in this parameter
collection.  

Returns
-------
`StringList_t` with the names of all parameters in this parameter collection.  
";

%feature("docstring") Pylon::DataProcessing::IsValidRegionType "
Pylon::DataProcessing::IsValidRegionType
Checks whether a given region type is valid.  

Parameters
----------
* `regionType` :  
    The region type to check.  

Returns
-------
Returns true if the region type is valid or false otherwise.  

\\error Doesn't throw C++ exceptions.  
";

%feature("docstring") Pylon::DataProcessing::BitPerRegionElement "
Pylon::DataProcessing::BitPerRegionElement
Determines the element size in bits of a given region type.  

Parameters
----------
* `regionType` :  
    The region type to get the element size of.  

pre:  

    *   The region type must be valid.  

Returns
-------
Returns the size of an element of a region type in bits.  

\\error Throws an exception if the preconditions aren't met.  
";

%feature("docstring") Pylon::DataProcessing::ComputeRegionSize "
Pylon::DataProcessing::ComputeRegionSize
Determines the required data size of a region with a given region type and
number of region elements.  

Parameters
----------
* `regionType` :  
    The region type to be used.  
* `elementCount` :  
    The number of region elements.  

pre:  

    *   The region type must be valid.  

Returns
-------
Returns the required data size of a region with a given region type and number
of region elements.  

\\error Throws an exception if the preconditions aren't met.  
";

// File: _acquisition_mode_8h.xml

// File: _builders_recipe_8h.xml

// File: _callable_event_observer_8h.xml

// File: _callable_output_observer_8h.xml

// File: _callable_update_observer_8h.xml

// File: _circle_f_8h.xml

// File: _ellipse_f_8h.xml

// File: _generic_output_observer_8h.xml

// File: _i_event_observer_8h.xml

// File: _i_output_observer_8h.xml

// File: _i_parameter_collection_8h.xml

// File: _i_update_observer_8h.xml

// File: _line_f2_d_8h.xml

// File: _parameter_names_8h.xml

// File: _point_f2_d_8h.xml

// File: _pylon_data_processing_8h.xml

// File: _pylon_data_processing_includes_8h.xml

// File: _pylon_data_processing_version_8h.xml

// File: _queue_mode_8h.xml

// File: _recipe_8h.xml

// File: _rectangle_f_8h.xml

// File: _region_8h.xml

// File: _region_entry_8h.xml

// File: _region_type_8h.xml

// File: _region_user_buffer_event_handler_8h.xml

// File: _transformation_data_8h.xml

// File: _update_8h.xml

// File: _variant_8h.xml

// File: _variant_container_8h.xml

// File: _variant_container_type_8h.xml

// File: _variant_data_type_8h.xml

// File: dir_5043b2f144d5f322b3d454b2efef9db4.xml

// File: dir_6253a1aaf92bae6c2d2e9ee40ee5135c.xml

// File: dir_c3360addf176ad57f7364093e004800e.xml

// File: dir_7a153bad9178605b17280b5b16bdfe05.xml

// File: dir_8bf978817657829de860156342dc6797.xml

// File: dir_f75f1aac289c542387affbfce84ea76e.xml

