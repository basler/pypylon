%rename(GenericOutputObserverResult) Pylon::DataProcessing::SGenericOutputObserverResult;
%rename(GenericOutputObserver) Pylon::DataProcessing::CGenericOutputObserver;
%rename(RetrieveFullResult) Pylon::DataProcessing::CGenericOutputObserver::GetResult;
%rename(RetrieveResult) Pylon::DataProcessing::CGenericOutputObserver::GetResultContainer;
%ignore SGenericOutputObserverResult::Container;

namespace Pylon
{
    namespace DataProcessing
    {
        struct SGenericOutputObserverResult
        {
            CUpdate Update; //!< The update the output belongs to.
            intptr_t UserProvidedID = 0; //!< The user provided id belonging to the update.
            CVariantContainer Container; //!< The output data of the recipe.
        };
    
        class CGenericOutputObserver : public IOutputObserver
        {
        public:
            CGenericOutputObserver()
                : m_waitObject(Pylon::WaitObjectEx::Create())
            {
            }

            // Implements IOutputObserver::OutputDataPush.
            // This method is called when an output of the CRecipe pushes data out.
            // The call of the method can be performed by any thread of the thread pool of the recipe.
            void OutputDataPush(
                CRecipe& recipe,
                CVariantContainer value,
                const CUpdate& update,
                intptr_t userProvidedId) override
            {
                // Add data to the result queue in a thread-safe way.
                AutoLock scopedLock(m_memberLock);

                // The following variables are not used here:
                PYLON_UNUSED(recipe);

                SGenericOutputObserverResult outputData = {update, userProvidedId, value};
                m_queue.emplace_back(outputData);
                m_waitObject.Signal();
            }

            // Get the wait object for waiting for data.
            const WaitObject& GetWaitObject()
            {
                return m_waitObject;
            }

            size_t GetNumResults() const
            {
                AutoLock scopedLock(m_memberLock);
                return !m_queue.empty();
            }
            
            void Clear()
            {
                AutoLock scopedLock(m_memberLock);
                m_waitObject.Reset();
                m_queue.clear();
            }

            // Get one result data object from the queue.
            CVariantContainer GetResultContainer()
            {
                AutoLock scopedLock(m_memberLock);
                if (m_queue.empty())
                {
                    return CVariantContainer();
                }

                auto resultDataOut = std::move(m_queue.front());
                m_queue.pop_front();
                if (m_queue.empty())
                {
                    m_waitObject.Reset();
                }
                return resultDataOut.Container;
            }
            
            SGenericOutputObserverResult GetResult()
            {
                AutoLock scopedLock(m_memberLock);
                if (m_queue.empty())
                {
                    return {CUpdate(), 0, CVariantContainer()};
                }

                auto result = std::move(m_queue.front());
                m_queue.pop_front();
                if (m_queue.empty())
                {
                    m_waitObject.Reset();
                }
                return result;
            }

        private:
            mutable CLock m_memberLock;
            WaitObjectEx m_waitObject;
            std::list<SGenericOutputObserverResult> m_queue;
        };
    }
}

%extend Pylon::DataProcessing::SGenericOutputObserverResult {
    CVariantContainer GetContainer()
    {
        return $self->Container;
    }
}

%pythoncode %{ GenericOutputObserverResult.Container = property(GenericOutputObserverResult.GetContainer) %}