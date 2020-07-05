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
            Bind(this, &EntityManager::OnInit);
        }

        void OnInit(Init *e)
        {
            // TODO : DO STUFF...
            EventQueue::GetInstance()->Dispatch(new Quit);
        }
    };

} // namespace KGE
