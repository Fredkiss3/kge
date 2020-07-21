#pragma once

#include "headers.h"
#include "KGE/Core/Entity.h"
#include "KGE/Base.h"

#define CLASS_TYPE(type)                                 \
    static const char *GetStaticType() { return #type; } \
    virtual const char *GetType() const override { return GetStaticType(); }
#define EVENT_TYPE(type) #type

namespace KGE
{
class Scene;

/*
     * We use struct here because we Want to have a default initializer
     * and all attributes should be public
     * */
struct Event
{
    virtual std::string GetData() const = 0;

    const std::string Print() const;
    virtual ~Event() = default;

    Ref<Scene> scene = nullptr;
    Ref<Entity> entity = nullptr;

    bool handled = false;

    virtual const char *GetType() const = 0;
    static const char *GetStaticType() { return "Event"; }

    // to give full control to the queue only
    friend class EventQueue;

protected:
    /*
         * This will be used to get the type of the element
         * It will be used primarly When logging the call to an event
         * */
    virtual std::string GetTypeName() const
    {
        return type(*this);
    };
};

class EventQueue
{
public:
    /*
         * Post an event onto the event queue
         * */
    void DispatchEvent(Event *e, bool immediate = false)
    {
        //K_CORE_DEBUG("Adding Event : {} to the queue", e->Print());

        // Casting the raw pointer to a shared_ptr
        Ref<Event> ev(e);
        if (immediate)
        {
            m_EventList.push_front(ev);
        }
        else
        {
            m_NextEventList.push_back(ev);
        }
    }

    static void Dispatch(Event *e, bool immediate = false)
    {
        GetInstance();
        s_Instance->DispatchEvent(e, immediate);
    }

    /**
         * Swap & get the next event to process
         * @return the next event to process
         */
    Ref<Event> GetNextEvent()
    {
        Ref<Event> e = nullptr;
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

    static Ref<EventQueue> &GetInstance()
    {
        if (s_Instance == nullptr)
        {
            s_Instance = Ref<EventQueue>(new EventQueue());
        }

        return s_Instance;
    }

private:
    std::deque<Ref<Event>> m_EventList;
    std::deque<Ref<Event>> m_NextEventList;
    //Event *m_Cursor;
    static Ref<EventQueue> s_Instance;

    EventQueue() : m_EventList(0), m_NextEventList(0) {}

}; // namespace KGE

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

    std::vector<std::string> GetSupportedEvents() const
    {
        return m_SupportedEvents;
    }

    virtual ~EventListener() = default;

    virtual void OnEvent(Event const &e) {}

protected:
    void Bind(const char *event)
    {
        m_SupportedEvents.push_back(std::string(event));
    }

private:
    std::vector<std::string> m_SupportedEvents;
};

class ListenerContainer
{
public:
    void Add(EventListener &listener);

    void Remove(EventListener &listener);

    std::vector<Ref<EventListener>> Get(const char *event) const;

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
    std::vector<Ref<EventListener>> m_Listeners;
    std::map<std::string, std::vector<Ref<EventListener>>> m_ListenerMap;
};

} // namespace KGE
