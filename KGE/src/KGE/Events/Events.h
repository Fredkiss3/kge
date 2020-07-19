//
// Created by Fredkiss3 on 04/07/2020.
//
#pragma once

#include "headers.h"
#include "Event.h"

namespace KGE
{
    struct Update : public Event
    {
        explicit Update(double d) : deltaTime(d) {}

        double deltaTime;

        std::string GetData() const override
        {
            return "deltaTime=" + std::to_string(deltaTime);
        }

        CLASS_TYPE(Update);
    };

    struct Init : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        CLASS_TYPE(Init);
    };
    
    struct EnableEntity : public Event
    {
        EnableEntity(Entity& e)  
        {
            entity = Ref<Entity>(&e);
        }

        std::string GetData() const override
        {
            return "entity=" + entity->GetName();
        }

        CLASS_TYPE(EnableEntity);
    };

    struct DisableEntity : public Event
    {
        DisableEntity(Entity& e)
        {
            entity = Ref<Entity>(&e);
        }

        std::string GetData() const override
        {
            return "entity=" + entity->GetName();
        }

        CLASS_TYPE(DisableEntity);
    };
    
    struct DestroyEntity : public Event
    {
        DestroyEntity(Entity& e)
        {
            entity = Ref<Entity>(&e);
        }

        std::string GetData() const override
        {
            return "entity=" + entity->GetName();
        }

        CLASS_TYPE(DestroyEntity);
    };

    struct Quit : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        CLASS_TYPE(Quit);
    };

    struct StartScene : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        CLASS_TYPE(StartScene);
    };

    struct StopScene : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        CLASS_TYPE(StopScene);
    };

    struct PauseScene : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        CLASS_TYPE(PauseScene);
    };

    struct ContinueScene : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        CLASS_TYPE(ContinueScene);
    };

} // namespace KGE