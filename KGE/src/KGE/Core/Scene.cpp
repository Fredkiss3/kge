#include <headers.h>
#include "Scene.h"

namespace KGE {
    int Scene::s_NumInstances = 0;

    Scene::Scene() : m_Entities(0), m_Name("New Scene") {
        ++s_NumInstances;
        m_Name += " " + std::to_string(s_NumInstances);
    }

    void Scene::add(Entity const &e) {
        m_Entities.push_back(e);
    }

    void Scene::remove(Entity const &e) {
        for (unsigned int i(0); i < m_Entities.size(); ++i) {
            if (m_Entities[i] == e) {
                m_Entities.erase(m_Entities.begin() + i);
                break;
            }
        }
    }
} // namespace KGE