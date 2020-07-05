//
// Created by Fredkiss3 on 04/07/2020.
//
#pragma once
#include "headers.h"

namespace KGE {

    struct Task {
        // TODO

    public:
        void call() {
            // TODO : Execute function
        }
    };

    class K_Timer {
    public:
        static void Schedule(Task task);
        static void ScheduleInterval(Task task, double interval);
//        static std::vector<Task>& GetScheduledTasks(double time);
    private:
//        static std::unordered_map<double, std::vector<Task>> s_ScheduledTasks;
    };

}
