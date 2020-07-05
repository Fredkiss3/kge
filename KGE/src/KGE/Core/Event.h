#pragma once

#include "headers.h"
#include "Scene.h"
#include "KGE/Base.h"

#define EVENT_CLASS_TYPE(type)                           \
    static const char *GetStaticType() { return #type; } \
    virtual const char *GetEventType() const override { return GetStaticType(); }
#define EVENT_TYPE(type) #type

namespace KGE
{
    /*
     * We use struct here because we Want to have a default initializer
     * and all attributes should be public
     * */
    struct Event
    {

        virtual std::string GetData() const = 0;
        std::string Print() const
        {
            return GetTypeName() + "{ " + (scene != nullptr ? scene->GetName() + ", " : "") + "Handled=" +
                   (handled ? "true, " : "false, ") + GetData() + " }";
        }

        virtual ~Event() = default;

        Scene *scene = nullptr;
        Entity *onlyEntity = nullptr;

        bool handled = false;
        virtual const char *GetEventType() const = 0;

        // to give full control to the queue only
        friend class EventQueue;
        static const char *GetStaticType() { return "Event"; }

    protected:
        /*
         * This will be used to get the type of the element
         * It will be used primarly When logging the call to an event
         * */
        virtual std::string GetTypeName() const
        {
            std::string fullName(type(*this));
            return fullName;
        };
    };

    class EventQueue
    {
    public:
        /*
         * Post an event onto the event queue
         * */
        void Dispatch(Event *e, bool immediate = false)
        {
            K_CORE_DEBUG("Adding Event : {} to the queue", e->Print());
            if (immediate)
            {
                m_EventList.push_front(e);
            }
            else
            {
                m_NextEventList.push_back(e);
            }
        }

        /**
         * Swap & get the next event to process
         * @return the next event to process
         */
        Event *GetNextEvent()
        {
            Event *e = nullptr;
            if (m_EventList.size() > 0)
            {
                // Pick event
                e = m_EventList.front();
                // go to next event
                //m_EventList.pop();
                m_EventList.pop_front();
            }

            return e;
        }

        /*
         * Swap the next events to the current
         */
        void SwapEvents()
        {
            //  swap the lists
            m_EventList.swap(m_NextEventList);
        }

        static EventQueue *GetInstance()
        {
            if (s_Instance == nullptr)
            {
                s_Instance = new EventQueue();
            }

            return s_Instance;
        }

    private:
        std::deque<Event *> m_EventList;
        std::deque<Event *> m_NextEventList;
        //Event *m_Cursor;
        static EventQueue *s_Instance;
        EventQueue() : m_EventList(0), m_NextEventList(0) {}

    }; // namespace KGE

    // This is the interface for EventHandler that each specialization will use
    class HandlerBase
    {
    public:
        // Call the member function
        void exec(Event *evnt)
        {
            call(evnt);
        }

        virtual std::string GetEventName() const { return m_EventName; }

    private:
        // Implemented by EventHandler
        virtual void call(Event *evnt) = 0;

    protected:
        std::string m_EventName;
    };

    template <class T, typename EventType>
    class EventHandler : public HandlerBase
    {
    public:
        typedef void (T::*EventCallBack)(EventType *);

        EventHandler(T *instance, EventCallBack callBack) : instance{instance},
                                                            m_CallBack{callBack}
        {
            m_EventName = EventType::GetStaticType();
        };

        void call(Event *evnt) override
        {
            // Cast event to the correct type and call member function
            (instance->*m_CallBack)(static_cast<EventType *>(evnt));
        }

    private:
        // Pointer to class instance of the callback to call
        T *instance;

        // Pointer to member function
        EventCallBack m_CallBack;
    };

    class EventListener
    {
    public:
        /*
         * This will be used to get the type of the element
         * It will be used primarly When logging the call to an event
         * */
        virtual std::string GetTypeName() const
        {
            std::string fullName(type(*this));
            return fullName;
        };

        template <typename EventType>
        void handle(EventType *event)
        {
            std::string type(event->GetEventType());
            if (m_HandlersMap.find(type) != m_HandlersMap.end())
            {
                auto handler = m_HandlersMap[type];
                handler->exec(event);
            }
        }

        /**
         * For registering listeners in container
         */
        virtual std::vector<HandlerBase *> GetHandlers() const
        {
            return m_HandlerCache;
        }

    protected:
        void DumpHandlerCache() const
        {
            for (auto it = m_HandlersMap.begin(); it != m_HandlersMap.end(); ++it)
            {
                K_CORE_TRACE("Found Handler {1} for {0}", it->first, it->second->GetEventName());
            }
        }

        /**
         * Register handlers to be called when this type of event occurs
         */
        template <class T, class EventType>
        void Bind(T *instance, void (T::*eventCallBack)(EventType *))
        {

            // get event Name and add it to the map
            HandlerBase *handler = new EventHandler<T, EventType>(instance, eventCallBack);
            m_HandlersMap[EventType::GetStaticType()] = handler;
            // Add event to list in order to access it from container
            m_HandlerCache.push_back(m_HandlersMap[EventType::GetStaticType()]);
        };

    private:
        std::vector<HandlerBase *> m_HandlerCache;
        std::map<std::string, HandlerBase *> m_HandlersMap;
    };

    class ListenerContainer
    {
    public:
        void Register(EventListener *listener);

        void UnRegister(EventListener *listener);

        std::vector<EventListener *> Get(const char *event) const;

        void DumpListenerMap() const
        {
            for (auto it = m_ListenerMap.begin(); it != m_ListenerMap.end(); ++it)
            {
                for (auto listener : it->second)
                {
                    K_CORE_TRACE("Got listener {0} for {1}", listener->GetTypeName(), it->first);
                }
            }
        }

    protected:
        std::map<std::string, std::vector<EventListener *>> m_ListenerMap;
    };

} // namespace KGE
