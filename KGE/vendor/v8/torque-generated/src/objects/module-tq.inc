class Module;
class JSModuleNamespace;
// Alias for HeapObject::IsModule() that avoids inlining.
V8_EXPORT_PRIVATE bool IsModule_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedModule : public P {
  static_assert(std::is_same<Module, D>::value,
    "Use this class as direct base for Module.");
  static_assert(std::is_same<HeapObject, P>::value,
    "Pass in HeapObject as second template parameter for TorqueGeneratedModule.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedModule<D,P>;

  // Torque type: ObjectHashTable
inline ObjectHashTable exports() const;
inline ObjectHashTable exports(PtrComprCageBase cage_base) const;
inline void set_exports(ObjectHashTable value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline int hash() const;
inline void set_hash(int value);

inline int status() const;
inline void set_status(int value);

  // Torque type: (Undefined | class JSModuleNamespace)
inline HeapObject module_namespace() const;
inline HeapObject module_namespace(PtrComprCageBase cage_base) const;
inline void set_module_namespace(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Object exception() const;
inline Object exception(PtrComprCageBase cage_base) const;
inline void set_exception(Object value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSPromise)
inline HeapObject top_level_capability() const;
inline HeapObject top_level_capability(PtrComprCageBase cage_base) const;
inline void set_top_level_capability(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void ModuleVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kExportsOffset = P::kHeaderSize;
  static constexpr int kExportsOffsetEnd = kExportsOffset + kTaggedSize - 1;
  static constexpr int kHashOffset = kExportsOffsetEnd + 1;
  static constexpr int kHashOffsetEnd = kHashOffset + kTaggedSize - 1;
  static constexpr int kStatusOffset = kHashOffsetEnd + 1;
  static constexpr int kStatusOffsetEnd = kStatusOffset + kTaggedSize - 1;
  static constexpr int kModuleNamespaceOffset = kStatusOffsetEnd + 1;
  static constexpr int kModuleNamespaceOffsetEnd = kModuleNamespaceOffset + kTaggedSize - 1;
  static constexpr int kExceptionOffset = kModuleNamespaceOffsetEnd + 1;
  static constexpr int kExceptionOffsetEnd = kExceptionOffset + kTaggedSize - 1;
  static constexpr int kTopLevelCapabilityOffset = kExceptionOffsetEnd + 1;
  static constexpr int kTopLevelCapabilityOffsetEnd = kTopLevelCapabilityOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kTopLevelCapabilityOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kTopLevelCapabilityOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kTopLevelCapabilityOffsetEnd + 1;
  static constexpr int kHeaderSize = kTopLevelCapabilityOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedModule() : P() {
    static_assert(std::is_base_of<TorqueGeneratedModule, 
      DAlias>::value,
      "class TorqueGeneratedModule should be used as direct base for Module.");
  }
 protected:
  inline explicit TorqueGeneratedModule(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedModule(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

// Alias for HeapObject::IsJSModuleNamespace() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSModuleNamespace_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSModuleNamespace : public P {
  static_assert(std::is_same<JSModuleNamespace, D>::value,
    "Use this class as direct base for JSModuleNamespace.");
  static_assert(std::is_same<JSSpecialObject, P>::value,
    "Pass in JSSpecialObject as second template parameter for TorqueGeneratedJSModuleNamespace.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSModuleNamespace<D,P>;

inline Module module() const;
inline Module module(PtrComprCageBase cage_base) const;
inline void set_module(Module value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSModuleNamespaceVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kModuleOffset = P::kHeaderSize;
  static constexpr int kModuleOffsetEnd = kModuleOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kModuleOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kModuleOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kModuleOffsetEnd + 1;
  static constexpr int kHeaderSize = kModuleOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSModuleNamespace() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSModuleNamespace, 
      DAlias>::value,
      "class TorqueGeneratedJSModuleNamespace should be used as direct base for JSModuleNamespace.");
  }
 protected:
  inline explicit TorqueGeneratedJSModuleNamespace(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSModuleNamespace(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

