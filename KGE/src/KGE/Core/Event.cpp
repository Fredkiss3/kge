//
// Created by Fredkiss3 on 04/07/2020.
//
#include <headers.h>
#include "Event.h"

namespace KGE
{
    EventQueue *EventQueue::s_Instance = nullptr;

    void ListenerContainer::Add(EventListener &listener)
    {
        // create a ref to the pointer, this will be added both to our listeners' list and to the cache
        Ref<EventListener> ref(&listener);
        for (auto eventName : listener.GetSupportedEvents())
        {
            if (m_ListenerMap.find(eventName) != m_ListenerMap.end())
            {
                // If key exists then add the listener to the cache
                m_ListenerMap[eventName].push_back(ref);
            }
            else
            {
                // create a new pair of  "eventName <-> listener"
                m_ListenerMap[eventName] = std::vector<Ref<EventListener>>(1, ref);
            }
        }

        // add listener to the list of events
        m_Listeners.push_back(Ref<EventListener>(ref));
    }

    void ListenerContainer::Remove(EventListener &listener)
    {
        // create a ref to the pointer, in order to test equality between listeners
        Ref<EventListener> ref(&listener);

        for (auto eventName : listener.GetSupportedEvents())
        {
            auto it = m_ListenerMap.find(eventName);
            if (it != m_ListenerMap.end())
            {
                // Get List of listeners associated with key
                auto eList = it->second;

                // find listener onto the cache
                auto found = std::find(eList.begin(), eList.end(), ref);
                if (found != eList.end())
                {
                    // remove listener from the cache
                    eList.erase(found);
                }
            }

            // Remove listener from listeners attached to this container
            auto found = std::find(m_Listeners.begin(), m_Listeners.end(), ref);
            if (found != m_Listeners.end())
            {
                // remove listener from the list of listeners
                m_Listeners.erase(found);
            }
        }
    }

    std::vector<Ref<EventListener>> ListenerContainer::Get(const char *eventNameName) const
    {
        // Initialize to size zero vector
        std::vector<Ref<EventListener>> eList(0);
        auto it = m_ListenerMap.find(eventNameName);
        if (it != m_ListenerMap.end())
        {
            eList = it->second;
        }
        return eList;
    }

} // namespace KGE
