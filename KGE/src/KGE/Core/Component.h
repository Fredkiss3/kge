//
// Created by Fredkiss3 on 03/07/2020.
//

#pragma once
#include "KGE/Base.h"
#include "headers.h"

namespace KGE {
    enum class ComponentCategory {
        Transform = 1,
        Behaviour = 2,
    };
    
    class Entity;

    struct Component {
    public:
        /*
        * Called when the component is attached to the entity
        */
        virtual void Init() {};

        /*
        * Get the category of the component
        */
        const virtual ComponentCategory GetCategory() const = 0;

        Entity* entity = nullptr;

        /*
        * Return a pointer to the Component if found, otherwise it returns a nullptr
        */
        Ref<Component> GetComponent(const char* type);
        Ref<Component> GetComponent(ComponentCategory category);

        /*
        * For Usage in C++ only
        */
        template<ComponentCategory category>
        Ref<Component> GetComponent() {
            return GetComponent(category);
        }
       
        /*
        * For Usage in C++ only 
        */
        template<typename T>
        T& GetComponent() {
            return castRef<T>(GetComponent(T::GetStaticType));
        }

        //template<typename T>
        //T& cast() {
        //    auto ref = Ref<Component>(this);
        //    return castRef<T>(ref);
        //}

       

        bool active = true;

        /*
        * Get real type
        */
        virtual std::string GetTypeName() { return type(*this); }
        
        static std::string GetStaticTypeName() { return type<Component>(); }

        static const char* GetStaticType() { return "Component"; }
        virtual const char* GetType() const { return GetStaticType(); }

        virtual ~Component();
    };
}
