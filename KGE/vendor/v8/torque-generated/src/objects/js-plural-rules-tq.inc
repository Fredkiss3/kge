class JSPluralRules;
// Alias for HeapObject::IsJSPluralRules() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSPluralRules_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSPluralRules : public P {
  static_assert(std::is_same<JSPluralRules, D>::value,
    "Use this class as direct base for JSPluralRules.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSPluralRules.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSPluralRules<D,P>;

inline String locale() const;
inline String locale(PtrComprCageBase cage_base) const;
inline void set_locale(String value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline int flags() const;
inline void set_flags(int value);

inline Foreign icu_plural_rules() const;
inline Foreign icu_plural_rules(PtrComprCageBase cage_base) const;
inline void set_icu_plural_rules(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign icu_number_formatter() const;
inline Foreign icu_number_formatter(PtrComprCageBase cage_base) const;
inline void set_icu_number_formatter(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSPluralRulesVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kLocaleOffset = P::kHeaderSize;
  static constexpr int kLocaleOffsetEnd = kLocaleOffset + kTaggedSize - 1;
  static constexpr int kFlagsOffset = kLocaleOffsetEnd + 1;
  static constexpr int kFlagsOffsetEnd = kFlagsOffset + kTaggedSize - 1;
  static constexpr int kIcuPluralRulesOffset = kFlagsOffsetEnd + 1;
  static constexpr int kIcuPluralRulesOffsetEnd = kIcuPluralRulesOffset + kTaggedSize - 1;
  static constexpr int kIcuNumberFormatterOffset = kIcuPluralRulesOffsetEnd + 1;
  static constexpr int kIcuNumberFormatterOffsetEnd = kIcuNumberFormatterOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kIcuNumberFormatterOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kIcuNumberFormatterOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kIcuNumberFormatterOffsetEnd + 1;
  static constexpr int kHeaderSize = kIcuNumberFormatterOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSPluralRules() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSPluralRules, 
      DAlias>::value,
      "class TorqueGeneratedJSPluralRules should be used as direct base for JSPluralRules.");
  }
 protected:
  inline explicit TorqueGeneratedJSPluralRules(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSPluralRules(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

