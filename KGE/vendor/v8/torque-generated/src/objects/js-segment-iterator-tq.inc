class JSSegmentIterator;
// Alias for HeapObject::IsJSSegmentIterator() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSSegmentIterator_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSSegmentIterator : public P {
  static_assert(std::is_same<JSSegmentIterator, D>::value,
    "Use this class as direct base for JSSegmentIterator.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSSegmentIterator.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSSegmentIterator<D,P>;

inline Foreign icu_break_iterator() const;
inline Foreign icu_break_iterator(PtrComprCageBase cage_base) const;
inline void set_icu_break_iterator(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign unicode_string() const;
inline Foreign unicode_string(PtrComprCageBase cage_base) const;
inline void set_unicode_string(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline int flags() const;
inline void set_flags(int value);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSSegmentIteratorVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kIcuBreakIteratorOffset = P::kHeaderSize;
  static constexpr int kIcuBreakIteratorOffsetEnd = kIcuBreakIteratorOffset + kTaggedSize - 1;
  static constexpr int kUnicodeStringOffset = kIcuBreakIteratorOffsetEnd + 1;
  static constexpr int kUnicodeStringOffsetEnd = kUnicodeStringOffset + kTaggedSize - 1;
  static constexpr int kFlagsOffset = kUnicodeStringOffsetEnd + 1;
  static constexpr int kFlagsOffsetEnd = kFlagsOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kFlagsOffsetEnd + 1;
  static constexpr int kHeaderSize = kFlagsOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSSegmentIterator() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSSegmentIterator, 
      DAlias>::value,
      "class TorqueGeneratedJSSegmentIterator should be used as direct base for JSSegmentIterator.");
  }
 protected:
  inline explicit TorqueGeneratedJSSegmentIterator(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSSegmentIterator(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

