#pragma once

#include <headers.h>
#include <KGE/Core/Entity.h>
#include <KGE/Utils/Log.h>
#include <KGE/Events/Events.h>

namespace KGE
{
class Engine;

struct EntityData
{
	virtual std::vector<Component *> GetComponents() const = 0;
};

template <ComponentCategory... Types>
class EntityComponentIterator
{
public:
	EntityComponentIterator(Scene *scene, size_t index, bool bIsEnd);

	size_t getIndex() const
	{
		return index;
	}

	bool isEnd() const;

	Scene *getScene() const
	{
		return m_Scene;
	}

	Ref<Entity> get() const;

	Ref<Entity> operator*() const
	{
		return get();
	}

	bool operator==(const EntityComponentIterator<Types...> &other) const
	{
		if (m_Scene != other.m_Scene)
			return false;

		if (isEnd())
			return other.isEnd();

		return index == other.index;
	}

	bool operator!=(const EntityComponentIterator<Types...> &other) const
	{
		if (m_Scene != other.m_Scene)
			return true;

		if (isEnd())
			return !other.isEnd();

		return index != other.index;
	}

	EntityComponentIterator<Types...> &operator++();

private:
	bool bIsEnd = false;
	size_t index;
	Scene *m_Scene;
};

template <ComponentCategory... Types>
class EntityComponentView
{
public:
	EntityComponentView(const EntityComponentIterator<Types...> &first, const EntityComponentIterator<Types...> &last);

	const EntityComponentIterator<Types...> &begin() const
	{
		return firstItr;
	}

	const EntityComponentIterator<Types...> &end() const
	{
		return lastItr;
	}

private:
	EntityComponentIterator<Types...> firstItr;
	EntityComponentIterator<Types...> lastItr;
};

class Scene
{
	typedef std::vector<Ref<Entity>> EntityList;
	typedef std::function<void(Entity &)> viewFn;
	typedef std::function<void(Scene *)> SetupFn;

public:
	struct EntityPool
	{
		EntityList activeEntities;
		EntityList currentEntities;
		EntityList deadEntities;
		EntityList inactiveEntities;
	};

public:
	Scene(const SetupFn &fn, const std::string &name = "new Scene") : m_SetupFn(fn), m_Name(name), m_lastID(0) {}
	~Scene();

	void setUp()
	{
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
	static void Load(const char *name);
	static void Pop();

public:
	void add(Entity &e);
	void add(Entity &e, EntityData *data);

	void remove(Entity &e);

	void Disable(Entity &e);

	void Enable(Entity &e);

	template <ComponentCategory... Types>
	void each(const viewFn &func)
	{
		invalidate();
		for (auto ent : each<Types...>())
		{
			if (ent)
				func(*ent);
		}
	}

	template <ComponentCategory... Types>
	EntityComponentView<Types...> each()
	{
		EntityComponentIterator<Types...> first(this, 0, false);
		EntityComponentIterator<Types...> last(this, getCount(), true);
		return EntityComponentView<Types...>(first, last);
	}

	void all(const viewFn &func)
	{
		invalidate();
		for (auto ent : m_Pool.currentEntities)
		{
			if (ent->IsActive())
				func(*ent);
		}
	}

	Ref<Entity> getByIndex(size_t index)
	{
		if (index >= getCount())
			return nullptr;

		return m_Pool.currentEntities[index];
	}

	const size_t getCount() const
	{
		return m_Pool.currentEntities.size();
	}

private:
	/*
		* Invalidate the current list of entitites
		*/
	void invalidate()
	{
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
EntityComponentIterator<Types...>::EntityComponentIterator(Scene *scene, size_t index, bool bIsEnd)
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
Ref<Entity> EntityComponentIterator<Types...>::get() const
{
	if (isEnd())
		return nullptr;

	return m_Scene->getByIndex(index);
}

template <ComponentCategory... Types>
EntityComponentIterator<Types...> &EntityComponentIterator<Types...>::operator++()
{
	++index;
	while (
		index < m_Scene->getCount() &&
		(get() == nullptr || !get()->template hasComponent<Types...>() || !get()->IsAlive() || !get()->IsActive()))
	{
		++index;
	}

	if (index >= m_Scene->getCount())
		bIsEnd = true;

	return *this;
}

template <ComponentCategory... Types>
EntityComponentView<Types...>::EntityComponentView(const EntityComponentIterator<Types...> &first, const EntityComponentIterator<Types...> &last)
	: firstItr(first), lastItr(last)
{
	if (firstItr.get() == nullptr || (!firstItr.get()->IsAlive()) || !firstItr.get()->template hasComponent<Types...>())
	{
		++firstItr;
	}
}

} // namespace KGE