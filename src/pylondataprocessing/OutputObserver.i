%rename(Recipe) Pylon::DataProcessing::CRecipe;
%rename(OutputObserver) Pylon::DataProcessing::IOutputObserver;
%feature("director") Pylon::DataProcessing::IOutputObserver;

%include <pylondataprocessing/IOutputObserver.h>;