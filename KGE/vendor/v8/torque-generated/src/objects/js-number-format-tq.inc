class JSNumberFormat;
// Alias for HeapObject::IsJSNumberFormat() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSNumberFormat_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSNumberFormat : public P {
  static_assert(std::is_same<JSNumberFormat, D>::value,
    "Use this class as direct base for JSNumberFormat.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSNumberFormat.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSNumberFormat<D,P>;

inline String locale() const;
inline String locale(PtrComprCageBase cage_base) const;
inline void set_locale(String value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign icu_number_formatter() const;
inline Foreign icu_number_formatter(PtrComprCageBase cage_base) const;
inline void set_icu_number_formatter(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_format() const;
inline HeapObject bound_format(PtrComprCageBase cage_base) const;
inline void set_bound_format(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSNumberFormatVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kLocaleOffset = P::kHeaderSize;
  static constexpr int kLocaleOffsetEnd = kLocaleOffset + kTaggedSize - 1;
  static constexpr int kIcuNumberFormatterOffset = kLocaleOffsetEnd + 1;
  static constexpr int kIcuNumberFormatterOffsetEnd = kIcuNumberFormatterOffset + kTaggedSize - 1;
  static constexpr int kBoundFormatOffset = kIcuNumberFormatterOffsetEnd + 1;
  static constexpr int kBoundFormatOffsetEnd = kBoundFormatOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kBoundFormatOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kBoundFormatOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kBoundFormatOffsetEnd + 1;
  static constexpr int kHeaderSize = kBoundFormatOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSNumberFormat() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSNumberFormat, 
      DAlias>::value,
      "class TorqueGeneratedJSNumberFormat should be used as direct base for JSNumberFormat.");
  }
 protected:
  inline explicit TorqueGeneratedJSNumberFormat(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSNumberFormat(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

