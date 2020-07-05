//
// Created by Fredkiss3 on 04/07/2020.
//

#include "Event.h"

namespace KGE
{
    EventQueue *EventQueue::s_Instance = nullptr;

    std::ostream &operator<<(std::ostream &out, const Event &e)
    {
        return out << e.GetData();
    }

    void ListenerContainer::Register(EventListener *listener)
    {
        for (auto handler : listener->GetHandlers())
        {
            if (m_ListenerMap.find(handler->GetEventName()) != m_ListenerMap.end())
            {
                // If key exists then add the listener to the cache
                m_ListenerMap[handler->GetEventName()].push_back(listener);
            }
            else
            {
                m_ListenerMap[handler->GetEventName()] = std::vector<EventListener *>(1, listener);
            }
        }
    }

    void ListenerContainer::UnRegister(EventListener *listener)
    {
        for (auto handler : listener->GetHandlers())
        {
            auto it = m_ListenerMap.find(handler->GetEventName());
            if (it != m_ListenerMap.end())
            {
                // Get List of listeners associated with key
                auto eList = it->second;

                // find listener onto the list
                auto found = std::find(eList.begin(), eList.end(), listener);
                if (found != eList.end())
                {
                    // remove listener from the list
                    eList.erase(found);
                }
            }
        }
    }

    std::vector<EventListener *> ListenerContainer::Get(const char *eventName) const
    {
        // Initialize to size zero vector
        std::vector<EventListener *> eList(0);
        auto it = m_ListenerMap.find(eventName);
        if (it != m_ListenerMap.end())
        {
            eList = it->second;
        }
        return eList;
    }

} // namespace KGE
