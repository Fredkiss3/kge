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

        EVENT_CLASS_TYPE(Update);
    };

    struct Init : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        EVENT_CLASS_TYPE(Init);
    };

    struct Quit : public Event
    {
        std::string GetData() const override
        {
            return "";
        }

        EVENT_CLASS_TYPE(Quit);
    };

    struct Dummy : public Event
    {
        Dummy(int data) : data(data) {}

        int data;

        std::string GetData() const override
        {
            return "data=" + std::to_string(data);
        }

        EVENT_CLASS_TYPE(Quit);
    };

} // namespace KGE