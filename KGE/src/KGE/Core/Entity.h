#pragma once
#include <headers.h>

namespace KGE
{
    class Entity
    {
    public:
        Entity();
        virtual ~Entity(){};

        friend bool operator==(Entity const &, Entity const &);

    private:
        std::string m_Name;
        int m_ID;
        static int s_NumInstances;
    };

} // namespace KGE