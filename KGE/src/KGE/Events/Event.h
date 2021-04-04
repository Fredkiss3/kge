#pragma once

#include "headers.h"
#include "KGE/Base.h"

namespace KGE
{
	class Scene;
	class Entity;

	/*
	* We use struct here because we Want to have a default initializer
	* and all attributes should be public
	* */
	struct Event
	{
		virtual const std::string GetData() const
		{
			return "";
		};

		const std::string Print() const;
		virtual ~Event() = default;

		Ref<Scene> scene = nullptr;
		Ref<Entity> entity = nullptr;

		bool handled = false;

		virtual const char* GetType() const
		{
			return "Event";
		};

		static const char* GetStaticType() { return "Event"; }

		// to give full control to the queue only
		friend class EventQueue;

	protected:
		/*
			 * This will be used to get the type of the element
			 * It will be used primarly When logging the call to an event
			 * */
		virtual const std::string& GetTypeName() const
		{
			return type(*this);
		};
	};

	class EventQueue
	{
	public:
		/*
			 * Post an event onto the event queue
			 * */
		void DispatchEvent(Event* e, bool immediate = false)
		{
			//K_CORE_DEBUG("Adding Event : {} to the queue", e->Print());

			// Casting the raw pointer to a shared_ptr
			Ref<Event> ev(e);
			if (immediate)
			{
				m_EventList.push_front(ev);
			}
			else
			{
				m_NextEventList.push_back(ev);
			}
		}

		static void Dispatch(Event* e, bool immediate = false)
		{
			GetInstance();
			s_Instance->DispatchEvent(e, immediate);
		}

		/**
			 * Swap & get the next event to process
			 * @return the next event to process
			 */
		Ref<Event> GetNextEvent()
		{
			Ref<Event> e = nullptr;
			if (m_EventList.size() > 0)
			{
				// Pick event
				e = m_EventList.front();
				// go to next event
				//m_EventList.pop();
				m_EventList.pop_front();
			}

			return e;
		}

		/*
			 * Swap the next events to the current
			 */
		void SwapEvents()
		{
			//  swap the lists
			m_EventList.swap(m_NextEventList);
		}

		static Ref<EventQueue>& GetInstance()
		{
			if (s_Instance == nullptr)
			{
				s_Instance = Ref<EventQueue>(new EventQueue());
			}

			return s_Instance;
		}

	private:
		std::deque<Ref<Event>> m_EventList;
		std::deque<Ref<Event>> m_NextEventList;
		static Ref<EventQueue> s_Instance;

		EventQueue() : m_EventList(0), m_NextEventList(0) {}

	}; // namespace KGE

	class HandlerBase
	{
	public:
		virtual const std::string GetEventName() const { return m_EventName; }

		// Implemented by EventHandler
		virtual void call(Event& evnt) = 0;

	protected:
		std::string m_EventName;
	};

	template <typename EventType>
	class EventHandler : public HandlerBase
	{
	public:
		typedef std::function<void(EventType&)> EventCallback;

		EventHandler(const EventCallback& callBack) : m_CallBack{ callBack }
		{
			m_EventName = EventType::GetStaticType();
		};

		void call(Event& event) override
		{
			m_CallBack(static_cast<EventType&>(event));
		}
	private:
		// Pointer to a function
		EventCallback m_CallBack;
	};

	class EventListener
	{
	public:
		virtual ~EventListener() 
		{
			OnDestroy();
		}

		virtual void OnInit() {}
		
		virtual void OnDestroy() {}

		EventListener(bool debugPrint = true) : m_DebugShow(debugPrint)
		{
			m_HandlersMap.clear();
		}

		/*
		* This will be used to get the type of the element
		* It will be used primarly When logging the call to an event
		* */
		virtual std::string GetTypeName() const
		{
			return type(*this);
		}

#ifdef K_DEBUG
		void DumpHandlers() 
		{
			K_CORE_TRACE("\n==========================================================\n");
			K_CORE_TRACE("List of Handlers : \n");
			for (auto pair : m_HandlersMap) {
				K_CORE_TRACE("Found Handler {} for event {}", pair.first, pair.second->GetEventName());
			}
			K_CORE_TRACE("\n==========================================================\n");
		}
#else
		void DumpHandlers() {}
#endif // K_DEBUG


		virtual void OnEvent(Event& e)
		{
			// Call an event function if there is one
			if (m_HandlersMap.find(e.GetType()) != m_HandlersMap.end())
			{
				if (m_DebugShow) {
					K_CORE_DEBUG("Calling Listener {0} for {1}", GetTypeName(), e.Print());
				}
				auto& cb = m_HandlersMap[e.GetType()];
				cb->call(e);
			}
		}

	protected:
		/*
		* For usage in c++ only
		* 
		* TODO : Find an automatic mechanism for python to register 
		*		 event callbacks
		* 
		*/
		template <typename EventType>
		void Bind(const std::function<void(EventType&)>& callback)
		{
			// get event Name and add it to the map
			Ref<HandlerBase> handler(new EventHandler<EventType>(callback));
			m_HandlersMap[EventType::GetStaticType()] = handler;
		}

	private:
		std::unordered_map<std::string, Ref<HandlerBase>> m_HandlersMap;
	protected:
		bool m_DebugShow;
	};
} // namespace KGE
