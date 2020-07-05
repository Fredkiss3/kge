//
// Created by Fredkiss3 on 04/07/2020.
//

#pragma once
#include "headers.h"

namespace KGE {

    /**
     * Random Generator
     */
    class K_Random {
    public:
        template<typename T>
        static void Choice(std::vector<T> &);
        template<typename T>
        static void Range(T, T);
    };

    template<typename T>
    void K_Random::Choice(std::vector<T> &v) {
        // TODO
    }

    template<typename T>
    void K_Random::Range(T begin, T end) {
        // TODO
    }

}
