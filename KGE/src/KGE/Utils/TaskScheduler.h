#pragma once
#include "headers.h"

namespace KGE {

    struct Task {
        // A function that takes the time elapsed since the last call as an argument
        typedef void(*TaskFn)(double);

        TaskFn fn;
        int id = 0;
        bool active = true;

        bool operator=(Task& another) {
            return id == another.id;
        }
    };
    
    class TaskScheduler {
        typedef std::unordered_map<double, std::vector<Tasks>> TaskMap;
        typedef std::chrono::high_resolution_clock Clock;
        public:
            static void Attach(const Task& task, int interval, bool loop = false) 
            {
                // TODO
            }

            static void Detach(const Task& task) 
            {
                // TODO
            }
            
            static void Update(double ts) 
            {
                // TODO
            }
        
        private:
            static TaskMap s_Tasklist;
            static int s_lastID;
    };

    // init last ID
    int TaskScheduler::s_lastID = 0;
}