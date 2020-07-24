#pragma once
#include "Component.h"
#include "KGE/Events/Events.h"

namespace KGE
{

	// Component Category
#define CC(type_) const ComponentCategory GetCategory() const override { return ComponentCategory::type_; }

	struct Behaviour : public EventListener, public Component
	{
	public:
		virtual void OnUpdate(double ts) {};

		~Behaviour()
		{
			//K_CORE_ERROR("Deleting A Behaviour");
		}

		friend struct ScriptComponent;
		CC(Behaviour);
	};

	// Allow usage of both 'Behaviour & Behavior'
	typedef Behaviour Behavior;

	/*
	* A Script can have multiple behaviours attached
	*/
	struct ScriptComponent : public Component
	{
	public:
		/*ScriptComponent(Behaviour bh)
		{
			behaviours.push_back(Ref<Behavior>(&bh));
		};*/

		ScriptComponent() = default;


		void Init() {
			// Init Behaviours
			/*for (auto& b : behaviours) {
				b->Init();
			}*/

			for (auto& p : m_behaviourMap) {
				auto& b = p.second;
				b->Init();
			}
		}


		Ref<Behavior> Get(const std::string& type) {
			return  (m_behaviourMap.find(type) != m_behaviourMap.end()) ?  
				m_behaviourMap[type] : nullptr;
		}

		const bool Has(const std::string& type) const {
			return m_behaviourMap.find(type) != m_behaviourMap.end();
		}
		

		void OnEvent(Event& e) {
			/*for (auto& b : behaviours) {
				b->OnEvent(e);
			}*/

			for (auto& p : m_behaviourMap) {
				auto& b = p.second;
				b->OnEvent(e);
			}
		}

		void Add(Behaviour& bh)
		{
			//m_behaviourMap
			//behaviours.push_back(Ref<Behavior>(&bh));

			// Add behaviour
			m_behaviourMap[bh.GetType()] = Ref<Behavior>(&bh);
		};

		void OnUpdate(double ts) {
			/*for (auto& b : behaviours) {
				b->OnUpdate(ts);
			}*/

			for (auto& p : m_behaviourMap) {
				auto& b = p.second;
				b->OnUpdate(ts);
			}
		}

		~ScriptComponent()
		{
			//behaviours.clear();
			m_behaviourMap.clear();
			//K_CORE_ERROR("Deleting Script Component");
		}

		CC(Script);
		CLASS_TYPE(ScriptComponent);

	public:
		//std::vector<Ref<Behaviour>> behaviours;
		std::unordered_map<std::string, Ref<Behaviour>> m_behaviourMap;
	};

	// TODO Change this to use glm instead
	struct TransformComponent : public Component
	{
		struct Vec2
		{
			double x, y;
		};


		TransformComponent(Vec2 pos = { 0, 0 }, Vec2 scale = { 1, 1 }, float angle = 0)
			: pos(pos), scale(scale), angle(angle) {}

		Vec2 pos;
		Vec2 scale;
		float angle;

		CC(Transform);

		~TransformComponent()
		{
			//K_CORE_ERROR("Deleting Transform Component");
		}

		CLASS_TYPE(TransformComponent);
	};
} // namespace KGE