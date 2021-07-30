class JSDisplayNames;
// Alias for HeapObject::IsJSDisplayNames() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSDisplayNames_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSDisplayNames : public P {
  static_assert(std::is_same<JSDisplayNames, D>::value,
    "Use this class as direct base for JSDisplayNames.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSDisplayNames.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSDisplayNames<D,P>;

inline Foreign internal() const;
inline Foreign internal(PtrComprCageBase cage_base) const;
inline void set_internal(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline int flags() const;
inline void set_flags(int value);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSDisplayNamesVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kInternalOffset = P::kHeaderSize;
  static constexpr int kInternalOffsetEnd = kInternalOffset + kTaggedSize - 1;
  static constexpr int kFlagsOffset = kInternalOffsetEnd + 1;
  static constexpr int kFlagsOffsetEnd = kFlagsOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kHeaderSize = kFlagsOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSDisplayNames() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSDisplayNames, 
      DAlias>::value,
      "class TorqueGeneratedJSDisplayNames should be used as direct base for JSDisplayNames.");
  }
 protected:
  inline explicit TorqueGeneratedJSDisplayNames(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSDisplayNames(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

