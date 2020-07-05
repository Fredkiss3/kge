#pragma once

#include <headers.h>
#include <KGE/Core/Entity.h>
#include <KGE/Core/Log.h>

namespace KGE {
    class Engine;

    class Scene {
    public:
        virtual void setUp() = 0;

        void add(Entity const &e);

        void remove(Entity const &e);

        std::string GetName() { return m_Name; }

        Scene();

        virtual ~Scene() {
            K_CORE_INFO("Deleting {}", GetName());
        };

        // Allow full control of scene in Engine
        friend class Engine;

    private:
        std::string m_Name;
        std::vector<Entity> m_Entities;
        static int s_NumInstances;
    };

} // namespace KGE