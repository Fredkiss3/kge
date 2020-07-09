#include <headers.h>
#include "Entity.h"

namespace KGE
{

    int Entity::s_NumInstances = 0;
    Entity::Entity() : m_ID(0)
    {
        ++s_NumInstances;
        m_ID = s_NumInstances;
    }

    bool operator==(Entity const &e1, Entity const &e2)
    {
        return e1.m_ID == e2.m_ID;
    }
} // namespace KGE