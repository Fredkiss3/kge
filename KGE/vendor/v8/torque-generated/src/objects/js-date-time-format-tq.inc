class JSDateTimeFormat;
// Alias for HeapObject::IsJSDateTimeFormat() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSDateTimeFormat_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSDateTimeFormat : public P {
  static_assert(std::is_same<JSDateTimeFormat, D>::value,
    "Use this class as direct base for JSDateTimeFormat.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSDateTimeFormat.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSDateTimeFormat<D,P>;

inline String locale() const;
inline String locale(PtrComprCageBase cage_base) const;
inline void set_locale(String value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign icu_locale() const;
inline Foreign icu_locale(PtrComprCageBase cage_base) const;
inline void set_icu_locale(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign icu_simple_date_format() const;
inline Foreign icu_simple_date_format(PtrComprCageBase cage_base) const;
inline void set_icu_simple_date_format(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign icu_date_interval_format() const;
inline Foreign icu_date_interval_format(PtrComprCageBase cage_base) const;
inline void set_icu_date_interval_format(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_format() const;
inline HeapObject bound_format(PtrComprCageBase cage_base) const;
inline void set_bound_format(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline int flags() const;
inline void set_flags(int value);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSDateTimeFormatVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kLocaleOffset = P::kHeaderSize;
  static constexpr int kLocaleOffsetEnd = kLocaleOffset + kTaggedSize - 1;
  static constexpr int kIcuLocaleOffset = kLocaleOffsetEnd + 1;
  static constexpr int kIcuLocaleOffsetEnd = kIcuLocaleOffset + kTaggedSize - 1;
  static constexpr int kIcuSimpleDateFormatOffset = kIcuLocaleOffsetEnd + 1;
  static constexpr int kIcuSimpleDateFormatOffsetEnd = kIcuSimpleDateFormatOffset + kTaggedSize - 1;
  static constexpr int kIcuDateIntervalFormatOffset = kIcuSimpleDateFormatOffsetEnd + 1;
  static constexpr int kIcuDateIntervalFormatOffsetEnd = kIcuDateIntervalFormatOffset + kTaggedSize - 1;
  static constexpr int kBoundFormatOffset = kIcuDateIntervalFormatOffsetEnd + 1;
  static constexpr int kBoundFormatOffsetEnd = kBoundFormatOffset + kTaggedSize - 1;
  static constexpr int kFlagsOffset = kBoundFormatOffsetEnd + 1;
  static constexpr int kFlagsOffsetEnd = kFlagsOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kHeaderSize = kFlagsOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSDateTimeFormat() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSDateTimeFormat, 
      DAlias>::value,
      "class TorqueGeneratedJSDateTimeFormat should be used as direct base for JSDateTimeFormat.");
  }
 protected:
  inline explicit TorqueGeneratedJSDateTimeFormat(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSDateTimeFormat(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

