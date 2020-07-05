//
// Created by Fredkiss3 on 04/07/2020.
//

#pragma once

namespace KGE
{

    class K_Allocator
    {
    public:
        template <typename T>
        static void *allocate()
        {
            int size = sizeof(T);
        }
    };
} // namespace KGE
