//
// Created by Fredkiss3 on 04/07/2020.
//

#pragma once
#include "KGE/Base.h"
#include "Log.h"
#include "System.h"
#include "Events.h"

namespace KGE
{

    class EntityManager : public System
    {
    public:
        EntityManager()
        {
            Bind(EVENT_TYPE(Init));
        }

        void OnEvent(Event const &e) override
        {
            if (e.GetType() == EVENT_TYPE(Init))
            {
                OnInit((Init &)e);
            }
        }

        void OnInit(Init const &e)
        {
            EventQueue::GetInstance()->Dispatch(new Quit);
        }
    };

} // namespace KGE
