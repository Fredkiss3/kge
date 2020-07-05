#include <KGE.h>

using namespace KGE;

class MyScene : public Scene
{
public:
    void setUp() override
    {
        K_TRACE("This is my name : {}", GetName());
    }
};

struct Update : public Event
{
    std::string GetTypeName() const override
    {
        return "Update";
    }

    std::string GetData() const override
    {
        return "delaTime=" + std::to_string(deltaTime);
    }

    double deltaTime = 1.0f / 60.0f;
};

/**
 * class Handler : public EventListener
{
public:
    std::string GetTypeName() const override
    {
        return "Custom Handler";
    }

    void handle(Event *e) override
    {
        e->handled = true;
        K_INFO("Event Data {}", e->Print());
    }
};

 * /
/*
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