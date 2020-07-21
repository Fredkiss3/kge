#include <functional>
#include <iostream>
#include <string>

struct Entity
{
    std::string name;
};

typedef std::function<int(Entity &)> viewFn;

Entity &caller(const viewFn &fn)
{
    Entity e{"A certain Entity"};
    fn(e);

    return e;
}

int main()
{
    auto &val = caller([&](Entity &e) {
        std::cout << e.name << std::endl;
        return 0;
    });

    return 0;
}