#pragma once

#include <headers.h>
#include <KGE/Core/Entity.h>
#include <KGE/Utils/Log.h>
#include <KGE/Events/Events.h>

namespace KGE {
	class Engine;

	struct EntityData {
		virtual std::vector<Component*> GetComponents() const = 0;
	};

	template<ComponentCategory... Types>
	class EntityComponentIterator
	{
	public:
		EntityComponentIterator(Scene* scene, size_t index, bool bIsEnd);

		size_t getIndex() const
		{
			return index;
		}

		bool isEnd() const;

		Scene* getScene() const
		{
			return m_Scene;
		}

		Entity* get() const;

		Entity* operator*() const
		{
			return get();
		}

		bool operator==(const EntityComponentIterator<Types...>& other) const
		{
			if (m_Scene != other.m_Scene)
				return false;

			if (isEnd())
				return other.isEnd();

			return index == other.index;
		}

		bool operator!=(const EntityComponentIterator<Types...>& other) const
		{
			if (m_Scene != other.m_Scene)
				return true;

			if (isEnd())
				return !other.isEnd();

			return index != other.index;
		}

		EntityComponentIterator<Types...>& operator++();

	private:
		bool bIsEnd = false;
		size_t index;
		Scene* m_Scene;
	};

	template<ComponentCategory... Types>
	class EntityComponentView
	{
	public:
		EntityComponentView(const EntityComponentIterator<Types...>& first, const EntityComponentIterator<Types...>& last);

		const EntityComponentIterator<Types...>& begin() const
		{
			return firstItr;
		}

		const EntityComponentIterator<Types...>& end() const
		{
			return lastItr;
		}

	private:
		EntityComponentIterator<Types...> firstItr;
		EntityComponentIterator<Types...> lastItr;
	};

	class Scene {
		typedef std::vector<Entity> EntityList;
		typedef std::common_type<std::function<void(Entity&)>>::type viewFn;
		typedef void(*SetupFn)(Scene*);
	public:
		struct EntityPool {
			EntityList activeEntities;
			EntityList currentEntities;
			EntityList deadEntities;
			EntityList inactiveEntities;
		};

	public:
		Scene(SetupFn fn, const std::string& name = "new Scene") : m_SetupFn(fn), m_Name(name), m_lastID(0)  {}
		~Scene();

		void setUp() {
			K_CORE_ASSERT(!m_Started, "Should stop the scene before starting a new scene !");

			// TODO should dispatch events
			EventQueue::Dispatch(new StartScene, true);
			m_SetupFn(this);
			m_Started = true;
		};

		void tearDown()
		{
			K_CORE_ASSERT(m_Started, "Should start the scene before tearing it down !");

			// TODO should dispatch events
			EventQueue::Dispatch(new StopScene, true);
			//K_CORE_TRACE("Tearing Down '{}'", GetName());
			m_Started = false;
		};

		std::string GetName() { return m_Name; }

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
	public:
		void add(Entity& e);
		void add(Entity& e, EntityData* data);

		void remove(Entity& e)
		{
			if (e.IsActive())
			{
				auto& active = m_Pool.activeEntities;
				auto& dead = m_Pool.deadEntities;
				auto& it = std::find(active.begin(), active.end(), e);

				if (it != active.end())
				{
					dead.push_back(*it);
					active.erase(it);
				}
			}
			else
			{
				auto& inactive = m_Pool.inactiveEntities;
				auto& dead = m_Pool.deadEntities;
				auto& it = std::find(inactive.begin(), inactive.end(), e);

				if (it != inactive.end())
				{
					dead.push_back(*it);
					inactive.erase(it);
				}
			}

			// Reset ID
			e.m_ID = 0;
		}

		void Disable(Entity& e)
		{
			if (e.scene != nullptr) {
				auto& active = m_Pool.activeEntities;
				auto& inactive = m_Pool.inactiveEntities;
				auto& it = std::find(active.begin(), active.end(), e);

				if (it != active.end()) {
					inactive.push_back(*it);
					active.erase(it);
				}
			}
		}

		void Enable(Entity& e)
		{
			if (e.scene != nullptr) {
				auto& active = m_Pool.activeEntities;
				auto& inactive = m_Pool.inactiveEntities;
				auto& it = std::find(inactive.begin(), inactive.end(), e);

				if (it != inactive.end()) {
					active.push_back(*it);
					inactive.erase(it);
				}
			}
		}

		template <ComponentCategory... Types>
		void each(viewFn func)
		{
			invalidate();
			for (Entity* ent : each<Types...>())
			{
				if(ent) func(*ent);
			}
		}

		template <ComponentCategory... Types>
		EntityComponentView<Types...> each()
		{
			EntityComponentIterator<Types...> first(this, 0, false);
			EntityComponentIterator<Types...> last(this, getCount(), true);
			return EntityComponentView<Types...>(first, last);
		}



		void all(viewFn func)
		{
			invalidate();
			for (auto ent : m_Pool.currentEntities)
			{
				if (ent.IsActive()) func(ent);
			}
		}

		Entity* getByIndex(size_t index)
		{
			if (index >= getCount())
				return nullptr;

			return &m_Pool.currentEntities[index];
		}


		const size_t getCount() const {
			return m_Pool.currentEntities.size();
		}
	private:
		/*
		* Invalidate the current list of entitites
		*/
		void invalidate() {
			m_Pool.currentEntities = m_Pool.activeEntities;
		}
	private:
		EntityPool m_Pool;
		size_t m_lastID;

		std::string m_Name = "new Scene";
		bool m_Started = false;
		SetupFn m_SetupFn;
	};



	template <ComponentCategory... Types>
	EntityComponentIterator<Types...>::EntityComponentIterator(Scene* scene, size_t index, bool bIsEnd)
		: bIsEnd(bIsEnd), index(index), m_Scene(scene)
	{
		if (index >= scene->getCount())
			this->bIsEnd = true;
	}

	template <ComponentCategory... Types>
	bool EntityComponentIterator<Types...>::isEnd() const
	{
		return bIsEnd || index >= m_Scene->getCount();
	}

	template <ComponentCategory... Types>
	Entity* EntityComponentIterator<Types...>::get() const
	{
		if (isEnd())
			return nullptr;

		return m_Scene->getByIndex(index);
	}

	template <ComponentCategory... Types>
	EntityComponentIterator<Types...>& EntityComponentIterator<Types...>::operator++()
	{
		++index;
		while (
			index < m_Scene->getCount() &&
			(
				get() == nullptr
				|| !get()->template hasComponent<Types...>()
				|| !get()->IsAlive()
				|| !get()->IsActive()
				)
			)
		{
			++index;
		}

		if (index >= m_Scene->getCount())
			bIsEnd = true;

		return *this;
	}

	template <ComponentCategory... Types>
	EntityComponentView<Types...>::EntityComponentView(const EntityComponentIterator<Types...>& first, const EntityComponentIterator<Types...>& last)
		: firstItr(first), lastItr(last)
	{
		if (firstItr.get() == nullptr || (!firstItr.get()->IsAlive()) || !firstItr.get()->template hasComponent<Types...>())
		{
			++firstItr;
		}
	}

} // namespace KGE