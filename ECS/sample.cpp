// #pragma once
#include <string>
#include <iostream>
#include <typeinfo>

#ifdef __GNUG__
#include <cstdlib>
#include <memory>
#include <cxxabi.h>

std::string demangle(const char *name)
{

	int status = -4; // some arbitrary value to eliminate the compiler warning

	// enable c++11 by passing the flag -std=c++11 to g++
	std::unique_ptr<char, void (*)(void *)> res{
		abi::__cxa_demangle(name, NULL, NULL, &status),
		std::free};

	return (status == 0) ? res.get() : name;
}
#else

// does nothing if not g++
std::string demangle(const char *name)
{
	return name;
}
#endif

template <class T>
std::string type(const T &t)
{
	return demangle(typeid(t).name());
}

template <class T>
std::string type()
{
	return demangle(typeid(T).name());
}

#define TYPE_NAME \
	virtual std::string GetTypeName() { return type(*this); }

#define CLASS_TYPE(type)                                 \
	static const char *GetStaticType() { return #type; } \
	virtual const char *GetType() const override { return GetStaticType(); }

#include <iostream>
#include <bitset>
#include <string>
#include <memory>
#include <unordered_map>
#include <functional>
#include <chrono>
#include <array>

template <typename T>
using Ref = std::shared_ptr<T>;

void print();
void print(bool val);

template <typename First, typename... Args>
void print(First const &arg, Args const &... rest);

/***************************************************************/
typedef std::bitset<100> Signature;

enum class CType
{
	Position,
	Velocity,
	Behaviour,
};

std::ostream &operator<<(std::ostream &os, const CType &type)
{
	switch (type)
	{
	case CType::Position:
		os << "Position";
		break;
	case CType::Velocity:
		os << "Velocity";
		break;
	case CType::Behaviour:
		os << "Behaviour";
		break;
	default:
		break;
	}
	return os;
}

class Scene;
typedef std::unordered_map<std::string, int> SignatureIndexMap;
class Hasher
{
public:
	static Signature computeSignature(const CType &type, Signature &sign, bool value = true)
	{
		sign[(int)type] = value;
		return sign;
	}

	static Signature computeSignature(const std::string &type, Signature &sign, bool value = true)
	{

		if (s_SignatureCache.find(type) != s_SignatureCache.end())
		{
			sign[s_SignatureCache[type]] = value;
		}
		else
		{
			sign[s_LastIndex] = value;
			s_SignatureCache[type] = s_LastIndex;
			++s_LastIndex;
		}

		return sign;
	}

	static SignatureIndexMap GetSignatureCache()
	{
		return s_SignatureCache;
	}

	static Signature getSignature(const CType &type)
	{
		Signature sign;
		sign[(int)type] = true;
		return sign;
	}

	static Signature getSignature(const std::string &type)
	{
		Signature sign;
		if (s_SignatureCache.find(type) != s_SignatureCache.end())
		{
			sign[s_SignatureCache[type]] = true;
		}
		else
		{
			sign[s_LastIndex] = true;
			s_SignatureCache[type] = s_LastIndex;
			++s_LastIndex;
		}

		return sign;
	}

private:
	static SignatureIndexMap s_SignatureCache;
	static int s_LastIndex;
};

int Hasher::s_LastIndex{0};
SignatureIndexMap Hasher::s_SignatureCache;

struct Component
{
	virtual CType GetCategory() = 0;

	static const char *GetStaticType() { return "Component"; }
	virtual const char *GetType() const { return GetStaticType(); }
};

class Entity
{
	typedef std::vector<Ref<Component>> ComponentList;

public:
	Entity(const std::string &name) : m_Name(name), m_ID(0), m_Alive(true), m_Active(true), scene(nullptr) {}

	void addComponent(Component *c)
	{
		Ref<Component> ref(c);
		m_CategorySignature = Hasher::computeSignature(c->GetCategory(), m_CategorySignature);
		m_ComponentSignature = Hasher::computeSignature(c->GetType(), m_ComponentSignature);

		// add component to components
		const auto &bit1 = Hasher::getSignature(c->GetType());
		const auto &bit2 = Hasher::getSignature(c->GetCategory());
		m_ComponentTypesMap[bit1].push_back(ref);
		m_CategoryComponentMap[bit2].push_back(ref);
	}

	//void DumpComponents() {
	//	print("Entity ", GetName(), " has : \n");
	//	print("For Categories : ");
	//	for (auto& pair : m_CategoryComponentMap) {
	//		for (auto& el : pair.second) {
	//			print("Component category => ", el->GetCategory());
	//		}
	//	}
	//
	//	print("\nFor Component Types : ");
	//	for (auto& pair : m_ComponentTypesMap) {
	//		for (auto& el : pair.second) {
	//			print("Component type => ", el->GetType());
	//		}
	//	}
	//}

	const bool hasComponent(const CType &category) const
	{
		//print("trying to see if entity ", GetName(), " has component ", category );
		const auto &bit2 = Hasher::getSignature(category);
		auto &bit1 = m_CategorySignature;
		bool has = (bit1 & bit2) == bit2;
		//print((has ? "Yes it has" : "Not it hasn't\n"));
		return (bit1 & bit2) == bit2;
	}

	template <CType c1, CType... Args>
	const bool hasComponent() const
	{
		return hasComponent(c1) && hasComponent(Args...);
	}

	const bool hasComponent(const std::string &type) const
	{
		const auto &bit2 = Hasher::getSignature(type);
		auto &bit1 = m_ComponentSignature;
		return (bit1 & bit2) == bit2;
	}

	Ref<Component> getComponent(const std::string &type)
	{
		Ref<Component> ref = nullptr;

		if (hasComponent(type))
		{
			// Get type signature
			auto &cMap = m_ComponentTypesMap;
			const auto &sign = Hasher::getSignature(type);

			// if signature has been found then get the first component of this type
			const auto &it = cMap.find(sign);
			if (it != cMap.end())
			{
				auto &cList = it->second;
				if (cList.size() > 0)
				{
					ref = cList[0];
				}
			}
		}
		return ref;
	}

	ComponentList getComponents(const std::string &type)
	{
		ComponentList ref;

		if (hasComponent(type))
		{
			// Get type signature
			auto &cMap = m_ComponentTypesMap;
			const auto &sign = Hasher::getSignature(type);

			// if signature has been found then get the first component of this type
			const auto &it = cMap.find(sign);
			if (it != cMap.end())
			{
				auto &cList = it->second;
				if (cList.size() > 0)
				{
					ref = cList;
				}
			}
		}
		return ref;
	}

	template <CType category>
	Ref<Component> getComponent()
	{
		return getComponent(category);
	}

	Ref<Component> getComponent(CType category)
	{
		Ref<Component> ref = nullptr;
		if (hasComponent(category))
		{
			auto &cMap = m_CategoryComponentMap;
			const auto &sign = Hasher::getSignature(category);

			// if signature has been found then get the first component of this type
			const auto &it = cMap.find(sign);
			if (it != cMap.end())
			{
				auto &cList = it->second;
				if (cList.size() > 0)
				{
					ref = cList[0];
				}
			}
		}

		return ref;
	}

	ComponentList getComponents()
	{
		ComponentList ref;
		return ref;
	}

	ComponentList getComponents(CType category)
	{
		ComponentList ref;

		// if signature has been found then get the first component of this type
		if (hasComponent(category))
		{
			auto &cMap = m_CategoryComponentMap;
			const auto &sign = Hasher::getSignature(category);

			// if signature has been found then get the first component of this type
			const auto &it = cMap.find(sign);
			if (it != cMap.end())
			{
				auto &cList = it->second;
				if (cList.size() > 0)
				{
					ref = cList;
				}
			}
		}

		return ref;
	}

	template <CType category>
	ComponentList getComponents()
	{
		return getComponents(category);
	}

	const bool IsActive() const
	{
		return m_Active;
	}

	const bool IsAlive() const
	{
		return m_ID != 0;
	}

	void SetActive(bool active);
	void destroy();

	bool operator==(Entity const &other) const
	{
		return scene == other.scene && m_ID == other.m_ID;
	}

	friend class Scene;

	const std::string &GetName() const
	{
		return m_Name;
	}

private:
	const bool hasComponent() const
	{
		return true;
	}

private:
	size_t m_ID;
	Scene *scene;
	std::unordered_map<Signature, ComponentList> m_CategoryComponentMap;
	std::unordered_map<Signature, ComponentList> m_ComponentTypesMap;
	bool m_Alive;
	bool m_Active;

	Signature m_ComponentSignature;
	Signature m_CategorySignature;
	std::string m_Name;
};

template <CType... Types>
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

	Entity *get() const;

	Entity *operator*() const
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

template <CType... Types>
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
	typedef std::vector<Entity> EntityList;
	typedef std::function<void(Entity &)> viewFn;

public:
	struct EntityPool
	{
		EntityList activeEntities;
		EntityList currentEntities;
		EntityList deadEntities;
		EntityList inactiveEntities;
	};

	Scene() : m_lastID(0) {}

	void add(Entity &e)
	{
		++m_lastID;
		e.scene = this;
		e.m_ID = m_lastID;

		if (e.IsAlive())
		{
			m_Pool.activeEntities.push_back(e);
		}
		else
		{
			m_Pool.inactiveEntities.push_back(e);
		}
	}

	void remove(Entity &e)
	{
		if (e.IsActive())
		{
			auto &active = m_Pool.activeEntities;
			auto &dead = m_Pool.deadEntities;
			const auto &it = std::find(active.begin(), active.end(), e);

			if (it != active.end())
			{
				dead.push_back(*it);
				active.erase(it);
			}
		}
		else
		{
			auto &inactive = m_Pool.inactiveEntities;
			auto &dead = m_Pool.deadEntities;
			const auto &it = std::find(inactive.begin(), inactive.end(), e);

			if (it != inactive.end())
			{
				dead.push_back(*it);
				inactive.erase(it);
			}
		}

		// Reset ID
		e.m_ID = 0;
	}

	void Disable(const Entity &e)
	{
		if (e.scene != nullptr)
		{
			auto &active = m_Pool.activeEntities;
			auto &inactive = m_Pool.inactiveEntities;
			const auto &it = std::find(active.begin(), active.end(), e);

			if (it != active.end())
			{
				inactive.push_back(*it);
				active.erase(it);
			}
		}
	}

	void Enable(const Entity &e)
	{
		if (e.scene != nullptr)
		{
			auto &active = m_Pool.activeEntities;
			auto &inactive = m_Pool.inactiveEntities;
			const auto &it = std::find(inactive.begin(), inactive.end(), e);

			if (it != inactive.end())
			{
				active.push_back(*it);
				inactive.erase(it);
			}
		}
	}

	template <CType... Types>
	void each(const viewFn &func)
	{
		invalidate();
		for (Entity *ent : each<Types...>())
		{
			func(*ent);
		}
	}

	template <CType... Types>
	EntityComponentView<Types...> each()
	{
		EntityComponentIterator<Types...> first(this, (size_t)0, false);
		EntityComponentIterator<Types...> last(this, getCount(), true);
		return EntityComponentView<Types...>(first, last);
	}

	void all(const viewFn &func)
	{
		invalidate();
		for (auto ent : m_Pool.currentEntities)
		{
			if (ent.IsActive())
				func(ent);
		}
	}

	Entity *getByIndex(size_t index)
	{
		if (index >= getCount())
			return nullptr;

		return &m_Pool.currentEntities[index];
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
};

template <CType... Types>
EntityComponentIterator<Types...>::EntityComponentIterator(Scene *scene, size_t index, bool bIsEnd)
	: bIsEnd(bIsEnd), index(index), m_Scene(scene)
{
	if (index >= scene->getCount())
		this->bIsEnd = true;
}

template <CType... Types>
bool EntityComponentIterator<Types...>::isEnd() const
{
	return bIsEnd || index >= m_Scene->getCount();
}

template <CType... Types>
Entity *EntityComponentIterator<Types...>::get() const
{
	if (isEnd())
		return nullptr;

	return m_Scene->getByIndex(index);
}

template <CType... Types>
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

template <CType... Types>
EntityComponentView<Types...>::EntityComponentView(const EntityComponentIterator<Types...> &first, const EntityComponentIterator<Types...> &last)
	: firstItr(first), lastItr(last)
{
	if (firstItr.get() == nullptr || (!firstItr.get()->IsAlive()) || !firstItr.get()->template hasComponent<Types...>())
	{
		++firstItr;
	}
}

void Entity::SetActive(bool active)
{
	m_Active = active;
	if (scene != nullptr)
	{
		if (active)
		{
			scene->Enable(*this);
		}
		else
		{
			scene->Disable(*this);
		}
	}
}

void Entity::destroy()
{
	if (scene != nullptr)
	{
		scene->remove(*this);
	}
}

template <typename T, typename Y>
T &castRef(Ref<Y> ref)
{
	return dynamic_cast<T &>(*ref);
}

/***************************************************************/

void print()
{
	std::cout << std::endl;
}

void print(bool val)
{
	if (val)
		std::cout << "true";
	else
		std::cout << "false";
	std::cout << " ";
}

template <typename First, typename... Args>
void print(First const &arg, Args const &... rest)
{
	std::cout << arg;
	print(rest...);
}

struct Position : public Component
{
	Position(int x, int y) : x(x), y(y) {}
	int x, y;
	CType GetCategory() override
	{
		return CType::Position;
	}

	CLASS_TYPE(Position);
};

struct Velocity : public Component
{
	CType GetCategory() override
	{
		return CType::Velocity;
	}

	CLASS_TYPE(Velocity);
};

struct Behaviour : public Component
{
	virtual void OnUpdate() = 0;
	CType GetCategory() override
	{
		return CType::Behaviour;
	}

	CLASS_TYPE(Behaviour);
};

class MyBehaviour : public Behaviour
{
public:
	void OnUpdate()
	{
		// DO SOMETHING...
		++i;
	}

	CLASS_TYPE(MyBehaviour);
	int i = 0;
};

class Timer
{
public:
	Timer()
	{
		m_Start = std::chrono::high_resolution_clock::now();
	}

	void Stop()
	{
		auto endT = std::chrono::high_resolution_clock::now();

		auto start = std::chrono::time_point_cast<std::chrono::microseconds>(m_Start).time_since_epoch().count();
		auto end = std::chrono::time_point_cast<std::chrono::microseconds>(endT).time_since_epoch().count();

		auto sec = (end - start) * 1e-6;
		auto ms = (end - start) * 0.001;

		print("Took ", sec, " s ( ", ms, " ms) to run");
	}

	~Timer()
	{
		Stop();
	}

private:
	std::chrono::time_point<std::chrono::system_clock> m_Start;
};

int main()
{

	Scene scene;
	Entity e("player 1");
	Entity e2("player 2");

	e.addComponent(new Position{2, 25});
	e.addComponent(new Position{5, 5});
	e.addComponent(new MyBehaviour());

	e2.addComponent(new Position{0, 0});

	// Adding entities to scene
	scene.add(e);
	scene.add(e2);

	print();

	//e2.addComponent(new Position());
	//e2.addComponent(new Velocity());
	//
	//print();
	//
	//print("Test Entity " , e.GetName());
	//std::cout << "Category Position= " << e.hasComponent(CType::Position) << std::endl;
	//std::cout << "Position type= " << e.hasComponent(Position::GetStaticType()) << std::endl;
	//
	//print();
	//
	////e.DumpComponents();
	//
	//auto c = e.getComponent<CType::Position>();
	//if (c != nullptr)
	//{
	//	auto &p = (Position&)(*c);
	//	print("Position Count : ", c.use_count());
	//	print("Position Found : ", "(x=", p.x, ", y=", p.y, ")");
	//}
	//print();
	//
	//auto& cList = e.getComponents(CType::Position);
	//
	//for (auto c : cList) {
	//	auto& p = (Position&)(*c);
	//	print("Position Got : ", "(x=", p.x, ", y=", p.y, ")");
	//}
	//
	//auto& cache = Hasher::GetSignatureCache();
	//for (auto it = cache.begin(); it != cache.end(); ++it) {
	//	print("Cache[" , it->first , "] = ", it->second);
	//}

	print("Getting all entities in the scene : \n");
	scene.all([&](Entity &e) {
		print(e.GetName());
		e.destroy();
	});

	print();

	print("Getting all entities that have position category in the scene : \n");

	scene.each<CType::Position>([&](Entity &e) {
		const auto &c = e.getComponent<CType::Position>();
		if (c != nullptr)
		{
			auto &p = (Position &)(*c);
			print(e.GetName(), " => (", p.x, ", ", p.y, ")");
		}
	});

	print();

	print("Getting all entities that have position & behaviour in the scene : \n");

	scene.each<CType::Position, CType::Behaviour>([&](Entity &e) {
		const auto &c = e.getComponent<CType::Position>();
		if (c != nullptr)
		{
			auto &p = (Position &)(*c);
			print(e.GetName(), " => (", p.x, ", ", p.y, ")");
		}
	});

	print();

	print("Getting all entities that have velocity in the scene : \n");

	scene.each<CType::Velocity>([&](Entity &e) {
		const auto &c = e.getComponent<CType::Velocity>();
		/*if (c != nullptr)
		{
			auto& p = (Position&)(*c);
			print(e.GetName(), " => (", p.x, ", ", p.y, ")");
		}*/
	});

	{
		Timer timer;
		//print(sizeof(Entity));
		for (int i = 0; i < 1000; i++)
		{
			Entity e("player 3");
			//	//Element* e = new Element;
			//	// add 5 behaviours
			e.addComponent(new MyBehaviour());
			e.addComponent(new MyBehaviour());
			e.addComponent(new MyBehaviour());
			e.addComponent(new MyBehaviour());
			e.addComponent(new MyBehaviour());

			// Adding entities to scene
			scene.add(e);
		}
	}

	print();

	print("Getting all entities that have behaviour in the scene : \n");

	int i(0);
	int bh(0);
	{
		Timer timer;
		scene.each<CType::Behaviour>([&](Entity &e) {
			auto c = e.getComponents(MyBehaviour::GetStaticType());
			for (auto b : c)
			{
				castRef<Behaviour>(b).OnUpdate();
				++bh;
			}
			++i;
		});
	}

	print("Found ", i, " Entities");
	print("Found ", bh, " Behaviours");

	return 0;
}