class JSLocale;
// Alias for HeapObject::IsJSLocale() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSLocale_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSLocale : public P {
  static_assert(std::is_same<JSLocale, D>::value,
    "Use this class as direct base for JSLocale.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSLocale.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSLocale<D,P>;

inline Foreign icu_locale() const;
inline Foreign icu_locale(PtrComprCageBase cage_base) const;
inline void set_icu_locale(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSLocaleVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kIcuLocaleOffset = P::kHeaderSize;
  static constexpr int kIcuLocaleOffsetEnd = kIcuLocaleOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kIcuLocaleOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kIcuLocaleOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kIcuLocaleOffsetEnd + 1;
  static constexpr int kHeaderSize = kIcuLocaleOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSLocale() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSLocale, 
      DAlias>::value,
      "class TorqueGeneratedJSLocale should be used as direct base for JSLocale.");
  }
 protected:
  inline explicit TorqueGeneratedJSLocale(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSLocale(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

