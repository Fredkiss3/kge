#pragma once
#include "headers.h"
#include "KGE/Core/Entity.h"
#include "KGE/Events/Events.h"
#include "KGE/Core/Components.h"
#include "KGE/Base.h"
#include "KGE/Utils/Color.h"

#include <entt/entt.hpp>

namespace KGE
{
	class Engine;
	//class Entity;

	struct EntityData
	{
	public:
		EntityData(const std::string& tag, TransformComponent xf = Vec2{0.0}) : xf(xf), Tag(tag) {}
		EntityData() : xf({0.0}), Tag("Empty Entity") {}


		virtual Behaviour* GetScript() const {
			return nullptr;
		}

		virtual const std::vector<Component*> GetComponents() const
		{
			return {};
		}

	protected:
		std::string Tag;
		TransformComponent xf;

		friend class Entity;
		friend class Scene;
	};

	class Scene
	{
		typedef std::function<void(Scene*)> SetupFn;

	public:
		Scene(const SetupFn& fn, const std::string& name = "new Scene");
		~Scene();

		void setUp();

		void tearDown()
		{
			K_CORE_ASSERT(m_Started, "Should start the scene before tearing it down !");
			K_CORE_TRACE("Tearing Down '{}'", GetName());

			// TODO should dispatch events
			EventQueue::Dispatch(new StopScene, true);
			m_Started = false;
		};

		std::string GetName() { return m_Name; }
		
		Entity& Create(const EntityData& data);
		Entity& Create();
		
		template<typename T, typename... Args>
		Entity& CreatePrefab(Args&&... args) {
			return Create(T(std::forward<Args>(args)...));
		}
		//Entity& Create(EntityData&& data);

		void Destroy(Entity& e);

		void Disable(Entity& e);

		void Enable(Entity& e);

		entt::registry& Reg() { return m_Registry; }

		// Retrieve entity from ID
		Entity* Get(entt::entity id) {
			if (m_EntityMap.find(id) != m_EntityMap.end()) {
				return &m_EntityMap[id];
			}
			return nullptr;
		}
		
		// Get Main Camera 
		Entity& GetMainCamera() {
			return m_MainCamera;
		}

	public:
		// STATIC METHODS
		static void Pause()
		{
			EventQueue::Dispatch(new PauseScene, true);
		};

		static void Continue()
		{
			EventQueue::Dispatch(new ContinueScene, true);
		};

		// Allow full control of scene in Engine
		friend class Engine;

		// Start a new scene
		static void Load(int index);
		static void Load(const char* name);
		static void Pop();

		// The scene Background color
		Color bgColor = { 0.22f, 0.22f, 0.22f, 1.0f };
	public: 
		const std::unordered_map <entt::entity, Entity>& all() {
			return m_EntityMap;
		}

	private:
		std::string m_Name = "new Scene";
		bool m_Started = false;
		SetupFn m_SetupFn;
		entt::registry m_Registry;

		std::unordered_map <entt::entity, Entity> m_EntityMap;

		Entity m_MainCamera;
	private:
		void AddComponents(const std::vector<Component*>& cps, Entity& e);
	};
} // namespace KGE