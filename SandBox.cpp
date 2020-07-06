#include <KGE.h>

using namespace KGE;

// class MyScene : public Scene
// {
// public:
//     void setUp() override
//     {
//         K_TRACE("This is my name : {}", GetName());
//     }
// };

/**
 * class Player: Entity {
 *      public:
 *      void OnUpdate(UpdateEvent& e, std::function& _) {
 *          MyScene scene2;
 *          Scene::load(scene2);
 *      }
 * }
 * */
int main()
{
    // Code for starting our app
    KGE::Logger::Init();
    KGE::Logger::SetLogLevel(LogLevel::TRACE);

    KGE::Engine::Run();
    //delete e;

    return 0;
}