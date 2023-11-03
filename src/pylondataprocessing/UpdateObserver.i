%rename(Recipe) Pylon::DataProcessing::CRecipe;
%rename(UpdateObserver) Pylon::DataProcessing::IUpdateObserver;
%feature("director") Pylon::DataProcessing::IUpdateObserver;

%include <pylondataprocessing/IUpdateObserver.h>;